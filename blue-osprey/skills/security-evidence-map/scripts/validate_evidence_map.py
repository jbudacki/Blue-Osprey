#!/usr/bin/env python3
"""Validate a Blue Osprey security evidence map in canonical Markdown form."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = (
    "id",
    "action",
    "where to point",
    "evidence shown",
    "source -> sink / impact",
    "soc evidence to collect",
    "status",
)

VALID_STATUSES = (
    "Confirmed in source — operationally unverified — open",
    "Confirmed in source — SOC corroborated — open",
    "Conditionally reachable — evidence needed",
    "Evidence gap confirmed — action open",
    "Hypothesis — insufficient source evidence",
    "Remediated — verification pending",
    "Closed — verified",
    "Accepted risk — approval reference required",
)

SOURCE_CLAIM_STATUSES = {
    "Confirmed in source — operationally unverified — open",
    "Confirmed in source — SOC corroborated — open",
    "Conditionally reachable — evidence needed",
    "Evidence gap confirmed — action open",
    "Remediated — verification pending",
    "Closed — verified",
    "Accepted risk — approval reference required",
}

FILE_REFERENCE_RE = re.compile(
    r"(?P<path>(?:/|\.{1,2}/)?[^\s`|()\[\]<>]+?\.[A-Za-z0-9]{1,12})"
    r"(?::(?P<start>\d+)(?:-(?P<end>\d+))?)?"
    r"(?=$|[\s,);])"
)
ANCHORED_FILE_REFERENCE_RE = re.compile(
    r"^(?P<path>.+?\.[A-Za-z0-9]{1,12})"
    r"(?::(?P<start>\d+)(?:-(?P<end>\d+))?)?"
    r"(?:#.*)?$"
)
MALFORMED_LINE_RE = re.compile(
    r"(?:/|\.{1,2}/)?[^\s`|()\[\]<>]+?\.[A-Za-z0-9]{1,12}:"
    r"(?P<line>[^\d\s`][^\s,);`]*)"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
STABLE_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,15}-\d+[A-Z]?(?:-\d+)?\b")
OPERATIONAL_REFERENCE_RE = re.compile(
    r"\b(?:SOC|SIEM|WAF|CloudTrail|incident|case|alert|telemetry|log|dashboard|"
    r"audit event|provider usage)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str
    line: int | None = None
    row_id: str | None = None


@dataclass(frozen=True)
class LocalReference:
    raw: str
    path: str
    start: int | None
    end: int | None


def normalize_header(value: str) -> str:
    value = clean_text(value).lower().replace("→", "->")
    return re.sub(r"\s+", " ", value).strip()


def clean_text(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("**", "").replace("__", "").replace("`", "")
    return re.sub(r"\s+", " ", value).strip()


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith(r"\|"):
        stripped = stripped[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    in_code = False
    for character in stripped:
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\":
            escaped = True
            current.append(character)
            continue
        if character == "`":
            in_code = not in_code
            current.append(character)
            continue
        if character == "|" and not in_code:
            cells.append("".join(current).strip().replace(r"\|", "|"))
            current = []
            continue
        current.append(character)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip().replace(r"\|", "|"))
    return cells


def is_separator_row(cells: Iterable[str]) -> bool:
    cells = list(cells)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def find_canonical_table(lines: list[str]) -> tuple[int, list[str], list[tuple[int, list[str]]]] | None:
    required = set(REQUIRED_COLUMNS)
    for index, line in enumerate(lines):
        if "|" not in line:
            continue
        headers = split_table_row(line)
        normalized = [normalize_header(header) for header in headers]
        if len(required.intersection(normalized)) < 4:
            continue
        if index + 1 >= len(lines) or not is_separator_row(split_table_row(lines[index + 1])):
            continue
        rows: list[tuple[int, list[str]]] = []
        for row_index in range(index + 2, len(lines)):
            row_line = lines[row_index]
            if not row_line.strip() or "|" not in row_line:
                break
            cells = split_table_row(row_line)
            if is_separator_row(cells):
                continue
            rows.append((row_index + 1, cells))
        return index + 1, normalized, rows
    return None


def parse_status(value: str) -> str | None:
    cleaned = clean_text(value)
    for status in sorted(VALID_STATUSES, key=len, reverse=True):
        if cleaned == status or cleaned.startswith(f"{status};"):
            return status
    return None


def has_source_reference(value: str) -> bool:
    return bool(
        MARKDOWN_LINK_RE.search(value)
        or INLINE_CODE_RE.search(value)
        or STABLE_ID_RE.search(clean_text(value))
        or FILE_REFERENCE_RE.search(value)
    )


def extract_local_references(value: str) -> list[LocalReference]:
    anchored_candidates = list(MARKDOWN_LINK_RE.findall(value))
    text_without_links = MARKDOWN_LINK_RE.sub("", value)
    anchored_candidates.extend(INLINE_CODE_RE.findall(text_without_links))
    raw_text = INLINE_CODE_RE.sub("", text_without_links)
    references: dict[tuple[str, int | None, int | None], LocalReference] = {}
    for candidate in anchored_candidates:
        candidate = candidate.strip().strip("<>")
        if "://" in candidate or candidate.startswith(("mailto:", "#")):
            continue
        match = ANCHORED_FILE_REFERENCE_RE.fullmatch(candidate)
        if match:
            path = match.group("path").strip()
            start = int(match.group("start")) if match.group("start") else None
            end = int(match.group("end")) if match.group("end") else None
            key = (path, start, end)
            references[key] = LocalReference(candidate, path, start, end)
    for match in FILE_REFERENCE_RE.finditer(raw_text):
        path = match.group("path").strip()
        start = int(match.group("start")) if match.group("start") else None
        end = int(match.group("end")) if match.group("end") else None
        key = (path, start, end)
        references[key] = LocalReference(match.group(0), path, start, end)
    return list(references.values())


def reference_path(reference: LocalReference, repo_root: Path) -> Path:
    candidate = Path(reference.path).expanduser()
    return candidate if candidate.is_absolute() else repo_root / candidate


def validate_local_reference(
    reference: LocalReference,
    repo_root: Path,
    strict: bool,
    line: int,
    row_id: str,
) -> list[Issue]:
    issues: list[Issue] = []
    level = "error" if strict else "warning"
    if reference.start is not None and reference.start < 1:
        issues.append(Issue("error", "invalid-line", f"reference {reference.raw!r} uses a line below 1", line, row_id))
        return issues
    if reference.end is not None and reference.start is not None and reference.end < reference.start:
        issues.append(Issue("error", "reversed-line-range", f"reference {reference.raw!r} has a reversed line range", line, row_id))
        return issues

    resolved = reference_path(reference, repo_root)
    if not resolved.is_file():
        issues.append(Issue(level, "missing-local-reference", f"local reference does not exist: {resolved}", line, row_id))
        return issues
    if reference.start is not None:
        try:
            with resolved.open("r", encoding="utf-8", errors="replace") as source:
                line_count = sum(1 for _ in source)
        except OSError as error:
            issues.append(Issue(level, "unreadable-local-reference", f"cannot read {resolved}: {error}", line, row_id))
            return issues
        requested_end = reference.end or reference.start
        if requested_end > line_count:
            issues.append(Issue(level, "line-out-of-range", f"reference {reference.raw!r} exceeds {resolved}'s {line_count} lines", line, row_id))
    return issues


def validate_markdown(
    text: str,
    *,
    repo_root: Path | None = None,
    strict_local_references: bool = False,
) -> tuple[list[Issue], int]:
    lines = text.splitlines()
    table = find_canonical_table(lines)
    if table is None:
        return [Issue("error", "missing-canonical-table", "canonical evidence-map table was not found")], 0

    header_line, headers, table_rows = table
    issues: list[Issue] = []
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in headers]
    if missing_columns:
        issues.append(Issue("error", "missing-columns", f"missing columns: {', '.join(missing_columns)}", header_line))
        return issues, 0
    if not table_rows:
        issues.append(Issue("error", "missing-rows", "canonical evidence-map table has no data rows", header_line))
        return issues, 0

    column_index = {header: index for index, header in enumerate(headers)}
    seen_ids: set[str] = set()
    for line_number, cells in table_rows:
        if len(cells) != len(headers):
            issues.append(Issue("error", "column-count", f"row has {len(cells)} cells; expected {len(headers)}", line_number))
            continue
        row = {header: cells[index] for header, index in column_index.items()}
        row_id = clean_text(row["id"])
        if not row_id:
            issues.append(Issue("error", "missing-id", "row ID is empty", line_number))
        elif row_id in seen_ids:
            issues.append(Issue("error", "duplicate-id", f"duplicate row ID: {row_id}", line_number, row_id))
        else:
            seen_ids.add(row_id)

        for column in (
            "action",
            "where to point",
            "evidence shown",
            "source -> sink / impact",
            "soc evidence to collect",
            "status",
        ):
            if not clean_text(row[column]):
                issues.append(Issue("error", "empty-cell", f"{column} is empty", line_number, row_id or None))

        status = parse_status(row["status"])
        if clean_text(row["status"]) and status is None:
            issues.append(Issue("error", "uncontrolled-status", "status is not in the controlled status model", line_number, row_id or None))
        if status in SOURCE_CLAIM_STATUSES and not has_source_reference(row["where to point"]):
            issues.append(Issue("error", "confirmed-without-source", "status requires a recognizable source evidence reference", line_number, row_id or None))
        if status == "Confirmed in source — SOC corroborated — open" and not OPERATIONAL_REFERENCE_RE.search(row["where to point"]):
            issues.append(Issue("error", "corroborated-without-operational-reference", "SOC-corroborated status requires an operational evidence reference", line_number, row_id or None))

        for malformed in MALFORMED_LINE_RE.finditer(row["where to point"]):
            issues.append(Issue("error", "malformed-line-reference", f"file line must be numeric: {malformed.group(0)!r}", line_number, row_id or None))

        for reference in extract_local_references(row["where to point"]):
            if reference.start is not None and reference.start < 1:
                issues.append(Issue("error", "invalid-line", f"reference {reference.raw!r} uses a line below 1", line_number, row_id or None))
            if reference.end is not None and reference.start is not None and reference.end < reference.start:
                issues.append(Issue("error", "reversed-line-range", f"reference {reference.raw!r} has a reversed line range", line_number, row_id or None))
            if repo_root is not None:
                issues.extend(validate_local_reference(reference, repo_root, strict_local_references, line_number, row_id))

    return issues, len(table_rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_map", type=Path, help="Markdown evidence map to validate")
    parser.add_argument("--repo-root", type=Path, help="Resolve relative local evidence references from this directory")
    parser.add_argument("--strict-local-references", action="store_true", help="Treat missing, unreadable, or out-of-range local references as errors")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit a machine-readable validation result")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.strict_local_references and args.repo_root is None:
        parser.error("--strict-local-references requires --repo-root")
    try:
        text = args.evidence_map.read_text(encoding="utf-8")
    except OSError as error:
        if args.json_output:
            print(json.dumps({"valid": False, "readError": str(error), "issues": []}, indent=2))
        else:
            print(f"validation error: cannot read {args.evidence_map}: {error}", file=sys.stderr)
        return 2

    repo_root = args.repo_root.resolve() if args.repo_root else None
    issues, row_count = validate_markdown(
        text,
        repo_root=repo_root,
        strict_local_references=args.strict_local_references,
    )
    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]

    if args.json_output:
        print(json.dumps({
            "valid": not errors,
            "rowCount": row_count,
            "errorCount": len(errors),
            "warningCount": len(warnings),
            "issues": [asdict(issue) for issue in issues],
        }, indent=2))
    else:
        for issue in issues:
            location = f" line {issue.line}" if issue.line is not None else ""
            row = f" row {issue.row_id}" if issue.row_id else ""
            print(f"{issue.level}:{location}{row} [{issue.code}] {issue.message}")
        if not errors:
            print(f"validated {row_count} evidence-map rows with {len(warnings)} warning(s)")
        else:
            print(f"validation failed with {len(errors)} error(s) and {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

PATTERNS = {
    'api_keys': [
        (r'sk-(?:(?:proj|svcacct)-)?[a-zA-Z0-9_-]{20,}', 'OpenAI API Key', 'CRITICAL', 'HIGH'),
        (r'pk_(?:test|live)_[a-zA-Z0-9]{24,}', 'Stripe Publishable Key', 'HIGH', 'HIGH'),
        (r'sk_(?:test|live)_[a-zA-Z0-9]{24,}', 'Stripe Secret Key', 'CRITICAL', 'HIGH'),
        (r'(?:gh[pousr]_[a-zA-Z0-9]{36,255}|github_pat_[a-zA-Z0-9_]{22,255})', 'GitHub Access Token', 'CRITICAL', 'HIGH'),
    ],
    'cloud': [
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID', 'CRITICAL', 'HIGH'),
        (r"aws_secret_access_key\s*[:=]\s*[\"'][a-zA-Z0-9/+=]{40}[\"']", 'AWS Secret Access Key', 'CRITICAL', 'HIGH'),
    ],
    'database': [
        (r"postgres(?:ql)?://[^\s\"']+:[^\s\"']+@[^\s\"']+", 'PostgreSQL Connection String', 'CRITICAL', 'HIGH'),
        (r"mongodb(?:\+srv)?://[^\s\"']+:[^\s\"']+@[^\s\"']+", 'MongoDB Connection String', 'CRITICAL', 'HIGH'),
    ],
    'crypto': [
        (r'-----BEGIN (?:RSA|EC|OPENSSH)? ?PRIVATE KEY-----', 'Private Key', 'CRITICAL', 'HIGH'),
    ],
    'services': [
        (r'xox[baprs]-[0-9a-zA-Z-]{10,100}', 'Slack Token', 'CRITICAL', 'HIGH'),
    ],
}

DEFAULT_SKIP_DIRS = {
    '.git', '.hg', '.svn', '.agents', '.pytest_cache', '.mypy_cache',
    '.ruff_cache', 'node_modules', 'vendor', '__pycache__', '.venv',
    'venv', 'dist', 'build', 'coverage', 'htmlcov',
}
DEFAULT_MAX_FILE_BYTES = 1_000_000

def fingerprint(value):
    digest = hashlib.sha256(value.encode('utf-8', errors='ignore')).hexdigest()[:12]
    return f'<redacted len={len(value)} sha256_12={digest}>'

def build_skip_dirs(extra_skip_dirs=None, include_agent_skills=False):
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    if include_agent_skills:
        skip_dirs.discard('.agents')
    for value in extra_skip_dirs or []:
        skip_dirs.add(Path(value).name)
    return skip_dirs


def scan_directory(path, categories, skip_dirs, max_file_bytes):
    results = []
    target_patterns = []
    if categories:
        for cat in categories:
            target_patterns.extend((cat, *pattern) for pattern in PATTERNS[cat])
    else:
        for category, cat_patterns in PATTERNS.items():
            target_patterns.extend((category, *pattern) for pattern in cat_patterns)

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                if file_path.stat().st_size > max_file_bytes:
                    continue
                content = file_path.read_text(errors='ignore')
            except Exception:
                continue
            for category, pattern, name, severity, confidence in target_patterns:
                for match in re.finditer(pattern, content):
                    line_no = content[:match.start()].count('\n') + 1
                    results.append({
                        'status': 'candidate',
                        'category': category,
                        'type': name,
                        'file': str(file_path),
                        'line': line_no,
                        'severity': severity,
                        'confidence': confidence,
                        'evidence': fingerprint(match.group(0)),
                    })
    return results

def main():
    parser = argparse.ArgumentParser(description='Secrets Analysis Scanner')
    parser.add_argument('--path', default='.', help='Path to scan')
    parser.add_argument('--category', action='append', help='Categories to scan')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--validate', action='store_true', help='Reserved for explicitly authorized active validation')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Additional directory name to skip; repeat as needed')
    parser.add_argument('--include-agent-skills', action='store_true', help='Include .agents directories, which are skipped by default')
    parser.add_argument('--max-file-bytes', type=int, default=DEFAULT_MAX_FILE_BYTES, help='Skip files larger than this size')
    args = parser.parse_args()

    if args.validate:
        parser.error('Active validation is not implemented; no credential validation was attempted')
    target = Path(args.path)
    if not target.is_dir():
        parser.error(f'Not a directory: {target}')
    if args.max_file_bytes < 1:
        parser.error('--max-file-bytes must be positive')
    unknown_categories = sorted(set(args.category or []) - set(PATTERNS))
    if unknown_categories:
        parser.error(f"Unknown categories: {', '.join(unknown_categories)}")

    skip_dirs = build_skip_dirs(args.exclude_dir, args.include_agent_skills)
    results = scan_directory(str(target), args.category, skip_dirs, args.max_file_bytes)
    if args.json:
        print(json.dumps({
            'status': 'candidates_only',
            'note': 'Matches require manual validation; active validation was not performed.',
            'results': results,
        }, indent=2))
    else:
        print(f'--- Secrets Scan Results ({len(results)} candidates) ---')
        if not results:
            print('No candidates found. This does not prove the repository contains no secrets.')
        for r in results:
            print(f"[{r['severity']}/{r['confidence']}] candidate: {r['type']} at {r['file']}:{r['line']} {r['evidence']}")

if __name__ == '__main__':
    main()

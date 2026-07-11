import argparse
import json
import os
import re
from pathlib import Path

DEFAULT_SKIP_DIRS = {
    '.git', '.hg', '.svn', '.agents', '.pytest_cache', '.mypy_cache',
    '.ruff_cache', 'node_modules', 'vendor', '__pycache__', '.venv',
    'venv', 'dist', 'build', 'coverage', 'htmlcov',
}
SCAN_SUFFIXES = ('.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java', '.rb', '.php', '.yaml', '.yml', '.json', '.toml')
DEFAULT_MAX_FILE_BYTES = 1_000_000

CATEGORY_SPECS = {
    'discovery': {
        'pattern': r'\b(?:from|import)\s+(?:openai|anthropic|langchain|llama_index)|(?:require|from)\s*\(?[\'"](?:openai|@anthropic-ai/sdk|langchain)',
        'severity': 'INFO',
        'confidence': 'HIGH',
        'reason': 'Identifies an LLM integration surface; it is not a vulnerability.',
    },
    'secrets': {
        'pattern': r'sk-(?:proj-)?[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{16,}|OPENAI_API_KEY|ANTHROPIC_API_KEY',
        'severity': 'HIGH',
        'confidence': 'MEDIUM',
        'reason': 'Confirm whether the match is a real credential rather than a variable name or fixture.',
    },
    'injection': {
        'pattern': r'prompt\s*=.*(?:input|request|query)|prompt\s*\+.*(?:input|request|query)|f[\'"].*\{.*(?:input|request|query)',
        'severity': 'HIGH',
        'confidence': 'LOW',
        'reason': 'String construction alone is not prompt injection; trace untrusted data and downstream authority.',
    },
    'output': {
        'pattern': r'(?:eval|exec)\(.*(?:response|completion|output)|innerHTML\s*=.*(?:response|completion|output)|execute\(?.*(?:response|completion|output)',
        'severity': 'HIGH',
        'confidence': 'MEDIUM',
        'reason': 'Confirm that model-controlled output reaches an executable or unsafe rendering sink.',
    },
    'agency': {
        'pattern': r'(?:function|tool).*(?:call|use).*(?:delete|drop|transfer|send|publish)|agent.*action.*(?:delete|drop|transfer|send|publish)',
        'severity': 'MEDIUM',
        'confidence': 'LOW',
        'reason': 'Confirm permissions, user approval, parameter validation, and rollback controls.',
    },
    'config': {
        'pattern': r'temperature|top_p|max_(?:tokens|output_tokens)|rate[_ -]?limit',
        'severity': 'INFO',
        'confidence': 'LOW',
        'reason': 'Configuration presence is a review signal, not a security defect.',
    },
}


def build_skip_dirs(extra_skip_dirs=None, include_agent_skills=False):
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    if include_agent_skills:
        skip_dirs.discard('.agents')
    for value in extra_skip_dirs or []:
        skip_dirs.add(Path(value).name)
    return skip_dirs


def scan_directory(path, category, spec, skip_dirs, max_file_bytes):
    results = []
    regex = re.compile(spec['pattern'], re.IGNORECASE)
    for root, dirs, files in os.walk(path):
        dirs[:] = [name for name in dirs if name not in skip_dirs]
        for name in files:
            if not (name.endswith(SCAN_SUFFIXES) or name.startswith('.env')):
                continue
            file_path = Path(root) / name
            try:
                if file_path.stat().st_size > max_file_bytes:
                    continue
                with file_path.open('r', errors='ignore') as handle:
                    for line_number, line in enumerate(handle, 1):
                        if regex.search(line):
                            results.append({
                                'status': 'candidate',
                                'category': category,
                                'severity': spec['severity'],
                                'confidence': spec['confidence'],
                                'reason': spec['reason'],
                                'file': str(file_path),
                                'line': line_number,
                                'content': line.strip(),
                            })
            except Exception:
                continue
    return results

def main():
    parser = argparse.ArgumentParser(description='LLM Security Scanner')
    parser.add_argument('--discover', action='store_true', help='Discover LLM usage')
    parser.add_argument('--secrets', action='store_true', help='Scan for secrets')
    parser.add_argument('--injection', action='store_true', help='Scan for prompt injection vectors')
    parser.add_argument('--output', action='store_true', help='Scan for output handling risks')
    parser.add_argument('--agency', action='store_true', help='Scan for excessive agency')
    parser.add_argument('--config', action='store_true', help='Scan for config risks')
    parser.add_argument('--all', action='store_true', help='Run all scans')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--path', default='.', help='Path to scan')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Additional directory name to skip; repeat as needed')
    parser.add_argument('--include-agent-skills', action='store_true', help='Include .agents directories, which are skipped by default')
    parser.add_argument('--max-file-bytes', type=int, default=DEFAULT_MAX_FILE_BYTES, help='Skip files larger than this size')
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        parser.error(f'Not a directory: {target}')
    if args.max_file_bytes < 1:
        parser.error('--max-file-bytes must be positive')

    selected = {
        'discovery': args.discover,
        'secrets': args.secrets,
        'injection': args.injection,
        'output': args.output,
        'agency': args.agency,
        'config': args.config,
    }
    if args.all:
        selected = {name: True for name in selected}
    if not any(selected.values()):
        parser.error('Select at least one scan category or use --all')

    skip_dirs = build_skip_dirs(args.exclude_dir, args.include_agent_skills)
    all_results = {
        name: scan_directory(str(target), name, CATEGORY_SPECS[name], skip_dirs, args.max_file_bytes)
        for name, enabled in selected.items()
        if enabled
    }

    if args.json:
        print(json.dumps({
            'status': 'candidates_only',
            'note': 'Matches require source-to-sink validation before reporting.',
            'results': all_results,
        }, indent=2))
    else:
        for category, results in all_results.items():
            print(f"\n--- {category.upper()} ---")
            if not results:
                print('No candidates found. This does not prove the category is safe.')
            for r in results[:10]:
                print(f"[{r['severity']}/{r['confidence']}] candidate at {r['file']}:{r['line']} - {r['content']}")
                print(f"  Review: {r['reason']}")
            if len(results) > 10:
                print(f"... and {len(results)-10} more.")

if __name__ == '__main__':
    main()

import argparse
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path

DEFAULT_SKIP_DIRS = {
    '.git', '.hg', '.svn', '.agents', '.pytest_cache', '.mypy_cache',
    '.ruff_cache', 'node_modules', 'vendor', '__pycache__', '.venv',
    'venv', 'dist', 'build', 'coverage', 'htmlcov',
}
ANALYSIS_EXTS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.kt',
    '.rb', '.php', '.cs', '.tf', '.yaml', '.yml', '.json', '.toml', '.sh',
}
DEFAULT_MAX_FILE_BYTES = 1_000_000

SECURITY_PATTERNS = (
    {
        'type': 'Potential hardcoded secret marker',
        'pattern': r'(api[_-]?key|secret|password|token)\s*[:=]',
        'severity': 'MEDIUM',
        'confidence': 'LOW',
        'reason': 'Assignment-like secret markers require credential-specific validation.',
    },
    {
        'type': 'Dynamic code execution',
        'pattern': r'\b(eval|exec)\s*\(',
        'severity': 'HIGH',
        'confidence': 'MEDIUM',
        'reason': 'Risk depends on whether untrusted input reaches the evaluated value.',
    },
    {
        'type': 'Shell execution',
        'pattern': r'(os\.system|subprocess\.(run|call|Popen)|child_process\.exec)',
        'severity': 'MEDIUM',
        'confidence': 'MEDIUM',
        'reason': 'Risk depends on argument construction and attacker control.',
    },
    {
        'type': 'SQL string construction',
        'pattern': r'(execute|query)\s*\([^\n]*(%s|\.format\(|\+)',
        'severity': 'HIGH',
        'confidence': 'LOW',
        'reason': 'Confirm whether the constructed value reaches a query without parameterization.',
    },
    {
        'type': 'Broad network exposure',
        'pattern': r'0\.0\.0\.0/0|::/0',
        'severity': 'MEDIUM',
        'confidence': 'MEDIUM',
        'reason': 'Exposure may be intentional or mitigated by other controls.',
    },
    {
        'type': 'LLM or tool integration',
        'pattern': r'(openai|anthropic|langchain|tool_call|function_call)',
        'severity': 'INFO',
        'confidence': 'MEDIUM',
        'reason': 'This is an attack-surface signal, not a vulnerability.',
    },
)


def build_skip_dirs(extra_skip_dirs=None, include_agent_skills=False):
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    if include_agent_skills:
        skip_dirs.discard('.agents')
    for value in extra_skip_dirs or []:
        skip_dirs.add(Path(value).name)
    return skip_dirs


def walk_files(path, skip_dirs):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for name in files:
            yield Path(root) / name


def get_file_distribution(path, skip_dirs):
    ext_counter = Counter()
    total_files = 0
    for file_path in walk_files(path, skip_dirs):
        ext = file_path.suffix.lower() or '<no_ext>'
        ext_counter[ext] += 1
        total_files += 1
    return ext_counter, total_files


def detect_tech_stack(path, skip_dirs):
    stack = set()
    indicators = {
        'package.json': 'Node.js',
        'pnpm-lock.yaml': 'Node.js/pnpm',
        'yarn.lock': 'Node.js/Yarn',
        'requirements.txt': 'Python',
        'pyproject.toml': 'Python',
        'uv.lock': 'Python/uv',
        'Cargo.toml': 'Rust',
        'go.mod': 'Go',
        'pom.xml': 'Java/Maven',
        'build.gradle': 'Java/Gradle',
        'Gemfile': 'Ruby',
        'composer.json': 'PHP',
        'Makefile': 'Make',
        'Dockerfile': 'Docker',
        'docker-compose.yml': 'Docker Compose',
        'docker-compose.yaml': 'Docker Compose',
    }
    for file_path in walk_files(path, skip_dirs):
        if file_path.name in indicators:
            stack.add(indicators[file_path.name])
        if file_path.suffix == '.tf':
            stack.add('Terraform')
        if file_path.suffix in {'.k8s', '.helm'} or 'kubernetes' in str(file_path).lower():
            stack.add('Kubernetes')
    return sorted(stack)

def safe_read(file_path, max_file_bytes):
    if file_path.suffix.lower() not in ANALYSIS_EXTS:
        return ''
    try:
        if file_path.stat().st_size > max_file_bytes:
            return ''
        return file_path.read_text(errors='ignore')
    except Exception:
        return ''


def find_integrations(path, skip_dirs, max_file_bytes):
    patterns = {
        'LLM/AI': r'openai|anthropic|langchain|llamaindex|huggingface|bedrock|vertexai',
        'Cloud': r'aws_|azure|google-cloud|boto3|@aws-sdk|cloudformation|terraform',
        'Payments': r'stripe|adyen|paypal|braintree',
        'Messaging': r'slack|twilio|sendgrid|\b(?:ses|sns|sqs)\b|kafka|rabbitmq',
        'Datastores': r'postgres|mysql|mongodb|redis|dynamodb|elasticsearch|opensearch|pinecone|weaviate|chroma',
        'Auth': r'oauth|oidc|saml|jwt|passport|auth0|okta|cognito',
    }
    counts = Counter()
    samples = {k: [] for k in patterns}
    for file_path in walk_files(path, skip_dirs):
        text = safe_read(file_path, max_file_bytes)
        if not text:
            continue
        lower = text.lower()
        for label, pattern in patterns.items():
            if re.search(pattern, lower):
                counts[label] += 1
                if len(samples[label]) < 5:
                    samples[label].append(str(file_path))
    return {
        'status': 'signals_only',
        'counts': dict(counts),
        'samples': samples,
        'note': 'Integration matches identify review surfaces, not confirmed dependencies.',
    }


def find_security_patterns(path, skip_dirs, max_file_bytes):
    candidates = []
    for file_path in walk_files(path, skip_dirs):
        text = safe_read(file_path, max_file_bytes)
        if not text:
            continue
        for spec in SECURITY_PATTERNS:
            for match in re.finditer(spec['pattern'], text, re.IGNORECASE):
                line_no = text[:match.start()].count('\n') + 1
                candidates.append({
                    'status': 'candidate',
                    'type': spec['type'],
                    'file': str(file_path),
                    'line': line_no,
                    'severity': spec['severity'],
                    'confidence': spec['confidence'],
                    'reason': spec['reason'],
                })
                break
    return candidates[:100]

def git_analysis(path):
    repo = Path(path)
    if not (repo / '.git').exists():
        return {'git_present': False}
    def run(args):
        try:
            out = subprocess.check_output(args, cwd=path, stderr=subprocess.DEVNULL, text=True).strip()
            return out
        except Exception:
            return ''
    return {
        'git_present': True,
        'current_branch': run(['git', 'branch', '--show-current']),
        'dirty_files': len([x for x in run(['git', 'status', '--short']).splitlines() if x]),
        'commits_last_14_days': len([x for x in run(['git', 'log', '--since=14 days ago', '--oneline']).splitlines() if x]),
        'recent_authors': run(['git', 'log', '--since=90 days ago', '--format=%an']).splitlines()[:10],
    }

def main():
    parser = argparse.ArgumentParser(description='Codebase Discovery Tool')
    parser.add_argument('command', nargs='?', default='full-report', choices=['structure', 'tech-stack', 'git-analysis', 'integrations', 'security', 'full-report'])
    parser.add_argument('--path', default='.', help='Path to scan')
    parser.add_argument('--json', action='store_true', help='Output JSON for commands that normally print text')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Additional directory name to skip; repeat as needed')
    parser.add_argument('--include-agent-skills', action='store_true', help='Include .agents directories, which are skipped by default')
    parser.add_argument('--max-file-bytes', type=int, default=DEFAULT_MAX_FILE_BYTES, help='Skip analysis of files larger than this size')
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        parser.error(f'Not a directory: {target}')
    if args.max_file_bytes < 1:
        parser.error('--max-file-bytes must be positive')

    path = str(target)
    skip_dirs = build_skip_dirs(args.exclude_dir, args.include_agent_skills)
    exts, total = get_file_distribution(path, skip_dirs)

    if args.command == 'structure':
        payload = {'total_files': total, 'file_distribution': dict(exts.most_common(20))}
    elif args.command == 'tech-stack':
        payload = {'tech_stack': detect_tech_stack(path, skip_dirs)}
    elif args.command == 'git-analysis':
        payload = git_analysis(path)
    elif args.command == 'integrations':
        payload = find_integrations(path, skip_dirs, args.max_file_bytes)
    elif args.command == 'security':
        payload = {
            'status': 'candidates_only',
            'candidates': find_security_patterns(path, skip_dirs, args.max_file_bytes),
            'note': 'Candidates require source-to-sink validation before reporting.',
        }
    else:
        payload = {
            'total_files': total,
            'top_extensions': dict(exts.most_common(10)),
            'tech_stack': detect_tech_stack(path, skip_dirs),
            'git': git_analysis(path),
            'integrations': find_integrations(path, skip_dirs, args.max_file_bytes),
            'security_candidates': find_security_patterns(path, skip_dirs, args.max_file_bytes)[:25],
            'analysis_note': 'Security candidates are unverified and require manual source-to-sink review.',
        }

    if args.json or args.command == 'full-report':
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f'{key}: {value}')

if __name__ == '__main__':
    main()

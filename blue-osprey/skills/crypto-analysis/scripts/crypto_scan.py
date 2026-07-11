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
SCAN_SUFFIXES = ('.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.java', '.c', '.cc', '.cpp', '.cs', '.rb', '.php')
DEFAULT_MAX_FILE_BYTES = 1_000_000

PATTERNS = {
    'broken_algorithms': [
        (r'\b(?:hashlib\.md5|MD5\.Create|createHash\(\s*[\'"]md5[\'"]|MessageDigest\.getInstance\(\s*[\'"]MD5[\'"])', 'MD5 in a cryptographic API', 'MEDIUM', 'HIGH', 'Confirm whether MD5 is used for a security property rather than a non-adversarial checksum.'),
        (r'\b(?:hashlib\.sha1|SHA1\.Create|createHash\(\s*[\'"]sha-?1[\'"]|MessageDigest\.getInstance\(\s*[\'"]SHA-?1[\'"])', 'SHA-1 in a cryptographic API', 'MEDIUM', 'HIGH', 'Confirm whether collision or signature resistance is required in this context.'),
        (r'\b(?:DES\.new|DESede|createCipheriv\(\s*[\'"][^\'"]*des|Cipher\.getInstance\(\s*[\'"][^\'"]*DES)', 'DES-family cipher use', 'HIGH', 'HIGH', 'Confirm the algorithm, effective key strength, and migration constraints.'),
        (r'\b(?:ARC4\.new|createCipheriv\(\s*[\'"][^\'"]*(?:rc4|arc4)|Cipher\.getInstance\(\s*[\'"](?:RC4|ARCFOUR))', 'RC4-family cipher use', 'HIGH', 'HIGH', 'Confirm the runtime path and replace stream-cipher use with an authenticated modern construction.'),
    ],
    'weak_modes': [
        (r'\b(?:MODE_ECB|AES[/_-]?ECB|aes-[0-9]+-ecb)\b', 'ECB block-cipher mode', 'HIGH', 'HIGH', 'Confirm the mode is used for sensitive data and replace it with an authenticated mode.'),
    ],
    'weak_asymmetric': [
        (r'\b(?:RSA[^\n]{0,80}1024|key_size\s*=\s*1024)\b', 'RSA 1024-bit key configuration', 'HIGH', 'MEDIUM', 'Confirm this value configures an RSA key and is reachable in production.'),
    ],
    'insecure_rng': [
        (r'\b(?:Math\.random|random\.random)\s*\(', 'Non-cryptographic random generator', 'MEDIUM', 'LOW', 'This is a security issue only when randomness protects tokens, secrets, nonces, or similar assets.'),
    ],
    'encoding_misuse': [
        (r'base64[^\n]{0,80}password|password[^\n]{0,80}base64', 'Base64 used near password handling', 'MEDIUM', 'LOW', 'Confirm whether encoding is being mistaken for encryption or secure storage.'),
    ]
}


def build_skip_dirs(extra_skip_dirs=None, include_agent_skills=False):
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    if include_agent_skills:
        skip_dirs.discard('.agents')
    for value in extra_skip_dirs or []:
        skip_dirs.add(Path(value).name)
    return skip_dirs


def scan_directory(path, categories, skip_dirs, max_file_bytes):
    results = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [name for name in dirs if name not in skip_dirs]
        for name in files:
            if not name.endswith(SCAN_SUFFIXES):
                continue
            file_path = Path(root) / name
            try:
                if file_path.stat().st_size > max_file_bytes:
                    continue
                content = file_path.read_text(errors='ignore')
                for category in categories:
                    for pattern, finding_type, severity, confidence, reason in PATTERNS[category]:
                        for match in re.finditer(pattern, content, re.IGNORECASE):
                            line_no = content[:match.start()].count('\n') + 1
                            results.append({
                                'status': 'candidate',
                                'category': category,
                                'type': finding_type,
                                'file': str(file_path),
                                'line': line_no,
                                'severity': severity,
                                'confidence': confidence,
                                'reason': reason,
                                'match': match.group(0),
                            })
            except Exception:
                continue
    return results

def main():
    parser = argparse.ArgumentParser(description='Cryptographic Security Scanner')
    parser.add_argument('--path', default='.', help='Path to scan')
    parser.add_argument('--all', action='store_true', help='Run all scans')
    parser.add_argument('--broken', action='store_true', help='Scan for broken patterns')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--exclude-dir', action='append', default=[], help='Additional directory name to skip; repeat as needed')
    parser.add_argument('--include-agent-skills', action='store_true', help='Include .agents directories, which are skipped by default')
    parser.add_argument('--max-file-bytes', type=int, default=DEFAULT_MAX_FILE_BYTES, help='Skip files larger than this size')
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        parser.error(f'Not a directory: {target}')
    if args.max_file_bytes < 1:
        parser.error('--max-file-bytes must be positive')

    categories = {'broken_algorithms'} if args.broken and not args.all else set(PATTERNS)
    skip_dirs = build_skip_dirs(args.exclude_dir, args.include_agent_skills)
    results = scan_directory(str(target), categories, skip_dirs, args.max_file_bytes)

    if args.json:
        print(json.dumps({
            'status': 'candidates_only',
            'note': 'Matches require usage-context and source-to-sink validation before reporting.',
            'results': results,
        }, indent=2))
    else:
        print(f"--- Crypto Scan Results ({len(results)} candidates) ---")
        if not results:
            print('No candidates found. This does not prove cryptographic usage is safe.')
        for r in results:
            print(f"[{r['severity']}/{r['confidence']}] candidate: {r['type']} at {r['file']}:{r['line']}")
            print(f"  Review: {r['reason']}")

if __name__ == '__main__':
    main()

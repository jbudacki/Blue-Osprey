import argparse
import ast
import json
import os
from collections import Counter
from pathlib import Path

class VibeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.total_functions = 0
        self.functions_with_types = 0
        self.functions_with_docstrings = 0
        self.classes = 0
        self.placeholders = 0

    def visit_FunctionDef(self, node):
        self.total_functions += 1
        args = [arg for arg in node.args.args if arg.arg != 'self']
        has_types = all(arg.annotation for arg in args)
        if has_types and node.returns:
            self.functions_with_types += 1
        if ast.get_docstring(node):
            self.functions_with_docstrings += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.classes += 1
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.placeholders += 1
        self.generic_visit(node)

def py_files():
    skip = {'__pycache__', '.venv', 'venv', '.git', 'node_modules'}
    files = []
    for root, dirs, names in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in names:
            if name.endswith('.py'):
                files.append(Path(root) / name)
    return files

def analyze_file(file_path):
    try:
        tree = ast.parse(file_path.read_text(encoding='utf-8'))
    except Exception:
        return None
    analyzer = VibeAnalyzer()
    analyzer.visit(tree)
    return analyzer

def collect_metrics():
    files = py_files()
    generic_names = {'utils.py', 'helpers.py', 'core.py', 'base.py', 'models.py', 'schemas.py', 'constants.py', 'config.py'}
    generic = [str(f) for f in files if f.name in generic_names]
    large = [(str(f), sum(1 for _ in f.open(errors='ignore'))) for f in files if f.exists()]
    large = [(p, n) for p, n in large if n > 500]
    totals = Counter()
    for f in files:
        res = analyze_file(f)
        if not res:
            continue
        totals['functions'] += res.total_functions
        totals['typed_functions'] += res.functions_with_types
        totals['docstring_functions'] += res.functions_with_docstrings
        totals['classes'] += res.classes
        totals['placeholder_classes'] += res.placeholders
    file_count = len(files)
    return {
        'python_files': file_count,
        'generic_files': generic,
        'large_files_over_500_lines': sorted(large, key=lambda x: x[1], reverse=True)[:20],
        'classes': totals['classes'],
        'class_to_file_ratio': round(totals['classes'] / file_count, 2) if file_count else 0,
        'placeholder_classes': totals['placeholder_classes'],
        'functions': totals['functions'],
        'type_hint_coverage_percent': round(totals['typed_functions'] / totals['functions'] * 100, 1) if totals['functions'] else 0,
        'docstring_coverage_percent': round(totals['docstring_functions'] / totals['functions'] * 100, 1) if totals['functions'] else 0,
    }

def main():
    parser = argparse.ArgumentParser(description='Vibe-Code Detection Script')
    parser.add_argument('command', choices=['generic-names', 'class-ratio', 'large-files', 'type-hints', 'docstrings', 'module-headers', 'emoji-scan', 'full-report'])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    metrics = collect_metrics()
    if args.command == 'generic-names':
        output = {'generic_files': metrics['generic_files']}
    elif args.command == 'class-ratio':
        output = {'classes': metrics['classes'], 'python_files': metrics['python_files'], 'ratio': metrics['class_to_file_ratio']}
    elif args.command == 'large-files':
        output = {'large_files_over_500_lines': metrics['large_files_over_500_lines']}
    elif args.command == 'type-hints':
        output = {'type_hint_coverage_percent': metrics['type_hint_coverage_percent'], 'functions': metrics['functions']}
    elif args.command == 'docstrings':
        output = {'docstring_coverage_percent': metrics['docstring_coverage_percent'], 'functions': metrics['functions']}
    elif args.command == 'module-headers':
        output = {'note': 'Manual review recommended: compare repetitive file headers across modules.'}
    elif args.command == 'emoji-scan':
        output = {'note': 'Manual review recommended: search for emoji in comments, docs, and logs.'}
    else:
        output = metrics

    if args.json or args.command == 'full-report':
        print(json.dumps(output, indent=2))
    else:
        for key, value in output.items():
            print(f'{key}: {value}')

if __name__ == '__main__':
    main()

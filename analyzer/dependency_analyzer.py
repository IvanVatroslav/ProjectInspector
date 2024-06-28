import ast
import os


class DependencyAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.dependencies = {}

    def visit_Import(self, node):
        for alias in node.names:
            self._add_dependency(alias.name, None)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self._add_dependency(module, alias.name)

    def visit_ClassDef(self, node):
        class_name = node.name
        self.dependencies[class_name] = {'imports': [], 'inherits': [], 'methods': []}
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.dependencies[class_name]['inherits'].append(base.id)
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                self.dependencies[class_name]['methods'].append(body_item.name)
            elif isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        self.dependencies[class_name]['imports'].append(target.id)
        self.generic_visit(node)

    def _add_dependency(self, module, name):
        if module not in self.dependencies:
            self.dependencies[module] = {'imports': [], 'inherits': [], 'methods': []}
        if name:
            self.dependencies[module]['imports'].append(name)

    def analyze_directory(self, path):
        for root, _, files in os.walk(path):
            if 'venv' in root:
                continue  # Skip the virtual environment directory
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            tree = ast.parse(f.read(), filename=file)
                            self.visit(tree)
                        except UnicodeDecodeError as e:
                            print(f"Error decoding {file_path}: {e}")
                        except SyntaxError as e:
                            print(f"Syntax error in {file_path}: {e}")
        return self.dependencies

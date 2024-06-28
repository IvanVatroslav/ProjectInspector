import json
import os
from analyzer import DependencyAnalyzer

if __name__ == "__main__":
    analyzer = DependencyAnalyzer()
    project_path = 'C:\\Users\\ivan.zeljeznjak\\DataspellProjects\\slack_bot'
    dependencies = analyzer.analyze_directory(project_path)

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'dependencies.json')
    with open(output_path, 'w') as f:
        json.dump(dependencies, f, indent=4)

    print(f"Dependencies written to {output_path}")

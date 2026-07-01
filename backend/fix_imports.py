import os

search_str = "from app.models.analytics import BehaviorSession"
replace_str = "from app.models.sessions import BehaviorSession"

for root, _, files in os.walk(r'd:\PythonProjects\AutopsyAI\backend\app'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if search_str in content:
                print(f"Replacing in {filepath}")
                content = content.replace(search_str, replace_str)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

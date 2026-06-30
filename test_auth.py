import ast
with open('src/bot/main.py', 'r') as f:
    tree = ast.parse(f.read())
print("Syntax OK")

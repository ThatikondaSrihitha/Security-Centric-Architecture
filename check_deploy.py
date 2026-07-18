import ast, os

errors = []
for f in os.listdir('page_modules'):
    if f.endswith('.py'):
        try:
            ast.parse(open(f'page_modules/{f}', encoding='utf-8').read())
        except SyntaxError as e:
            errors.append(f'page_modules/{f}: line {e.lineno}')

for f in ['app.py', 'config.py', 'requirements.txt']:
    if not os.path.exists(f):
        errors.append(f'MISSING: {f}')

if errors:
    print('ISSUES FOUND:')
    for e in errors:
        print(' ', e)
else:
    print('All files clean - ready to deploy!')

required = [
    'app.py', 'config.py', 'requirements.txt', 'runtime.txt',
    '.streamlit/config.toml', 'data/sample_ecommerce.json',
    'data/sample_banking.yaml', 'data/sample_hospital.xml',
    'data/sample_microservices.puml', 'data/sample_iot.json',
]
print('\nDeployment checklist:')
for f in required:
    status = 'OK' if os.path.exists(f) else 'MISSING'
    print(f'  [{status}] {f}')

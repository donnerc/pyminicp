
from datetime import datetime

def is_import(line: str) -> bool:
    return line.startswith('from ') or line.startswith('import ')

def collect_imports(lines: list[str]) -> list[str]:
    return [line for line in lines if is_import(line)]
    

                
imports = []
codelines = []

my_modules = [
    'exceptions',
    'domain',
    'variable',
    'constraint',
    'not_equal',
    'csp',
]

preamble = f'''
#####################################################
# Single file bundle of toycsp generated on {datetime.now()}
# Do not modify file
# Regenerate with 
#   python build_singlefile.py
#####################################################

'''


for filename in [m + '.py' for m in my_modules]:
    with open(filename, 'r') as fd:
        pysource: str = fd.read()
        pylines = pysource.split('\n')
        
        for line in pylines:
            if is_import(line):
                module = line.strip().split('from')[1].strip().split('import')[0].strip(' .')
                if module not in my_modules and line not in imports:
                    imports.append(line)
            else:
                codelines += [line]

        
imports_code = '\n'.join(imports)
code = '\n'.join(codelines)

print(preamble)
print(imports_code)
print()
print(code)
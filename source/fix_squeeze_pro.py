# fix_squeeze_pro.py
with open('/opt/render/project/src/.venv/lib/python3.11/site-packages/pandas_ta/momentum/squeeze_pro.py', 'r') as file:
    content = file.read()

# Aqui você pode modificar o conteúdo conforme necessário (exemplo: tratando NaN)
content = content.replace('NaN', 'nan')  # Modifique conforme necessário

# Escreva o conteúdo de volta para o arquivo
with open('/opt/render/project/src/.venv/lib/python3.11/site-packages/pandas_ta/momentum/squeeze_pro.py', 'w') as file:
    file.write(content)

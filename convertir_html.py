import os
import re

CSS = """
:root {
    --red-vintage: #CC3333;
    --blue-vintage: #1A3A5C;
    --yellow-vintage: #F5E6C8;
    --white-comic: #FFF8F0;
    --ink: #1A1A1A;
    --ink-faded: #5A5A5A;
    --cyan-amazon: #00B4D8;
    --green-selva: #2D6A4F;
    --gold-amanecer: #FFB703;
    --shadow-comic: 4px 4px 0 var(--ink);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--white-comic); color: var(--ink); line-height: 1.6; padding: 2rem; max-width: 1200px; margin: 0 auto; }
h1 { color: var(--blue-vintage); border-bottom: 3px solid var(--red-vintage); padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
h2 { color: var(--blue-vintage); margin: 1.5rem 0 1rem; }
h3 { color: var(--red-vintage); margin: 1rem 0 0.5rem; }
h4 { color: var(--green-selva); margin: 0.75rem 0 0.5rem; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; background: white; box-shadow: var(--shadow-comic); }
th { background: var(--blue-vintage); color: white; padding: 0.75rem; text-align: left; }
td { padding: 0.5rem 0.75rem; border-bottom: 1px solid #ddd; }
tr:hover { background: #f5f5f5; }
code { background: #f0f0f0; padding: 0.2rem 0.4rem; border-radius: 3px; font-family: 'Courier New', monospace; }
pre { background: #2d2d2d; color: #f8f8f2; padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0; }
pre code { background: transparent; padding: 0; }
ul, ol { margin: 0.5rem 0 1rem 2rem; }
li { margin: 0.25rem 0; }
strong { color: var(--red-vintage); }
hr { border: none; border-top: 2px solid var(--yellow-vintage); margin: 2rem 0; }
.header { background: linear-gradient(135deg, var(--blue-vintage) 0%, var(--green-selva) 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center; }
.header h1 { color: white; border: none; margin: 0; }
.header p { opacity: 0.9; margin-top: 0.5rem; }
.footer { text-align: center; padding: 2rem; color: var(--ink-faded); font-size: 0.9rem; border-top: 2px solid var(--yellow-vintage); margin-top: 2rem; }
"""

def md_to_html(md_content, title):
    html = md_content
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Tables
    lines = html.split('\n')
    in_table = False
    result = []
    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                result.append('<table>')
                in_table = True
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(set(c) <= set('-: ') for c in cells):
                continue
            tag = 'th' if not result or '<table>' in result[-1] else 'td'
            result.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
        else:
            if in_table:
                result.append('</table>')
                in_table = False
            result.append(line)
    if in_table:
        result.append('</table>')
    html = '\n'.join(result)
    
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html, flags=re.MULTILINE)
    
    # Paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = '<p>' + html + '</p>'
    
    # Limpiar párrafos vacíos
    html = html.replace('<p></p>', '')
    html = html.replace('<p><table>', '<table>')
    html = html.replace('</table></p>', '</table>')
    html = html.replace('<p><pre>', '<pre>')
    html = html.replace('</pre></p>', '</pre>')
    html = html.replace('<p><h1>', '<h1>')
    html = html.replace('</h1></p>', '</h1>')
    html = html.replace('<p><h2>', '<h2>')
    html = html.replace('</h2></p>', '</h2>')
    html = html.replace('<p><h3>', '<h3>')
    html = html.replace('</h3></p>', '</h3>')
    html = html.replace('<p><h4>', '<h4>')
    html = html.replace('</h4></p>', '</h4>')
    
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
<h1>{title}</h1>
<p>Soporte de beca - Octubre 2026</p>
</div>
{html}
<div class="footer">
<p>Universidad Distrital Francisco José de Caldas · Doctorado en Ingeniería</p>
<p>Camilo López · 2026</p>
</div>
</body>
</html>'''

# Convertir todos los archivos
input_dir = '/Users/milolopez/Desktop/INFORMES BECA/soportes_beca 6 pago'
output_dir = '/Users/milolopez/Desktop/INFORMES BECA/soportes_beca 6 pago_html'

os.makedirs(output_dir, exist_ok=True)

for filename in sorted(os.listdir(input_dir)):
    if filename.endswith('.md'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.md', '.html'))
        
        with open(input_path, 'r') as f:
            content = f.read()
        
        title = filename.replace('.md', '').replace('_', ' ').title()
        html_content = md_to_html(content, title)
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f'✅ {filename} -> {filename.replace(".md", ".html")}')

print(f'\nTotal: {len(os.listdir(output_dir))} archivos HTML creados')

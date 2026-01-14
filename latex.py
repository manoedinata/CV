from jinja2 import Environment
import os

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        return text  # Return numbers or None as-is
        
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def generate_latex(filename: str, env: Environment, template_dir: str, data: dict, output_dir: str | None = ""):
    if not output_dir: output_dir = template_dir
    header = env.get_template(f'{filename}.tex.j2')
    header_content = header.render(data=data)
    with open(os.path.join(output_dir, f'{filename}.tex'), 'w') as f:
        f.write(header_content)

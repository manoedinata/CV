from jinja2 import Environment
import os
import re

LATEX_REPLACEMENTS = {
    '\\': r'\textbackslash{}',
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
LATEX_PATTERN = re.compile('|'.join(re.escape(char) for char in LATEX_REPLACEMENTS))
SCHEME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')

def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        return text  # Return numbers or None as-is

    # Single pass so replacements are never escaped again
    return LATEX_PATTERN.sub(lambda match: LATEX_REPLACEMENTS[match.group()], text)

def href(url: str, text: str | None = None) -> str:
    """Render a \\href. Prepends https:// to URLs without a scheme."""
    if not SCHEME_PATTERN.match(url):
        url = f'https://{url}'
    target = url.replace('%', r'\%').replace('#', r'\#')
    return rf'\href{{{target}}}{{{escape_latex(text if text is not None else url)}}}'

def generate_latex(filename: str, env: Environment, template_dir: str, data: dict, output_dir: str | None = ""):
    if not output_dir: output_dir = template_dir
    header = env.get_template(f'{filename}.tex.j2')
    header_content = header.render(data=data)
    with open(os.path.join(output_dir, f'{filename}.tex'), 'w') as f:
        f.write(header_content)

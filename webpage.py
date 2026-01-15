import os

from jinja2 import Environment

import htmlmin

def generate_webpage(filename: str, data: dict, env: Environment, current_dir: str):
    template = env.get_template(f'{filename}.html.j2')
    output = template.render(data=data)
    output = htmlmin.minify(output, remove_empty_space=True, remove_comments=True, reduce_boolean_attributes=True)

    if filename == "resume":
        filename = "index"
    with open(os.path.join(current_dir, f'{filename}.html'), 'w') as f:
        f.write(output)

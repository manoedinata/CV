import os

from jinja2 import Environment

import htmlmin

def generate_webpage(data: dict, env: Environment, current_dir: str):
    template = env.get_template('resume.html.j2')
    output = template.render(data=data)
    output = htmlmin.minify(output, remove_empty_space=True, remove_comments=True, reduce_boolean_attributes=True)

    with open(os.path.join(current_dir, 'resume.html'), 'w') as f:
        f.write(output)

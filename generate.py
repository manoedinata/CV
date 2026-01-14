import json
import os
import shutil
import subprocess
import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader

from latex import escape_latex
from latex import generate_latex
from webpage import generate_webpage

def date_format(date_str: str) -> str:
    """Convert date from 'YYYY-MM' to 'Month YYYY' format."""
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m')
        return date_obj.strftime('%B %Y')
    except ValueError:
        return date_str  # Return as-is if format is incorrect

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
website_dir = os.path.join(current_dir, 'website')


output_dir = os.path.join(current_dir, 'output')
shutil.rmtree(output_dir) if os.path.exists(output_dir) else None
os.makedirs(output_dir)

generated_dir = os.path.join(current_dir, 'generated')
shutil.rmtree(generated_dir) if os.path.exists(generated_dir) else None
os.makedirs(generated_dir)

# Copy some original LaTeX to the generated directory
shutil.copyfile(os.path.join(template_dir, 'main.tex'), os.path.join(generated_dir, 'main.tex'))
shutil.copytree(os.path.join(template_dir, 'custom_commands'), os.path.join(generated_dir, 'custom_commands'))

# Load the JSON Data
with open('resume.json') as f:
    data = json.load(f)

# Set up the Jinja2 Environment
env = Environment(
    loader=FileSystemLoader(template_dir),
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='<<',  # Use << variable >> instead of {{ variable }} to avoid LaTeX conflicts
    variable_end_string='>>',
)

# Custom filter
env.filters['escape_tex'] = escape_latex
env.filters['date_format'] = date_format


### HEADER
generate_latex('header', env, template_dir, data, output_dir=generated_dir)

### SUMMARY
generate_latex('summary', env, template_dir, data, output_dir=generated_dir)

### EDUCATION
generate_latex('education', env, template_dir, data, output_dir=generated_dir)

### EXPERIENCE
generate_latex('experience', env, template_dir, data, output_dir=generated_dir)

### SKILLS
generate_latex('skills', env, template_dir, data, output_dir=generated_dir)

### PROJECTS
generate_latex('projects', env, template_dir, data, output_dir=generated_dir)

### ORGANIZATIONS
generate_latex('organizations', env, template_dir, data, output_dir=generated_dir)

### AWARDS
generate_latex('awards', env, template_dir, data, output_dir=generated_dir)

try:
    os.chdir(generated_dir)
    print("Compiling PDF...")

    for i in range(2):  # Run xelatex twice to ensure references are updated
        subprocess.run(["xelatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", "main.tex"], check=True)
    print("\nSuccess! main.pdf generated.")
except subprocess.CalledProcessError as e:
    print("Error during compilation. Check main.log for details.")
except FileNotFoundError:
    print("Error: xelatex not found. Make sure TeX Live or MiKTeX is installed and on your PATH.")


# Generate the Webpage
env.loader = FileSystemLoader(website_dir)
env.variable_start_string = '{{'
env.variable_end_string = '}}'
generate_webpage(data, env, output_dir)

os.chdir(output_dir)
os.remove("main.log")
os.remove("main.aux")
os.remove("main.out")

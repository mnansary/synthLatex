import random
import os
import json
import argparse

def escape_latex(text):
    """Escape LaTeX special characters in text."""
    replacements = {
        '&': r'\\&', '%': r'\\%', '$': r'\\$', '#': r'\\#', '_': r'\\_',
        '{': r'\\{', '}': r'\\}', '~': r'\\textasciitilde{}', '^': r'\\textasciicircum{}',
        '\\': r'\\textbackslash{}'
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text


def load_entries(json_path):
    """Load entries from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def entries_to_latex_table(entries):
    """Convert JSON entries to a LaTeX tabular environment."""
    lines = []
    lines.append(r"\begin{tabular}{|p{4cm}|p{6cm}|p{3cm}|}")
    lines.append(r"\hline")
    lines.append(r"\textbf{User Query} & \textbf{Response} & \textbf{Intent} \\")
    lines.append(r"\hline")

    users = entries.get('user', [])
    responses = entries.get('response', [])
    intents = entries.get('intents', [])

    for u, r, i in zip(users, responses, intents):
        lines.append(r"{0} & {1} & {2} \\".format(
            escape_latex(u), escape_latex(r), escape_latex(i)
        ))
        lines.append(r"\hline")

    lines.append(r"\end{tabular}")
    return '\n'.join(lines)


def generate_template_with_json(output_path, json_path):
    """Generate a LaTeX file embedding a table from JSON data."""
    entries = load_entries(json_path)
    table = entries_to_latex_table(entries)

    content = f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{array}}
\\usepackage{{booktabs}}

\\begin{{document}}
\\section*{{Data Table from JSON}}
{table}

\\end{{document}}
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX template from JSON data.")
    parser.add_argument("output_path", help="Path to output .tex file")
    parser.add_argument("json_path", help="Path to input JSON file (e.g., 1_xxx.json)")
    args = parser.parse_args()

    generate_template_with_json(args.output_path, args.json_path)
    print(f"Successfully generated LaTeX file at {args.output_path}")

if __name__ == "__main__":
    main()


    # python generate_tex.py ../output/temp.tex ../deliverables/D2/BanConvComm/1_xxx.json
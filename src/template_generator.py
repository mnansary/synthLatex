import random
import argparse
import os
import json
from tqdm import tqdm

def load_texts_from(dir_path):
    texts = []
    for fname in os.listdir(dir_path):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(dir_path, fname)
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
        # type-2 file: has "text"
        if "text" in obj:
            texts.append(obj["text"])
        # type-1 file: has lists of user/responses
        else:
            texts.extend(obj.get("response", []))
            # if you also want questions:
            # texts.extend(obj.get("user", []))
    return texts

def apply_text_style(text_placeholder):
    """Apply random text styles 50% of the time; otherwise, return plain text."""
    if random.random() < 0.5:  # 50% chance for plain text
        return text_placeholder
    styles = [
        r"\textbf{{{}}}".format(text_placeholder),  # Bold
        r"\textit{{{}}}".format(text_placeholder),  # Italic
        r"\underline{{{}}}".format(text_placeholder),  # Underline
        r"\texttt{{{}}}".format(text_placeholder),  # Typewriter
        r"\textsc{{{}}}".format(text_placeholder),  # Small caps
        r"Prefix-{{{}}}-Suffix".format(text_placeholder),  # Prefix and suffix
        r"\textbf{{\textit{{{}}}}}".format(text_placeholder),  # Bold italic (fixed)
        r"{{{}}} superscript^{{sup}}".format(text_placeholder),  # Superscript
        r"{{{}}} subscript_{{sub}}".format(text_placeholder),  # Subscript
    ]
    return random.choice(styles)

def generate_random_template(output_path, text_pool):
    """Generate a random LaTeX template with at least 50 structures and 30 base templates."""
    structures = [
    # 1-3: Headings
    r"\section{{{}}}".format(apply_text_style(random.choice(text_pool))),
    r"\subsection{{{}}}".format(apply_text_style(random.choice(text_pool))),
    r"\subsubsection{{{}}}".format(apply_text_style(random.choice(text_pool))),

    # 4-8: Lists
    r"\begin{{itemize}}\n    \item {{{}}}\n    \item {{{}}}\n\end{{itemize}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{enumerate}}\n    \item {{{}}}\n    \item {{{}}}\n\end{{enumerate}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{description}}\n    \item[{{{}}}] {{{}}}\n\end{{description}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{itemize}}\n    \item {{{}}}\n    \begin{{enumerate}}\n        \item {{{}}}\n    \end{{enumerate}}\n\end{{itemize}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{enumerate}}\n    \item {{{}}}\n    \begin{{itemize}}\n        \item {{{}}}\n    \end{{itemize}}\n\end{{enumerate}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),

    # 9-15: Tables
    r"\begin{{tabular}}{{|c|c|}}\n\hline\n    {{{}}} & {{{}}} \\\\\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{tabular}}{{||l|r||}}\n\hline\n    {{{}}} & {{{}}} \\\\\n    {{{}}} & {{{}}} \\\\\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{tabular}}{{|c|c|c|}}\n\hline\n    {{{}}} & {{{}}} & {{{}}} \\\\\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{table}}[h]\n\centering\n    \begin{{tabular}}{{|c|c|}}\n    \hline\n        {{{}}} & {{{}}} \\\\\n    \hline\n    \end{{tabular}}\n    \caption{{{}}}\n\end{{table}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{table}}[h]\n\centering\n    \begin{{tabular}}{{|c|c|c|}}\n    \hline\n        \multicolumn{{2}}{{|c|}}{{{}}} & {{{}}} \\\\\n    \hline\n        {{{}}} & {{{}}} & {{{}}} \\\\\n    \hline\n    \end{{tabular}}\n\end{{table}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{tabular}}{{|c|c|c|}}\n\hline\n    \multirow{{2}}{{*}}{{{}}} & {{{}}} & {{{}}} \\\\\n    \cline{{2-3}}\n     & {{{}}} & {{{}}} \\\\\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{tabular}}{{|l|c|r|}}\n\hline\n    {{{}}} & \multicolumn{{2}}{{|c|}}{{{}}} \\\\\n\hline\n    {{{}}} & {{{}}} & {{{}}} \\\\\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),

    # 16-22: Equations
    r"Equation: ${{{}}}$".format(apply_text_style(random.choice(text_pool))),
    r"Equation: $\frac{{{}}}{{{}}}$".format(apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))),
    r"Equation: ${{}} = {{}}$".format(apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))),
    r"\begin{{equation}}\n    {{{}}} = {{{}}}^2\n\end{{equation}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{equation}}\n    \sqrt{{{}}} = {{{}}}\n\end{{equation}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{align}}\n    {{{}}} &= {{{}}} \\\\\n    {{{}}} &= {{{}}}\n\end{{align}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{align*}}\n    {{{}}} + {{{}}} &= {{{}}} \\\\\n    {{{}}} &= \int {{{}}} \,dx\n\end{{align*}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)),
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),

    # 23-27: Multi-column layouts
    r"\begin{{multicols}}{{2}}\n    {{{}}}\n    \columnbreak\n    {{{}}}\n\end{{multicols}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{multicols}}{{3}}\n    {{{}}}\n    \columnbreak\n    {{{}}}\n    \columnbreak\n    {{{}}}\n\end{{multicols}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{multicols}}{{2}}\n    {{{}}}\n    \begin{{itemize}}\n        \item {{{}}}\n    \end{{itemize}}\n    \columnbreak\n    {{{}}}\n\end{{multicols}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{multicols}}{{2}}\n    {{{}}}\n    \begin{{tabular}}{{|c|}}\n    \hline\n        {{{}}}\n    \hline\n    \end{{tabular}}\n    \columnbreak\n    {{{}}}\n\end{{multicols}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{multicols}}{{3}}\n    {{{}}}\n    \columnbreak\n    {{{}}}\n    \begin{{equation}}\n        {{{}}}\n    \end{{equation}}\n    \columnbreak\n    {{{}}}\n\end{{multicols}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),

    # 28-35: Nested structures
    r"\section{{{}}}\n    {{{}}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\section{{{}}}\n    \begin{{itemize}}\n        \item {{{}}}\n    \end{{itemize}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\subsection{{{}}}\n    \begin{{tabular}}{{|c|c|}}\n    \hline\n        {{{}}} & {{{}}} \\\\\n    \hline\n    \end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{center}}\n    {{{}}}\n    \begin{{equation}}\n        {{{}}} = {{{}}}\n    \end{{equation}}\n\end{{center}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{itemize}}\n    \item {{{}}}\n    \begin{{align}}\n        {{{}}} &= {{{}}}\n    \end{{align}}\n\end{{itemize}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{tabular}}{{|c|}}\n\hline\n    {{{}}}\n    \begin{{itemize}}\n        \item {{{}}}\n    \end{{itemize}}\n\hline\n\end{{tabular}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\section{{{}}}\n\begin{{center}}\n    {{{}}}\n\end{{center}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{description}}\n    \item[{{{}}}] {{{}}}\n    \begin{{equation}}\n        {{{}}}\n    \end{{equation}}\n\end{{description}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),

    # 36-40: Figures and boxes
    r"\begin{{figure}}[h]\n\centering\n    \fbox{{{}}}\n    \caption{{{}}}\n\end{{figure}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{figure}}[h]\n\centering\n    {{{}}}\n    \caption{{{}}}\n\end{{figure}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\fbox{{{}}}".format(apply_text_style(random.choice(text_pool))),
    r"\framebox{{{}}}\n{{{}}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{center}}\n    \fbox{{{}}}\n\end{{center}}".format(apply_text_style(random.choice(text_pool))),

    # 41-45: Theorem-like environments
    r"\begin{{theorem}}\n    {{{}}}\n\end{{theorem}}".format(apply_text_style(random.choice(text_pool))),
    r"\begin{{proof}}\n    {{{}}}\n\end{{proof}}".format(apply_text_style(random.choice(text_pool))),
    r"\begin{{theorem}}\n    {{{}}}\n    \begin{{proof}}\n        {{{}}}\n    \end{{proof}}\n\end{{theorem}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{lemma}}\n    {{{}}}\n\end{{lemma}}".format(apply_text_style(random.choice(text_pool))),
    r"\begin{{proposition}}\n    {{{}}}\n\end{{proposition}}".format(apply_text_style(random.choice(text_pool))),

    # 46-50: Miscellaneous
    r"\textbf{{{}}}\n{{{}}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\textit{{{}}}\n\begin{{center}}\n    {{{}}}\n\end{{center}}".format(
        apply_text_style(random.choice(text_pool)), apply_text_style(random.choice(text_pool))
    ),
    r"\begin{{flushleft}}\n    {{{}}}\n\end{{flushleft}}".format(apply_text_style(random.choice(text_pool))),
    r"\begin{{flushright}}\n    {{{}}}\n\end{{flushright}}".format(apply_text_style(random.choice(text_pool))),
    r"\begin{{quote}}\n    {{{}}}\n\end{{quote}}".format(apply_text_style(random.choice(text_pool)))
    ]

    # Verify we have at least 50 structures
    assert len(structures) >= 50, f"Only {len(structures)} structures defined, need at least 50"

    # Randomly choose number of sections (1 to 7 for variety)
    num_sections = random.randint(1, 7)
    content = "\n\n".join(random.choices(structures, k=num_sections))

    # 30 distinct base templates
    base_templates = [
        # 1: Basic article
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 2: Article with math and theorems
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{amsmath, amssymb, amsthm}}
    \usepackage{{multirow}}
    \newtheorem{{theorem}}{{Theorem}}
    \newtheorem{{proof}}{{Proof}}
    \newtheorem{{lemma}}{{Lemma}}
    \newtheorem{{proposition}}{{Proposition}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 3: Multi-column article
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{multicol}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 4: Report with title page
        r"""
    \documentclass{{report}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \title{{{}}}
    \author{{{}}}
    \date{{{}}}
    \maketitle
    """.format(
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool))
        ) + content + r"""
    \end{{document}}
    """,

        # 5: Book with chapter
        r"""
    \documentclass{{book}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \chapter{{{}}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 6: Article with fancy headers
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{fancyhdr}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \pagestyle{{fancy}}
    \fancyhead[L]{{{}}}
    \fancyhead[R]{{{}}}
    \begin{{document}}
    """.format(
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool))
        ) + content + r"""
    \end{{document}}
    """,

        # 7: Two-column article
        r"""
    \documentclass[twocolumn]{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 8: Article with colored text
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{xcolor}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \color{{blue}}
    """ + content + r"""
    \end{{document}}
    """,

        # 9: Report with table of contents
        r"""
    \documentclass{{report}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \tableofcontents
    \newpage
    """ + content + r"""
    \end{{document}}
    """,

        # 10: Book with front matter
        r"""
    \documentclass{{book}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \frontmatter
    \title{{{}}}
    \maketitle
    \mainmatter
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 11: Article with bibliography
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \begin{{thebibliography}}{{9}}
    \bibitem{{{}}} {{{}}}
    \end{{thebibliography}}
    \end{{document}}
    """.format(
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool))
        ),

        # 12: Minimal class
        r"""
    \documentclass{{minimal}}
    \usepackage[utf8]{{inputenc}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 13: Letter class
        r"""
    \documentclass{{letter}}
    \usepackage[utf8]{{inputenc}}
    \begin{{document}}
    \signature{{{}}}
    \address{{{}}}
    \begin{{letter}}{{{}}}
    \opening{{{}}}
    """.format(
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool))
        ) + content + r"""
    \closing{{{}}}
    \end{{letter}}
    \end{{document}}
    """.format(apply_text_style(random.choice(text_pool))),

        # 14: Article with boxed title
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \fbox{{\textbf{{{}}}}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 15: Article with custom margins
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper, margin=0.5in}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 16: Article with landscape orientation
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage[landscape]{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 17: Memoir class with chapter
        r"""
    \documentclass{{memoir}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \chapter{{{}}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 18: Article with header and footer
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{fancyhdr}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \pagestyle{{fancy}}
    \fancyhead[C]{{{}}}
    \fancyfoot[C]{{{}}}
    \begin{{document}}
    """.format(
            apply_text_style(random.choice(text_pool)),
            apply_text_style(random.choice(text_pool))
        ) + content + r"""
    \end{{document}}
    """,

        # 19: Poster-like article
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a0paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 20: Article with watermark
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{draftwatermark}}
    \SetWatermarkText{{{}}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 21: Article with custom font size
        r"""
    \documentclass[12pt]{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 22: Beamer slide (presentation)
        r"""
    \documentclass{{beamer}}
    \usepackage[utf8]{{inputenc}}
    \begin{{document}}
    \begin{{frame}}
    \frametitle{{{}}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{frame}}
    \end{{document}}
    """,

        # 23: Article with abstract
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \begin{{abstract}}
    {{{}}}
    \end{{abstract}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 24: Article with custom section numbering
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \renewcommand{{\thesection}}{{\Roman{{section}}}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 25: Article with boxed content
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{boxedminipage}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \begin{{boxedminipage}}{{\textwidth}}
    """ + content + r"""
    \end{{boxedminipage}}
    \end{{document}}
    """,

        # 26: Article with rotated text
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{rotating}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    \begin{{sideways}}
    {{{}}}
    \end{{sideways}}
    """.format(apply_text_style(random.choice(text_pool))) + content + r"""
    \end{{document}}
    """,

        # 27: Article with custom line spacing
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{setspace}}
    \doublespacing
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 28: Article with background color
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{xcolor}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \pagecolor{{lightgray}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 29: Article with custom page numbering
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \pagenumbering{{roman}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \end{{document}}
    """,

        # 30: Article with appendix
        r"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{geometry}}
    \geometry{{a4paper}}
    \begin{{document}}
    """ + content + r"""
    \appendix
    \section{{{}}}
    \end{{document}}
    """.format(apply_text_style(random.choice(text_pool)))
    ]


    # Verify we have at least 30 base templates
    assert len(base_templates) >= 30, f"Only {len(base_templates)} base templates defined, need at least 30"

    # Choose a random base template
    template = random.choice(base_templates)

    # Write the template to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)

def main():
    parser = argparse.ArgumentParser(description="Generate random LaTeX templates.")
    parser.add_argument("--input-dir",
                        default="../deliverables/D2/BanConvComm/",
                        help="Where to read your JSONs from")
    parser.add_argument("--output-dir",
                        default=".",
                        help="Where to write .tex files")
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="How many templates to generate")
    args = parser.parse_args()

    pool = load_texts_from(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    for i in range(1, args.count + 1):
        out = os.path.join(args.output_dir, f"template_{i}.tex")
        generate_random_template(out, pool)

if __name__ == "__main__":
    main()

''' 
python template_generator.py --input-dir ../deliverables/D2/BanConvComm/ --output-dir ../output/ --count 5

'''
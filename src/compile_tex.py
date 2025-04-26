# compile_tex.py (fixed)
import subprocess
import os
import shutil
import sys

def compile_latex_to_pdf(tex_file, output_pdf="output.pdf"):
    """Compile LaTeX to PDF with comprehensive error handling"""
    try:
        tex_file = os.path.abspath(tex_file)
        output_dir = os.path.dirname(tex_file)
        base_name = os.path.splitext(os.path.basename(tex_file))[0]
        generated_pdf = os.path.join(output_dir, f"{base_name}.pdf")
        output_pdf = os.path.abspath(output_pdf)

        if not os.path.exists(tex_file):
            print(f"Error: Input file {tex_file} not found!")
            return False

        compile_cmd = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory", output_dir,
            tex_file
        ]

        for run in (1, 2):
            result = subprocess.run(
                compile_cmd,
                cwd=output_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0 and not os.path.exists(generated_pdf):
                print(f"\nCompilation errors (run {run}):")
                print("="*60)
                print(result.stderr or result.stdout or "Unknown error")
                print("="*60)

                log_file = os.path.join(output_dir, f"{base_name}.log")
                if os.path.exists(log_file):
                    print(f"\nLast 20 lines of {log_file}:")
                    print("-"*60)
                    with open(log_file, "r") as f:
                        lines = f.readlines()[-20:]
                        print("".join(lines))
                    print("-"*60)
                return False

        if not os.path.exists(generated_pdf):
            print("Error: PDF generation failed - no output file created")
            return False

        shutil.move(generated_pdf, output_pdf)
        print(f"\nSuccessfully created: {output_pdf}")

        for ext in (".aux", ".log", ".out", ".toc", ".lof", ".lot"):  
            aux_file = os.path.join(output_dir, f"{base_name}{ext}")
            if os.path.exists(aux_file):
                os.remove(aux_file)

        return True

    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution like TeX Live or MiKTeX.")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False


def main():
    if len(sys.argv) > 1:
        input_tex = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else "output.pdf"
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_tex = os.path.join(base_dir, "../output", "temp.tex")
        output_pdf = os.path.join(base_dir, "../output", "output.pdf")

    success = compile_latex_to_pdf(input_tex, output_pdf)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

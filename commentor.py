import os
import tkinter as tk
from tkinter import ttk, filedialog
from dotenv import load_dotenv
import openai
import re
from fpdf import FPDF

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

variable_declaration_pattern = r"^\s*(var|let|const)\s+\w+\s*(=.*?;)?$"  # Pattern for variable declarations

def is_variable_declaration(code_line):
    return re.match(variable_declaration_pattern, code_line)


def preprocess_code_block(code_block):
    # Remove comments and excess whitespace
    code_block = re.sub(r'\/\/.*?$', '', code_block, flags=re.MULTILINE)
    code_block = code_block.strip()

    return code_block


def generate_comment(code_block, complexity):
    prompt = f"This code block:\n\n{code_block}\n\nThe comment is:"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Using the "gpt-3.5-turbo-instruct" engine
            prompt=prompt,
            max_tokens=500,  # Increased max_tokens for longer and more detailed comments
            n=1,
            stop=None,
            temperature=0.7,  # Adjusted temperature for more diverse responses
            api_key=api_key
        )
        comment = response.choices[0].text.strip()
        return comment
    except openai.error.OpenAIError as e:
        print(f"Error generating comment: {e}")
        return None


def generate_answer(question, code_block):
    prompt = f"The code block below is provided:\n\n{code_block}\n\nThe question is:\n\n{question}\n\nThe answer is:"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Using the "gpt-3.5-turbo-instruct" engine
            prompt=prompt,
            max_tokens=200,  # Limiting max tokens for shorter answers
            n=1,
            stop=None,
            temperature=0.7,  # Adjusted temperature for more diverse responses
            api_key=api_key
        )
        answer = response.choices[0].text.strip()
        return answer
    except openai.error.OpenAIError as e:
        print(f"Error generating answer: {e}")
        return None


def generate_analysis_report(code_block):
    prompt = f"The code block below is provided:\n\n{code_block}\n\nGenerate analysis report and suggestions:"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Using the "text-davinci-002" engine for code analysis
            prompt=prompt,
            max_tokens=1000,  # Increased max_tokens for detailed analysis
            n=1,
            stop=None,
            temperature=0.7,  # Adjusted temperature for diverse responses
            api_key=api_key
        )
        report = response.choices[0].text.strip()
        return report
    except openai.error.OpenAIError as e:
        print(f"Error generating analysis report: {e}")
        return None


def generate_documentation(code_lines, complexity, question):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)


    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Code Documentation", ln=True, align="C")
    pdf.ln(10)

  
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Question", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", style="", size=12)
    pdf.multi_cell(0, 10, question, 0, 'L')
    pdf.ln(10)

   
    for i, line in enumerate(code_lines):
        comment = generate_comment(line, complexity)
        if i % 3 == 0:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 10, f"Code Block {i//3 + 1}", ln=True)
            pdf.ln(5)
        pdf.set_font("Arial", style="", size=12)
        pdf.multi_cell(0, 10, f"Line {i+1}: {line.strip()}", 0, 'L')
        pdf.set_font("Arial", style="I", size=12)
        pdf.multi_cell(0, 10, f"Comment: {comment}", 0, 'L')
        pdf.ln(5)

    
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Answer", ln=True)
    pdf.ln(5)
    answer = generate_answer(question, '\n'.join(code_lines))
    pdf.set_font("Arial", style="", size=12)
    pdf.multi_cell(0, 10, answer, 0, 'L')

    pdf_output_file = 'code_documentation.pdf'
    pdf.output(pdf_output_file)
    print(f"Professional code documentation generated and saved in {pdf_output_file}.")


def generate_code_analysis(code_lines):
    analysis_report = generate_analysis_report('\n'.join(code_lines))
    if analysis_report:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)


        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, "Code Analysis Report", ln=True, align="C")
        pdf.ln(10)


        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, analysis_report, 0, 'L')

        pdf_output_file = 'code_analysis_report.pdf'
        pdf.output(pdf_output_file)
        print(f"Code analysis report generated and saved in {pdf_output_file}.")
    else:
        print("Failed to generate code analysis report.")


def comment_file(file_path, complexity):
    with open(file_path, "r") as f:
        code_lines = f.readlines()

    commented_lines = []
    for i, line in enumerate(code_lines):
        if not is_variable_declaration(line):
            comment = generate_comment(line, complexity)
            if comment:
                commented_lines.append(f"/* {comment} */\n{line}\n\n")
        else:
            commented_lines.append(line + '\n\n')  # Retain variable declarations as-is

    output_file = 'output.js'
    with open(output_file, "w") as f:
        f.writelines(commented_lines)
    print(f"Comments generated and saved in {output_file}.")

# GUI functions
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    file_path_var.set(file_path)

def generate():
    complexity = complexity_var.get().lower()
    question = question_var.get()
    file_path = file_path_var.get()

    if not file_path:
        print("Please upload a file.")
        return

    if choice_var.get() == 1:
        with open(file_path, "r") as f:
            code_lines = f.readlines()
        generate_documentation(code_lines, complexity, question)
    elif choice_var.get() == 2:
        comment_file(file_path, complexity)
    else:
        with open(file_path, "r") as f:
            code_lines = f.readlines()
        generate_code_analysis(code_lines)


root = tk.Tk()
root.title("Code Documentation Generator **For Fun :) **")
root.geometry("700x500")

options_frame = ttk.Frame(root, padding="20")
options_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

complexity_label = ttk.Label(options_frame, text="Select complexity level of comments:")
complexity_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
complexity_var = tk.StringVar()
complexity_combo = ttk.Combobox(options_frame, textvariable=complexity_var, values=["Simple", "Complex"])
complexity_combo.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
complexity_combo.current(0)

choice_label = ttk.Label(options_frame, text="Select option:")
choice_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
choice_var = tk.IntVar()
choice_radio1 = ttk.Radiobutton(options_frame, text="Generate PDF documentation", variable=choice_var, value=1)
choice_radio1.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
choice_radio2 = ttk.Radiobutton(options_frame, text="Generate commented code file", variable=choice_var, value=2)
choice_radio2.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
choice_radio3 = ttk.Radiobutton(options_frame, text="Generate code analysis report", variable=choice_var, value=3)
choice_radio3.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
choice_radio1.invoke()  # Default select

question_label = ttk.Label(root, text="Enter your question about the code:")
question_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
question_var = tk.StringVar()
question_entry = ttk.Entry(root, textvariable=question_var, width=40)
question_entry.grid(column=0, row=2, sticky=(tk.W, tk.E), padx=5, pady=5)

file_frame = ttk.Frame(root, padding="20")
file_frame.grid(column=0, row=3, sticky=(tk.W, tk.E, tk.N, tk.S))

upload_button = ttk.Button(file_frame, text="Upload File", command=upload_file)
upload_button.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
file_path_var = tk.StringVar()
file_path_entry = ttk.Entry(file_frame, textvariable=file_path_var, width=40)
file_path_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)

generate_button = ttk.Button(root, text="Generate", command=generate)
generate_button.grid(column=0, row=4, sticky=tk.E, padx=5, pady=5)

root.mainloop()

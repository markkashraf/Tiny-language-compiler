from tkinter import *
from tkinter import filedialog, messagebox

import os
from Code.Scanner import Scanner
from Code.Parser import Parser
from Code import Util

dirpath = os.getcwd()
os.environ["PATH"] += os.pathsep + dirpath + os.pathsep + 'Graphviz\\bin'

root = Tk()

root.title('Tiny Language Compiler')

file_frame = LabelFrame(root, text="Open your file:", padx=20, pady=25)
file_frame.grid(row=0, column=0)

file_field = Text(file_frame, width=60, height=20)
file_field.insert(END, "Please Load File")
file_field.grid(row=0, column=0, columnspan=10, pady=10)

filepath = StringVar


def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Select A File", filetypes=(("text files", "*.txt"),))
    if filepath:
        global file_opened
        file_opened = True
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()
            file_field.delete("1.0", END)
            file_field.insert(END, file_content)
        scan_button.config(state="normal")
        parse_button.config(state="normal")
    else:
        messagebox.showerror("Error", "Please choose a valid file!!")


file_opened = False

file_button = Button(file_frame, text="Open File", command=open_file, width=68)
file_button.grid(row=1, column=0)

options_frame = LabelFrame(root, text="OPTIONS:", padx=20, pady=20)
options_frame.grid(row=0, column=1)

output_text = Text(options_frame, width=60, height=20)
output_text.insert(END, "Output")
output_text.config(state="disabled")
output_text.grid(row=0, column=0, columnspan=3, pady=5)


def scan():
    global filepath
    obj = Scanner()
    obj.tokenize(filepath)
    obj.export()
    f = open("output.txt", "r", encoding='utf-8').read()
    output_text.config(state="normal")
    output_text.delete("1.0", END)
    output_text.insert(END, f)
    output_text.config(state="disabled")


scan_button = Button(options_frame, text="SCAN", pady=10, padx=20, width=27, command=scan)
scan_button.config(state="disabled")
scan_button.grid(row=7, column=0, padx=4)


def parse():
    # scanning
    global filepath
    obj = Scanner()
    tokens = obj.tokenize(filepath)
    obj.export()
    f = open("output.txt", "r", encoding='utf-8').read()
    output_text.config(state="normal")
    output_text.delete("1.0", END)
    output_text.insert(END, f)
    output_text.config(state="disabled")
    # parsing
    pr_obj = Parser()
    pr_obj.tokens = tokens
    pr_obj.program()
    Util.generate_Parse_Tree(pr_obj.Nodes, pr_obj.tokens)


parse_button = Button(options_frame, text="PARSE", pady=10, padx=20, width=27, command=parse)
parse_button.config(state="disabled")
parse_button.grid(row=7, column=1, padx=4)

root.mainloop()



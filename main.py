from tkinter import *
from tkinter import filedialog, messagebox

import os
from Code.Scanner import Scanner
from Code.Parser import Parser
from Code import Util

dirpath = os.getcwd()
os.environ["PATH"] += os.pathsep + dirpath + os.pathsep + 'Graphviz\\bin'

status = False
root = Tk()
root.resizable(False,False)
root.title('Tiny Language Compiler')
root.config(bg="#fed9b7")

file_frame = LabelFrame(root, text="Open your file:", padx=20, pady=25, bg="#fed9b7")
file_frame.grid(row=0, column=0)

file_field = Text(file_frame, width=60, height=20, bg="#fdfcdc")
file_field.insert(END, "Please Load File")
file_field.config(state="disabled")
file_field.grid(row=0, column=0, columnspan=10, pady=10)

filepath = StringVar
file_opened = False

def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Select A Text File")
    if filepath:
        if not filepath.split('.')[1] == "txt":
            messagebox.showerror("File Type Error", "Please choose a Text file!!")
        else:
            global file_opened
            file_opened = True
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()
                file_field.config(state="normal")
                file_field.delete("1.0", END)
                file_field.insert(END, file_content)
                file_field.config(state="disabled")

    else:
        messagebox.showerror("File Error", "Please choose a file!!")

file_button = Button(file_frame, text="Open File", command=open_file, width=68, bg="#f07167")
file_button.grid(row=1, column=0)

options_frame = LabelFrame(root, text="OPTIONS:", padx=20, pady=20, bg="#fed9b7")
options_frame.grid(row=0, column=1)

output_text = Text(options_frame, width=60, height=20, bg="#fdfcdc")
#output_text.insert(END, "Output")
output_text.config(state="disabled")
output_text.grid(row=1, column=0, columnspan=3, pady=5)

label1 = Label(options_frame,text="Tokens",bg="#fed9b7")
label1.grid(row=0, column=0, columnspan=3, pady=0)
def scan():
    global filepath

    if not file_opened:
        messagebox.showerror("File Error", "Please choose a file!!")
    else:
        obj = Scanner()
        obj.tokenize(filepath)
        obj.export()
        f = open("Tokens.txt", "r", encoding='utf-8').read()
        output_text.config(state="normal")
        output_text.delete("1.0", END)
        output_text.insert(END, f)
        output_text.config(state="disabled")


scan_button = Button(options_frame, text="SCAN", pady=10, padx=20, width=27, bg="#0081a7", fg="#90e0ef", command=scan)

scan_button.grid(row=7, column=0, padx=4)


def parse():
    global status
    # scanning
    global filepath
    if not file_opened:
        messagebox.showerror("File Error", "Please choose a file!!")
    else:
        obj = Scanner()
        tokens = obj.tokenize(filepath)
        obj.export()
        f = open("Tokens.txt", "r", encoding='utf-8').read()
        output_text.config(state="normal")
        output_text.delete("1.0", END)
        output_text.insert(END, f)
        output_text.config(state="disabled")
        # parsing
        pr_obj = Parser()
        pr_obj.tokens = tokens
        try:
            pr_obj.program()
        except ValueError as v:
            messagebox.showerror("Error", "Syntax error\n"
                                      "This code is not accepted by Tiny language")
        else:
            Util.generate_Parse_Tree(pr_obj.Nodes)


parse_button = Button(options_frame, text="PARSE", pady=10, padx=20, width=27, bg="#0081a7", fg="#90e0ef",
                      command=parse)
parse_button.grid(row=7, column=1, padx=4)

root.mainloop()

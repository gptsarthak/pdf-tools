import os
import re
from pdfrw import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog

def browse_main_path():
    main_path = filedialog.askdirectory() + '\\'
    main_path_entry.delete(0, tk.END)
    main_path_entry.insert(0, main_path)

def browse_sup_path():
    sup_path = filedialog.askdirectory() + '\\'
    sup_path_entry.delete(0, tk.END)
    sup_path_entry.insert(0, sup_path)

def browse_file_dest():
    file_dest = filedialog.askdirectory() + '\\'
    file_dest_entry.delete(0, tk.END)
    file_dest_entry.insert(0, file_dest)

def merge_pdfs():
    main_path = main_path_entry.get()
    sup_path = sup_path_entry.get()
    file_dest = file_dest_entry.get()

    main_prefix = os.path.commonprefix([file for file in os.listdir(main_path) if file.endswith(".pdf")])
    sup_prefix = os.path.commonprefix([file for file in os.listdir(sup_path) if file.endswith(".pdf")])

    if main_prefix.find("-HIN-") == -1:
        result_label.config(text="Error: Extra file / No file in Main Folder")
    elif sup_prefix.find("-HIN-") == -1:
        result_label.config(text="Error: Extra file / No file in Supplementary Folder")
    elif re.search(r'S24-(\d+)-', main_prefix).group(1) != re.search(r'S24-(\d+)-', sup_prefix).group(1):
        result_label.config(text="Error: Account number mismatch")
    else:
        output = ""
        main_files = [file for file in os.listdir(main_path) if file.startswith(main_prefix) and file.endswith(".pdf")]
        sup_files = [file for file in os.listdir(sup_path) if file.startswith(sup_prefix) and file.endswith(".pdf")]

        def sort_key(filename):
            match = re.search(r'HIN-(\d+)\.pdf$', filename)
            if match:
                return int(match.group(1))
            return 0

        main_files.sort(key=sort_key)
        sup_files.sort(key=sort_key)

        for main_pdf in main_files:
            merger = PdfWriter()
            found = False
            for sup_pdf in sup_files:
                if int(main_pdf.split("-HIN-")[-1].split(".pdf")[0]) != int(sup_pdf.split("-HIN-")[-1].split(".pdf")[0]):
                    continue
                else:
                    found = True
                    merger.addpages(PdfReader(main_path + main_pdf).pages)
                    merger.addpages(PdfReader(sup_path + sup_pdf).pages)
                    break
            if not found:
                output += "Error: Supplementary not found for " + main_pdf + "\n"
                result_label.config(text=output)
            else:
                merged_pdf = main_pdf.split(".pdf")[0] + "-M" + ".pdf"
                merger.write(file_dest + merged_pdf)

        output += "PDFs merged successfully!" + "\n"
        result_label.config(text=output)

# Create a GUI window
root = tk.Tk()
root.title("PDF Merger")
root.geometry("600x300")

# Create input fields and labels
main_path_label = tk.Label(root, text="Main Path:")
sup_path_label = tk.Label(root, text="Supplementary Path:")
file_dest_label = tk.Label(root, text="File Destination:")

main_path_entry = tk.Entry(root, width = 50)
sup_path_entry = tk.Entry(root, width = 50)
file_dest_entry = tk.Entry(root, width = 50)

browse_main_button = tk.Button(root, text="Browse", command=browse_main_path)
browse_sup_button = tk.Button(root, text="Browse", command=browse_sup_path)
browse_dest_button = tk.Button(root, text="Browse", command=browse_file_dest)

merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs)

result_label = tk.Label(root, text="")

# Arrange widgets using the grid layout manager
main_path_label.grid(row=0, column=0, padx=20, pady=10)
main_path_entry.grid(row=0, column=1, padx=20, pady=10)
browse_main_button.grid(row=0, column=2, padx=20, pady=10)

sup_path_label.grid(row=1, column=0, padx=20, pady=10)
sup_path_entry.grid(row=1, column=1, padx=20, pady=10)
browse_sup_button.grid(row=1, column=2, padx=20, pady=10)

file_dest_label.grid(row=2, column=0, padx=20, pady=10)
file_dest_entry.grid(row=2, column=1, padx=20, pady=10)
browse_dest_button.grid(row=2, column=2, padx=20, pady=10)

merge_button.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

result_label.grid(row=4, column=0, columnspan=3, padx=20, pady=10)

root.mainloop()
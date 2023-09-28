import os
import zipfile
import html2text
import tkinter as tk
import re
from tkinter import filedialog, StringVar, IntVar, ttk, messagebox

def convert_html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown_content = converter.handle(html_content)
    return markdown_content

def is_comment_file(markdown_content, max_lines=20):
    lines = markdown_content.split('\n')
    
    # Checking for absence of H2 to H5 headers
    has_headers = any(line.startswith(('## ', '### ', '#### ', '##### ')) for line in lines)
    
    # Checking if the total number of lines is within the limit
    is_short = len(lines) <= max_lines
    
    # If the content doesn't have headers and is short, it's likely a comment
    return not has_headers and is_short

def process_zip_file(zip_path, extract_path, remove_date, replace_hyphens, skip_comments):
    cache_dir = os.path.join(extract_path, 'cache')
    os.makedirs(cache_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(cache_dir)

    posts_dir = os.path.join(cache_dir, 'posts')
    html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]

    converted_files_count = 0  # Initialize a counter for converted files

    for html_file in html_files:
        html_file_path = os.path.join(posts_dir, html_file)
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        markdown_content = convert_html_to_markdown(html_content)

        # Skip writing this file if it's identified as a comment and skip_comments is True
        if skip_comments and is_comment_file(markdown_content):
            continue
        
        md_filename = html_file.replace('.html', '.md')

        if remove_date:
            md_filename = md_filename.split('_')[1]

        # Remove alphanumeric string at the end of the filename
        md_filename = md_filename.rsplit('-', 1)[0]

        if replace_hyphens:
            md_filename = md_filename.replace('-', ' ').replace('--', ' ')

        # Replace occurrences of two or more spaces with a single space
        md_filename = re.sub(r' +', ' ', md_filename)
        
        md_filename += '.md'  # Ensure the filename ends with '.md'
        markdown_file_path = os.path.join(extract_path, md_filename)
        
        with open(markdown_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        
        converted_files_count += 1  # Increment the counter for each file converted

    # Clean up cache directory
    for root, dirs, files in os.walk(cache_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(cache_dir)

    return converted_files_count  # Return the count of converted files


def select_input():
    zip_path = filedialog.askopenfilename(title='Select ZIP File', filetypes=[('ZIP files', '*.zip')])
    if zip_path:
        input_path.set(zip_path)

def select_output():
    extract_path = filedialog.askdirectory(title='Select Export Directory')
    if extract_path:
        output_path.set(extract_path)

def start_conversion():
    zip_path = input_path.get()
    extract_path = output_path.get()
    if zip_path and extract_path:
        remove_date = remove_date_var.get()
        replace_hyphens = replace_hyphens_var.get()
        process_zip_file(zip_path, extract_path, remove_date, replace_hyphens)

def start_conversion():
    zip_path = input_path.get()
    extract_path = output_path.get()
    if zip_path and extract_path:
        remove_date = remove_date_var.get()
        replace_hyphens = replace_hyphens_var.get()
        skip_comments = skip_comments_var.get()
        converted_files_count = process_zip_file(zip_path, extract_path, remove_date, replace_hyphens, skip_comments)
        messagebox.showinfo("Conversion Complete", f"Successfully converted {converted_files_count} files!")

# Create and configure the GUI window
window = tk.Tk()
window.title('HTML to Markdown Converter')
window.geometry('600x200')  # Adjusted geometry to accommodate the new text box

frame = ttk.Frame(window, padding="10")
frame.pack(fill=tk.BOTH, expand=True)


input_path = StringVar()
output_path = StringVar()

remove_date_var = IntVar(value=1)  # Checkbox selected by default
replace_hyphens_var = IntVar(value=1)  # Checkbox selected by default
skip_comments_var = IntVar(value=1)  # Checkbox selected by default

ttk.Button(frame, text="Select Input ZIP", command=select_input).grid(row=0, column=0, pady=5, sticky=tk.W)
ttk.Label(frame, textvariable=input_path, width=50).grid(row=0, column=1, pady=5, sticky=tk.W)

ttk.Button(frame, text="Select Output Directory", command=select_output).grid(row=1, column=0, pady=5, sticky=tk.W)
ttk.Label(frame, textvariable=output_path, width=50).grid(row=1, column=1, pady=5, sticky=tk.W)

ttk.Checkbutton(frame, text="Remove Date from Filename", variable=remove_date_var).grid(row=2, column=0, pady=5, sticky=tk.W)
ttk.Checkbutton(frame, text="Replace Hyphens with Spaces", variable=replace_hyphens_var).grid(row=2, column=1, pady=5, sticky=tk.W)
ttk.Checkbutton(frame, text="Skip Comments", variable=skip_comments_var).grid(row=3, column=0, pady=5, sticky=tk.W)

convert_button = ttk.Button(frame, text='Convert', command=start_conversion)
convert_button.grid(row=4, columnspan=2, pady=20)

window.mainloop()
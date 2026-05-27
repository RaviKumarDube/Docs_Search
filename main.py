from tkinter import messagebox, filedialog
import tkinter as tk
import json
import os
app=tk.Tk()
app.title("Docsearch")
app.geometry("1000x600")
app.resizable(False, False)
color={
    "bg":"#0f1117",
    "panel":"#161b27",
    "logotext":"#00ff26",
    "text": "#f5f5f5"
    
}
app.configure(bg=color["bg"])
frame=tk.Frame(app, width=1000, height=500, bg=color["panel"])
frame.grid(row=0, column=0, padx=0, pady=10)
label=tk.Label(frame, text="# Docsearch", font=("Arial", 14), bg=color["panel"], fg=color["logotext"])
label.grid(row=0, column=0, padx=5, pady=10)



entry_frame=tk.Frame(frame, bg=color["panel"])
entry_frame.grid(row=0, column=2, padx=5, pady=0)
search_entry=tk.Entry(entry_frame, width=50, font=("Arial", 12), bg=color["bg"], fg="gray", insertbackground=color["text"], bd=1, relief="solid", highlightthickness=0)
search_entry.grid(row=0, column=6, ipady=8, padx=30)

placeholder_text = "Search URL or folder/file name here..."

search_entry.insert(0, placeholder_text)

original_fg = color["text"]

SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".docx", ".csv", ".json", ".xml", ".html", ".htm", ".py", ".js", ".log"}

indexed_folders = []


def on_focus_in(event):
    if search_entry.get() == placeholder_text:
        search_entry.delete(0, tk.END)
        search_entry.config(fg=original_fg)


def on_focus_out(event):
    if search_entry.get() == "":
        search_entry.insert(0, placeholder_text)
        search_entry.config(fg="gray")


def get_search_query():
    query = search_entry.get().strip()
    return "" if query == placeholder_text else query


def get_selected_folder():
    selected = add_folder_list.curselection()
    return indexed_folders[selected[0]] if selected else None


def scan_folder(folder_path):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTS:
                files.append(os.path.join(root, filename))
    return sorted(files, key=lambda x: x.lower())


def update_search_results():
    search_entry_list.delete(0, tk.END)
    query = get_search_query().lower()
    folder_path = get_selected_folder()

    files = []
    if folder_path:
        files = scan_folder(folder_path)
    else:
        for folder in indexed_folders:
            files.extend(scan_folder(folder))

    for path in files:
        if not query or query in path.lower():
            search_entry_list.insert(tk.END, path)


def add_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return
    if folder_path in indexed_folders:
        messagebox.showinfo("Folder already added", f"Folder is already in the list: {folder_path}")
        return
    indexed_folders.append(folder_path)
    add_folder_list.insert(tk.END, os.path.basename(folder_path) or folder_path)
    add_folder_list.selection_clear(0, tk.END)
    add_folder_list.selection_set(tk.END)
    add_folder_list.activate(tk.END)
    update_search_results()


def on_folder_select(event):
    if get_selected_folder():
        update_search_results()


def clear_search_results():
    search_entry_list.delete(0, tk.END)


def clear_folder_list():
    add_folder_list.delete(0, tk.END)
    indexed_folders.clear()
    clear_search_results()


search_entry.bind("<FocusIn>", on_focus_in)
search_entry.bind("<FocusOut>", on_focus_out)
search_entry.bind("<KeyRelease>", lambda event: update_search_results())
search_entry.bind("<Return>", lambda event: update_search_results())

Search_button=tk.Button(entry_frame, text="Search",width=10,height=1, font=("Arial", 12), bg=color["logotext"], fg=color["bg"], bd=1, relief="solid", highlightthickness=0, command=update_search_results)
Search_button.grid(row=0, column=7, padx=0, pady=0)
add_folder_button=tk.Button(frame, text="Add Folder",width=10,height=1, font=("Arial", 12), bg=color["logotext"], fg=color["bg"], bd=1, relief="solid", highlightthickness=0, command= add_folder)
add_folder_button.grid(row=0, column=8, padx=5, pady=10)

list_page = tk.Frame(app, width=1000, height=500, bg=color["bg"])
list_page.grid(row=1, column=0, padx=0, pady=0)
list_label = tk.Label(list_page, text=" Results", font=("Arial", 14   ), bg=color["bg"], fg=color["logotext"])
list_label.grid(row=1, column=0)

search_entry_list=tk.Listbox(list_page, width=70, height=22, font=("Arial", 12), bg=color["panel"], fg=color["text"], bd=1, relief="solid")
search_entry_list.grid(row=2, column=0, pady=10, padx=40)


label_folder_list=tk.Label(list_page, text="Added Folders", font=("Arial", 14), bg=color["bg"], fg=color["logotext"])
label_folder_list.grid(row=1, column=1)
add_folder_list=tk.Listbox(list_page, width=25, height=22, font=("Arial", 12), bg=color["panel"], fg=color["text"], bd=1, relief="solid")
add_folder_list.grid(row=2, column=1, pady=10, padx=10)
add_folder_list.bind("<<ListboxSelect>>", on_folder_select)

clear_search_button=tk.Button(list_page, text="Clear Results",width=20,height=1, font=("Arial", 12), bg=color["logotext"], fg=color["bg"], bd=1, relief="solid", highlightthickness=0, command=clear_search_results)
clear_search_button.grid(row=3, column=0, padx=10, pady=10)
clear_folder_button=tk.Button(list_page, text="Clear Folder List",width=20,height=  1, font=("Arial", 12), bg=color["logotext"], fg=color["bg"], bd=1, relief="solid", highlightthickness=0, command=clear_folder_list)
clear_folder_button.grid(row=3, column=1, padx=10, pady=10)    


app.mainloop()
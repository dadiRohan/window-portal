import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import ctypes

# --- THE HIDING TRICK ---
appdata_dir = os.path.join(os.environ['LOCALAPPDATA'], 'OfflineDataPortal')
os.makedirs(appdata_dir, exist_ok=True)
DB_NAME = os.path.join(appdata_dir, "client_database.db")

def hide_file(filepath):
    """Force Windows to set the file attribute to HIDDEN"""
    try:
        ctypes.windll.kernel32.SetFileAttributesW(filepath, 2)
    except Exception:
        pass

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()
    hide_file(DB_NAME)

def save_data():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    notes = notes_text.get("1.0", tk.END).strip()
    
    if not name:
        messagebox.showwarning("Input Error", "Name field is required!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data_entries (name, phone, notes) VALUES (?, ?, ?)", (name, phone, notes))
    conn.commit()
    conn.close()
    hide_file(DB_NAME)
    
    messagebox.showinfo("Success", "Data saved successfully!")
    clear_inputs()
    load_data()

def load_data():
    """Loads all records or filters them based on search box parameters"""
    for item in tree.get_children():
        tree.delete(item)
        
    search_query = search_entry.get().strip()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # If the user typed something into the search bar, filter the database query
    if search_query:
        query = """
            SELECT id, name, phone, notes FROM data_entries 
            WHERE name LIKE ? OR phone LIKE ? 
            ORDER BY id DESC
        """
        # The '%' signs allow partial matches (e.g., searching "Joh" finds "John Doe")
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
    else:
        # Otherwise, fetch everything normally
        cursor.execute("SELECT id, name, phone, notes FROM data_entries ORDER BY id DESC")
        
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def clear_inputs():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    notes_text.delete("1.0", tk.END)
    tree.selection_remove(tree.selection())

def clear_search():
    """Clears the search box and restores the complete database view"""
    search_entry.delete(0, tk.END)
    load_data()

def on_row_select(event):
    selected = tree.selection()
    if not selected:
        return
    row_data = tree.item(selected, 'values')
    
    name_entry.delete(0, tk.END)
    name_entry.insert(0, row_data[1])
    
    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, row_data[2])
    
    notes_text.delete("1.0", tk.END)
    notes_text.insert("1.0", row_data[3])

def update_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record from the table below to edit!")
        return
    row_id = tree.item(selected, 'values')[0]
    
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    notes = notes_text.get("1.0", tk.END).strip()
    
    if not name:
        messagebox.showwarning("Input Error", "Name field cannot be empty!")
        return
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE data_entries SET name=?, phone=?, notes=? WHERE id=?", (name, phone, notes, row_id))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Updated", "Record modified successfully!")
    clear_inputs()
    load_data()

def delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record from the table below to delete!")
        return
    
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to permanently delete this record?")
    if confirm:
        row_id = tree.item(selected, 'values')[0]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM data_entries WHERE id=?", (row_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Deleted", "Record wiped successfully!")
        clear_inputs()
        load_data()

init_db()
root = tk.Tk()
root.title("User Portal")
root.geometry("650x680") # Marginally taller window layout to fit search bar smoothly

# --- Section 1: Form Inputs ---
form_frame = ttk.LabelFrame(root, text=" Record Information ", padding=10)
form_frame.pack(fill="x", padx=15, pady=10)

ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
name_entry = ttk.Entry(form_frame, width=60)
name_entry.grid(row=0, column=1, pady=2, padx=5)

ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w", pady=2)
phone_entry = ttk.Entry(form_frame, width=60)
phone_entry.grid(row=1, column=1, pady=2, padx=5)

ttk.Label(form_frame, text="Notes:").grid(row=2, column=0, sticky="nw", pady=2)
notes_text = tk.Text(form_frame, width=45, height=5)
notes_text.grid(row=2, column=1, pady=2, padx=5)

# --- Section 2: Control Buttons ---
btn_frame = ttk.Frame(root)
btn_frame.pack(fill="x", padx=15, pady=5)

ttk.Button(btn_frame, text="Save New", command=save_data).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Update Selected", command=update_data).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Delete Selected", command=delete_data).pack(side="left", padx=5)
ttk.Button(btn_frame, text="Clear Fields", command=clear_inputs).pack(side="left", padx=5)

# --- Section 3: Interactive Search Bar ---
search_frame = ttk.LabelFrame(root, text=" Search Filters ", padding=10)
search_frame.pack(fill="x", padx=15, pady=5)

ttk.Label(search_frame, text="Search Name or Phone:").pack(side="left", padx=5)
search_entry = ttk.Entry(search_frame, width=35)
search_entry.pack(side="left", padx=5)

# Triggers the search instantly when user presses 'Enter' inside the bar
search_entry.bind("<Return>", lambda e: load_data()) 

ttk.Button(search_frame, text="Search", command=load_data).pack(side="left", padx=5)
ttk.Button(search_frame, text="Clear Search", command=clear_search).pack(side="left", padx=5)

# --- Section 4: Live Database Table ---
table_frame = ttk.LabelFrame(root, text=" Stored Records (Click any row to Edit/Delete) ", padding=10)
table_frame.pack(fill="both", expand=True, padx=15, pady=10)

columns = ("id", "name", "phone", "notes")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("phone", text="Phone")
tree.heading("notes", text="Notes")

tree.column("id", width=40, anchor="center")
tree.column("name", width=150)
tree.column("phone", width=120)
tree.column("notes", width=260)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_row_select)

load_data()
root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import csv

def init_db():
    conn = sqlite3.connect('stock_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_article(name, price, quantity):
    if not name or not price or not quantity:
        messagebox.showerror("Error", "All fields must be filled!")
        return
    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer!")
        return
    conn = sqlite3.connect('stock_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (name, price, quantity)
        VALUES (?, ?, ?)
    ''', (name, price, quantity))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Article added successfully!")
    list_articles()

def delete_article(article_id):
    conn = sqlite3.connect('stock_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles WHERE id = ?
    ''', (article_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Article deleted successfully!")
    list_articles()

def update_article(article_id, name, price, quantity):
    if not article_id or not name or not price or not quantity:
        messagebox.showerror("Error", "All fields must be filled!")
        return
    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Quantity must be an integer!")
        return

    conn = sqlite3.connect('stock_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE articles
        SET name = ?, price = ?, quantity = ?
        WHERE id = ?
    ''', (name, price, quantity, article_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Article updated successfully!")
    list_articles()

def list_articles():
    conn = sqlite3.connect('stock_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    for article in articles:
        tree.insert('', tk.END, values=article)
    return articles

def export_to_csv(file_name="articles.csv"):
    articles = list_articles()
    if not articles:
        messagebox.showwarning("Warning", "No articles to export!")
        return
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(['ID', 'Name', 'Price', 'Quantity'])
        for article in articles:
            csvwriter.writerow([article[0], article[1].replace(",", " "), article[2], article[3]])
    messagebox.showinfo("Success", "Articles exported to CSV successfully!")

def get_selected_article(event):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    if values:
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_price.delete(0, tk.END)
        entry_price.insert(0, values[2])
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, values[3])

init_db()

root = tk.Tk()
root.title("Stock Management System")

frame = tk.Frame(root)
frame.pack(pady=20)

# Label de bienvenue
welcome_label = tk.Label(frame, text="WELCOME TO STOCK MANAGEMENT SYSTEM", font=("Helvetica", 16, "bold"))
welcome_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Labels and Entry widgets
tk.Label(frame, text="ID").grid(row=1, column=0, padx=10, pady=5)
tk.Label(frame, text="Name").grid(row=2, column=0, padx=10, pady=5)
tk.Label(frame, text="Price").grid(row=3, column=0, padx=10, pady=5)
tk.Label(frame, text="Quantity").grid(row=4, column=0, padx=10, pady=5)

entry_id = tk.Entry(frame)
entry_id.grid(row=1, column=1, padx=10, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=2, column=1, padx=10, pady=5)
entry_price = tk.Entry(frame)
entry_price.grid(row=3, column=1, padx=10, pady=5)
entry_quantity = tk.Entry(frame)
entry_quantity.grid(row=4, column=1, padx=10, pady=5)

# Buttons 
add_button = tk.Button(frame, text="Add", command=lambda: add_article(entry_name.get(), entry_price.get(), entry_quantity.get()), bg="green", fg="white")
add_button.grid(row=5, column=0, padx=(100, 5), pady=5, columnspan=1)

update_button = tk.Button(frame, text="Update", command=lambda: update_article(entry_id.get(), entry_name.get(), entry_price.get(), entry_quantity.get()), bg="blue", fg="white")
update_button.grid(row=5, column=1, padx=5, pady=5, columnspan=1)

delete_button = tk.Button(frame, text="Delete", command=lambda: delete_article(entry_id.get()), bg="red", fg="white")
delete_button.grid(row=5, column=2, padx=(5, 100), pady=5, columnspan=1)



# Treeview
tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Quantity"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
tree.pack(pady=20)
tree.bind('<ButtonRelease-1>', get_selected_article)

# Bouton Export to CSV
export_button = tk.Button(root, text="Export to CSV", command=export_to_csv, bg="purple", fg="white")
export_button.pack(pady=10)


list_articles()

root.mainloop()

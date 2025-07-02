import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os

DATA_DIR = "data"

def get_registered_users():
    if not os.path.exists(DATA_DIR):
        return []
    files = os.listdir(DATA_DIR)
    return [f.split("_embedding.pkl")[0] for f in files if f.endswith("_embedding.pkl")]

def register_face():
    subprocess.Popen(["python", "faceid_register_gui.py"])

def authenticate_face():
    subprocess.Popen(["python", "faceid_authenticate_gui.py"])

def delete_faceid():
    users = get_registered_users()
    if not users:
        messagebox.showinfo("No Users", "No face IDs registered yet.")
        return

    username = simpledialog.askstring("Delete Face ID", f"Enter username to delete:\n{', '.join(users)}")
    if username and f"{username}_embedding.pkl" in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, f"{username}_embedding.pkl"))
        messagebox.showinfo("Deleted", f"❌ Face ID for '{username}' has been removed.")
    else:
        messagebox.showwarning("Not Found", "❌ Username not found.")

def view_users():
    users = get_registered_users()
    if users:
        messagebox.showinfo("Registered Users", "\n".join(users))
    else:
        messagebox.showinfo("No Users", "No face IDs registered yet.")

# GUI Setup
root = tk.Tk()
root.title("🧠 Face ID System")
root.geometry("400x400")
root.configure(bg="#1c1c1c")

tk.Label(root, text="Face ID System", font=("Helvetica", 20, "bold"), fg="white", bg="#1c1c1c").pack(pady=30)

tk.Button(root, text="🟢 Register Face ID", font=("Helvetica", 14), command=register_face,
          bg="#00cc66", fg="white", width=25).pack(pady=10)

tk.Button(root, text="🔐 Authenticate", font=("Helvetica", 14), command=authenticate_face,
          bg="#3399ff", fg="white", width=25).pack(pady=10)

tk.Button(root, text="📋 View Registered Users", font=("Helvetica", 12), command=view_users,
          bg="#999966", fg="white", width=25).pack(pady=10)

tk.Button(root, text="❌ Delete Face ID", font=("Helvetica", 12), command=delete_faceid,
          bg="#cc3300", fg="white", width=25).pack(pady=10)

tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.destroy,
          bg="#555555", fg="white", width=15).pack(pady=30)

root.mainloop()
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import json
import cv2
import mysql.connector

class EmployeeQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee QR Code Generator with MySQL")

        # Connect to MySQL
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#26809Vinayaksood",
            database="company"
        )
        self.cursor = self.db.cursor()
        self.create_table()

        # Form Fields
        self.entries = {}
        fields = ["Name", "ID", "Department", "Email"]
        for i, field in enumerate(fields):
            label = tk.Label(root, text=field)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(root, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field.lower()] = entry

        # Buttons
        tk.Button(root, text="Generate QR Code", command=self.generate_qr).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Load QR Code", command=self.load_qr).grid(row=6, column=0, columnspan=2, pady=5)

        # Image Display
        self.qr_label = tk.Label(root)
        self.qr_label.grid(row=0, column=2, rowspan=7, padx=20)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(100),
                email VARCHAR(100),
                qr_file VARCHAR(100)
            )
        """)
        self.db.commit()

    def generate_qr(self):
        data = {
            key: entry.get() for key, entry in self.entries.items()
        }

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        json_data = json.dumps(data)

            # 🗂️ Save to custom folder
        folder = "qr_codes"
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"{data['id']}_qr.png")

        qr = qrcode.make(json_data)
        qr.save(filename)

        # Display image
        img = Image.open(filename).resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk

        # Insert into MySQL
        try:
            self.cursor.execute(
                "INSERT INTO employees (id, name, department, email, qr_file) VALUES (%s, %s, %s, %s, %s)",
                (data['id'], data['name'], data['department'], data['email'], filename)
            )
            self.db.commit()
            messagebox.showinfo("Success", f"QR Code saved and data stored in MySQL.")
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists in the database.")

    def load_qr(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if not path:
            return

        img = cv2.imread(path)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        if data:
            try:
                emp_data = json.loads(data)
                msg = "\n".join(f"{k.capitalize()}: {v}" for k, v in emp_data.items())
                messagebox.showinfo("Employee Info", msg)
            except:
                messagebox.showerror("Error", "QR Code content is invalid")
        else:
            messagebox.showerror("Error", "No QR Code detected in image")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeQRApp(root)
    root.mainloop()

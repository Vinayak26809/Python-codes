import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import json
import cv2

class EmployeeQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee QR Code Generator")

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

    def generate_qr(self):
        data = {
            key: entry.get() for key, entry in self.entries.items()
        }

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        json_data = json.dumps(data)
        qr = qrcode.make(json_data)
        qr.save("employee_qr.png")

        # Display the image
        img = Image.open("employee_qr.png").resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk

        messagebox.showinfo("Success", "QR Code Generated and Saved as 'employee_qr.png'")

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

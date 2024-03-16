# leitor-de-HD
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR App")

        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10)

        browse_button = tk.Button(self.root, text="Select Image", command=self.load_image)
        browse_button.pack(pady=5)

        extract_button = tk.Button(self.root, text="Extract Text", command=self.extract_text)
        extract_button.pack(pady=5)

        self.text_box = tk.Text(self.root, height=10, width=50)
        self.text_box.pack(padx=10, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)

    def extract_text(self):
        if hasattr(self, 'image'):
            extracted_text = pytesseract.image_to_string(self.image)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, extracted_text)
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, "Please select an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from PIL.ExifTags import TAGS

class MetadataScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Escáner de Metadatos de Imágenes")
        master.geometry("600x400")

        self.label = tk.Label(master, text="Arrastra y suelta una imagen aquí o haz clic para seleccionar")
        self.label.pack(pady=20)

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(pady=10)

        self.label.bind("<Button-1>", self.browse_files)
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        file_path = event.data.strip('{}')  # Remove braces added by some OS
        self.extract_metadata(file_path)

    def browse_files(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.tiff")])
        if file_path:
            self.extract_metadata(file_path)

    def extract_metadata(self, image_path):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, f"Metadata for {image_path}:\n\n")
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if not exif_data:
                self.text_area.insert(tk.END, "No EXIF metadata found.")
                return
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                self.text_area.insert(tk.END, f"{tag_name}: {value}\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Error reading {image_path}: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MetadataScannerApp(root)
    root.mainloop()

import urllib.request
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import urllib.error
import socket

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Webpage Text Scraper")
        self.root.geometry("600x400")
        
        # URL Frame
        url_frame = ttk.LabelFrame(root, text="URL", padding="5")
        url_frame.pack(fill="x", padx=5, pady=5)
        
        self.url_entry = ttk.Entry(url_frame, width=70)
        self.url_entry.pack(fill="x", padx=5, pady=2)
        
        # File Path Frame
        file_frame = ttk.LabelFrame(root, text="Save Location", padding="5")
        file_frame.pack(fill="x", padx=5, pady=5)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=60)
        self.file_entry.pack(side="left", padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_location)
        browse_btn.pack(side="right", padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)
        
        preview_btn = ttk.Button(btn_frame, text="Preview", command=self.preview_text)
        preview_btn.pack(side="left", padx=5)
        
        save_btn = ttk.Button(btn_frame, text="Save", command=self.save_text)
        save_btn.pack(side="left", padx=5)
        
        # Preview Area
        preview_frame = ttk.LabelFrame(root, text="Preview", padding="5")
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.preview_text_widget = ScrolledText(preview_frame, wrap=tk.WORD, height=10)
        self.preview_text_widget.pack(fill="both", expand=True)
        
    def browse_location(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            
    def get_webpage_text(self):
        try:
            response = urllib.request.urlopen(self.url_entry.get())
            html_content = response.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = ""
            for paragraph in soup.find_all("p"):
                text_content += paragraph.get_text() + "\n\n"
            return text_content
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching webpage: {str(e)}")
            return None
            
    def preview_text(self):
        if not self.url_entry.get():
            messagebox.showwarning("Warning", "Please enter a URL")
            return
            
        text_content = self.get_webpage_text()
        if text_content:
            self.preview_text_widget.delete(1.0, tk.END)
            self.preview_text_widget.insert(tk.END, text_content)
            
    def save_text(self):
        if not self.file_path.get():
            messagebox.showwarning("Warning", "Please select a save location")
            return
            
        text_content = self.preview_text_widget.get(1.0, tk.END)
        try:
            with open(self.file_path.get(), 'w', encoding='utf-8') as file:
                file.write(text_content)
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()
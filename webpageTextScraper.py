import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import json

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Webpage Scraper")
        self.root.geometry("800x700")
        
        # Configure headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        # URL Frame
        url_frame = ttk.LabelFrame(root, text="URL", padding="5")
        url_frame.pack(fill="x", padx=5, pady=5)
        
        self.url_entry = ttk.Entry(url_frame, width=70)
        self.url_entry.pack(fill="x", padx=5, pady=2)
        
        # Scraping Options Frame
        options_frame = ttk.LabelFrame(root, text="Scraping Options", padding="5")
        options_frame.pack(fill="x", padx=5, pady=5)
        
        self.scrape_text = tk.BooleanVar(value=True)
        self.scrape_links = tk.BooleanVar(value=False)
        self.scrape_images = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Text Content", variable=self.scrape_text).pack(side="left", padx=5)
        ttk.Checkbutton(options_frame, text="Links", variable=self.scrape_links).pack(side="left", padx=5)
        ttk.Checkbutton(options_frame, text="Images", variable=self.scrape_images).pack(side="left", padx=5)
        
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
            
    def scrape_webpage(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            result = {}
            
            if self.scrape_text.get():
                result['text'] = []
                for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'article']):
                    result['text'].append(elem.get_text().strip())
            
            if self.scrape_links.get():
                result['links'] = []
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and href.startswith('http'):
                        result['links'].append(href)
            
            if self.scrape_images.get():
                result['images'] = []
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        result['images'].append(src)
            
            return json.dumps(result, indent=2)
            
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch webpage: {str(e)}")
            return None
            
    def preview_text(self):
        if not self.url_entry.get():
            messagebox.showwarning("Warning", "Please enter a URL")
            return
            
        text_content = self.scrape_webpage()
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
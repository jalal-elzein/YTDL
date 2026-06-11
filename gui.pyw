import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import ctypes

# DPI Awareness Fix
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

class YTDLGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Video Downloader")
        self.root.geometry("900x450")

        # Variables
        self.url_var = tk.StringVar()
        self.audio_var = tk.BooleanVar(value=True) # Default Checked
        self.thumb_var = tk.BooleanVar(value=True) # NEW: Thumbnail default Checked
        self.format_var = tk.StringVar(value="mp3")
        self.output_path_var = tk.StringVar(value=str(Path.home() / "Desktop/Songs/"))

        self.setup_ui()

    def setup_ui(self):
        ui_font = ("Segoe UI", 10)
        
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. URL Input
        tk.Label(main_container, text="YouTube Link:", font=ui_font).pack(anchor="w")
        tk.Entry(main_container, textvariable=self.url_var, font=ui_font).pack(fill="x", pady=(5, 15))

        # 2. Output Directory
        tk.Label(main_container, text="Save To:", font=ui_font).pack(anchor="w")
        path_frame = tk.Frame(main_container)
        path_frame.pack(fill="x", pady=5)
        
        tk.Entry(path_frame, textvariable=self.output_path_var, font=ui_font).pack(side="left", fill="x", expand=True)
        tk.Button(path_frame, text="Browse", command=self.browse_folder, font=ui_font).pack(side="left", padx=5)

        # 3. Options Frame
        options_frame = tk.LabelFrame(main_container, text="Options", font=ui_font, padx=10, pady=10)
        options_frame.pack(fill="x", pady=15)

        # Checkboxes side-by-side
        tk.Checkbutton(options_frame, text="Extract Audio Only", variable=self.audio_var, font=ui_font).pack(side="left")
        
        # NEW: The Thumbnail Toggle Checkbox
        tk.Checkbutton(options_frame, text="Embed Thumbnail", variable=self.thumb_var, font=ui_font).pack(side="left", padx=15)
        
        tk.Label(options_frame, text="Format:", font=ui_font).pack(side="left", padx=(10, 5))
        combo = ttk.Combobox(options_frame, textvariable=self.format_var, values=["mp3", "m4a"], width=8, state="readonly", font=ui_font)
        combo.pack(side="left")

        # 4. Download Button
        self.download_btn = tk.Button(main_container, text="Start Download", bg="#4CAF50", fg="white", 
                                      font=("Segoe UI", 11, "bold"), command=self.start_download_thread,
                                      pady=10)
        self.download_btn.pack(fill="x", pady=(20, 0))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path_var.set(folder)

    def start_download_thread(self):
        thread = threading.Thread(target=self.run_download, daemon=True)
        thread.start()

    def run_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please paste a YouTube link!")
            return

        self.download_btn.config(state="disabled", text="Downloading...")

        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", r"C:\ffmpeg\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\bin",
            "--paths", self.output_path_var.get(),
            url
        ]

        # Conditional Audio Extraction
        if self.audio_var.get():
            cmd.extend(["-x", "--audio-format", self.format_var.get()])
            
            # NEW: Only append thumbnail flags if the checkbox is checked
            if self.thumb_var.get():
                cmd.extend(["--write-thumbnail", "--embed-thumbnail"])

        try:
            CREATE_NO_WINDOW = 0x08000000
            result = subprocess.run(cmd, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Download Finished! :3")
            else:
                messagebox.showerror("Download Error", result.stderr)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.download_btn.config(state="normal", text="Start Download")

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLGui(root)
    root.mainloop()
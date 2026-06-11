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
        self.root.geometry("800x450")

        # Formats definitions
        self.audio_formats = ["mp3", "m4a"]
        self.video_formats = ["mp4", "webm"]

        # Variables
        self.url_var = tk.StringVar()
        self.audio_var = tk.BooleanVar(value=True) # Default: Audio only
        self.thumb_var = tk.BooleanVar(value=True) 
        self.format_var = tk.StringVar(value="mp3") # Default format
        self.output_path_var = tk.StringVar(value=str(Path.home() / "Desktop"))

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
        # Added 'command=self.toggle_mode' so it triggers a function when clicked
        self.audio_check = tk.Checkbutton(options_frame, text="Extract Audio Only", 
                                          variable=self.audio_var, font=ui_font, 
                                          command=self.toggle_mode)
        self.audio_check.pack(side="left")
        
        # Thumbnail Checkbox
        self.thumb_check = tk.Checkbutton(options_frame, text="Embed Thumbnail", 
                                          variable=self.thumb_var, font=ui_font)
        self.thumb_check.pack(side="left", padx=15)
        
        tk.Label(options_frame, text="Format:", font=ui_font).pack(side="left", padx=(10, 5))
        
        # We save a reference to 'self.combo' so we can modify it later
        self.combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                  values=self.audio_formats, width=8, 
                                  state="readonly", font=ui_font)
        self.combo.pack(side="left")

        # 4. Download Button
        self.download_btn = tk.Button(main_container, text="Start Download", bg="#4CAF50", fg="white", 
                                      font=("Segoe UI", 11, "bold"), command=self.start_download_thread,
                                      pady=10)
        self.download_btn.pack(fill="x", pady=(20, 0))

    def toggle_mode(self):
        """Switches dropdown values and toggles elements based on Audio vs Video selection."""
        if self.audio_var.get():
            # Switch dropdown to Audio options
            self.combo.config(values=self.audio_formats)
            self.format_var.set("mp3")
            # Enable thumbnail option (since video files handle artwork differently or natively)
            self.thumb_check.config(state="normal")
        else:
            # Switch dropdown to Video options
            self.combo.config(values=self.video_formats)
            self.format_var.set("mp4")
            # Disable thumbnail embedding checkbox if it's a full video download
            self.thumb_check.config(state="disabled")

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
        selected_format = self.format_var.get()

        # Base Command
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", r"C:\ffmpeg\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\bin",
            "--paths", self.output_path_var.get(),
            url
        ]

        # Logic separation based on user choice
        if self.audio_var.get():
            # AUDIO DOWNLOAD MODE
            cmd.extend(["-x", "--audio-format", selected_format])
            if self.thumb_var.get():
                cmd.extend(["--write-thumbnail", "--embed-thumbnail"])
        else:
            # VIDEO DOWNLOAD MODE
            # Tells yt-dlp to grab the best video and best audio, then merge them into your choice format
            cmd.extend(["-f", f"bv*[ext={selected_format}]+ba/b[ext={selected_format}]/best"])
            cmd.extend(["--merge-output-format", selected_format])

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
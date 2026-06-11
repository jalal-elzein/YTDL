import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000

class YTDLGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Video Downloader")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # Variables
        self.url_var = tk.StringVar()
        self.audio_var = tk.BooleanVar(value=True)
        self.format_var = tk.StringVar(value="m4a")
        self.output_path_var = tk.StringVar(value=str(Path.home() / "Desktop"))

        self.setup_ui()

    def setup_ui(self):
        padding = {'padx': 20, 'pady': 10}

        # 1. URL Input
        tk.Label(self.root, text="YouTube Link:").pack(anchor="w", padx=20, pady=(15, 0))
        tk.Entry(self.root, textvariable=self.url_var, width=60).pack(**padding)

        # 2. Output Directory
        tk.Label(self.root, text="Save To:").pack(anchor="w", padx=20)
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill="x", padx=20)
        tk.Entry(path_frame, textvariable=self.output_path_var, width=45).pack(side="left")
        tk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side="left", padx=5)

        # 3. Audio Options
        options_frame = tk.LabelFrame(self.root, text="Options", padx=10, pady=10)
        options_frame.pack(fill="x", **padding)

        tk.Checkbutton(options_frame, text="Extract Audio Only", variable=self.audio_var, ).pack(side="left")
        tk.Label(options_frame, text="Format:").pack(side="left", padx=(20, 5))
        ttk.Combobox(options_frame, textvariable=self.format_var, values=["mp3", "m4a"], width=5).pack(side="left")

        # 4. Download Button
        self.download_btn = tk.Button(self.root, text="Start Download", bg="#4CAF50", fg="white", 
                                      font=("Arial", 10, "bold"), command=self.start_download_thread)
        self.download_btn.pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path_var.set(folder)

    def start_download_thread(self):
        # Run in thread so GUI doesn't "Not Responding"
        thread = threading.Thread(target=self.run_download, daemon=True)
        thread.start()

    def run_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please paste a YouTube link!")
            return

        self.download_btn.config(state="disabled", text="Downloading...")

        # Base Command
        # Note: Added -f "best" as a fallback
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", r"C:\ffmpeg\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\ffmpeg-2026-04-19-git-de18feb0f0-essentials_build\bin",
            "--paths", self.output_path_var.get(),
            url
        ]

        # Audio Logic
        if self.audio_var.get():
            cmd.extend(["-x", "--audio-format", self.format_var.get()])

        try:
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
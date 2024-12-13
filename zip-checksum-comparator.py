import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import zipfile
import os

class ZipChecksumComparator:
    def __init__(self, master):
        self.master = master
        master.title("ZIP File Checksum Comparator")
        master.geometry("700x600")
        master.configure(bg='#f0f0f0')

        # File path variables
        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()

        # Create main frame
        self.main_frame = tk.Frame(master, bg='#f0f0f0')
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # File Selection Frame
        self.file_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.file_frame.pack(fill=tk.X, pady=(0, 10))

        # First ZIP File Selection
        self.create_file_selection(self.file_frame, "First ZIP File:", 0, self.file1_path)

        # Second ZIP File Selection
        self.create_file_selection(self.file_frame, "Second ZIP File:", 1, self.file2_path)

        # Compare Button
        self.compare_btn = tk.Button(
            self.main_frame,
            text="Compare ZIP Contents",
            command=self.compare_zip_files,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        self.compare_btn.pack(pady=10)

        # Results Frame
        self.results_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Results Label
        self.results_label = tk.Label(
            self.results_frame,
            text="Comparison Results:",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        )
        self.results_label.pack(anchor='w', pady=(10, 5))

        # Results Text with Scrollbar
        self.results_text_frame = tk.Frame(self.results_frame)
        self.results_text_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = tk.Text(
            self.results_text_frame,
            height=15,
            width=80,
            wrap=tk.WORD,
            font=('Courier', 10),
            bg='white',
            borderwidth=2,
            relief=tk.SUNKEN
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for Results
        self.scrollbar = tk.Scrollbar(self.results_text_frame, command=self.results_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=self.scrollbar.set)

    def create_file_selection(self, parent, label_text, row, path_var):
        """Create a file selection row with label, entry, and browse button."""
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=('Arial', 10),
            bg='#f0f0f0'
        )
        label.grid(row=row, column=0, sticky='w', padx=(0, 10), pady=5)

        # Entry with long path display
        entry = tk.Entry(
            parent,
            textvariable=path_var,
            width=50,
            font=('Courier', 10)
        )
        entry.grid(row=row, column=1, padx=(0, 10), pady=5, sticky='ew')

        # Browse Button
        browse_btn = tk.Button(
            parent,
            text="Browse",
            command=lambda var=path_var: self.browse_file(var),
            bg='#2196F3',
            fg='white'
        )
        browse_btn.grid(row=row, column=2, pady=5)

        return entry

    def browse_file(self, path_var):
        """Open file dialog and set the path."""
        filename = filedialog.askopenfilename(
            title="Select ZIP File",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            path_var.set(filename)

    def compare_zip_files(self):
        """Compare contents of two ZIP files."""
        # Get file paths
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()

        # Validate file paths
        if not file1 or not file2:
            messagebox.showwarning("Warning", "Please select both ZIP files")
            return

        # Disable compare button during processing
        self.compare_btn.config(state=tk.DISABLED)

        try:
            # Get MD5 checksums
            file1_md5 = self.get_zip_contents_md5(file1)
            file2_md5 = self.get_zip_contents_md5(file2)

            # Compare checksums
            if not file1_md5 or not file2_md5:
                return

            # Detailed comparison
            self.display_comparison_results(file1, file2, file1_md5, file2_md5)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            # Re-enable compare button
            self.compare_btn.config(state=tk.NORMAL)

    def get_zip_contents_md5(self, zip_path):
        """Generate MD5 checksums for all files in a ZIP archive."""
        md5_dict = {}
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if not file_info.is_dir():
                        with zip_ref.open(file_info) as file:
                            content = file.read()
                            md5_hash = hashlib.md5(content).hexdigest()
                            md5_dict[file_info.filename] = md5_hash
        except Exception as e:
            messagebox.showerror("Error", f"Could not read ZIP file: {e}")
        return md5_dict

    def display_comparison_results(self, file1, file2, file1_md5, file2_md5):
        """Display detailed comparison results."""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)

        # Comparison header
        self.results_text.insert(tk.END, "🔍 ZIP File Comparison Report\n", "header")
        self.results_text.insert(tk.END, f"File 1: {file1}\n", "file")
        self.results_text.insert(tk.END, f"File 2: {file2}\n\n", "file")

        # Check total number of files
        if len(file1_md5) != len(file2_md5):
            self.results_text.insert(tk.END, "❌ Different number of files\n", "error")
            self.results_text.insert(tk.END, f"File 1 contains {len(file1_md5)} files\n", "detail")
            self.results_text.insert(tk.END, f"File 2 contains {len(file2_md5)} files\n", "detail")
            return

        # Compare each file
        different_files = []
        for filename, md5 in file1_md5.items():
            if filename not in file2_md5:
                different_files.append(f"File {filename} not found in second ZIP")
            elif md5 != file2_md5[filename]:
                different_files.append(f"File {filename} has different content")

        # Display results
        if not different_files:
            self.results_text.insert(tk.END, "✅ ZIP files have identical contents!\n", "success")
        else:
            self.results_text.insert(tk.END, "❌ Differences found:\n", "error")
            for diff in different_files:
                self.results_text.insert(tk.END, f"  - {diff}\n", "detail")

        # Configure text tags for styling
        self.results_text.tag_config("header", font=('Arial', 12, 'bold'), foreground='navy')
        self.results_text.tag_config("file", font=('Courier', 10), foreground='dark green')
        self.results_text.tag_config("success", font=('Arial', 10, 'bold'), foreground='green')
        self.results_text.tag_config("error", font=('Arial', 10, 'bold'), foreground='red')
        self.results_text.tag_config("detail", font=('Courier', 10), foreground='blue')

def main():
    root = tk.Tk()
    app = ZipChecksumComparator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

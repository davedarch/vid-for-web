import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG
)

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        messagebox.showerror("Error", "ffmpeg is not installed or not found in PATH.")
        return False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Converter")
        self.geometry("700x700")  # Adjusted height to accommodate new widgets
        self.output_directory = Path.home()  # Default output directory
        logging.debug(f"Initial output directory set to: {self.output_directory}")
        self.output_dir_set_manually = False  # Flag to track manual setting
        self.load_scripts()
        self.create_widgets()

    def load_scripts(self):
        script_file = Path("./settings.json")  # Updated to settings.json in root
        if script_file.exists():
            try:
                with open(script_file, "r") as file:
                    data = json.load(file)
                    self.scripts = data.get("scripts", [])
            except json.JSONDecodeError as e:
                messagebox.showerror("JSON Error", f"Error parsing settings.json:\n{e}")
                logging.error(f"JSONDecodeError: {e}")
                self.scripts = []
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred while loading settings.json:\n{e}")
                logging.exception("Unexpected error in load_scripts")
                self.scripts = []
        else:
            messagebox.showerror("Error", "settings.json file not found.")
            logging.error("settings.json file not found.")
            self.scripts = []

    def create_widgets(self):
        # Input Files Selection
        self.select_input_button = tk.Button(self, text="Select Input Files", command=self.select_files)
        self.select_input_button.pack(pady=10)

        self.file_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=80)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=10)

        # Output Directory Selection
        self.select_output_button = tk.Button(self, text="Select Output Directory", command=self.select_output_directory)
        self.select_output_button.pack(pady=10)

        self.output_dir_label = tk.Label(self, text=f"Output Directory: {self.output_directory}")
        self.output_dir_label.pack(pady=5)

        # Script Selection
        self.script_var = tk.StringVar(self)
        self.script_dropdown = ttk.Combobox(
            self, 
            textvariable=self.script_var, 
            values=[script["name"] for script in self.scripts],
            state="readonly",
            width=50
        )
        self.script_dropdown.pack(pady=10)
        if self.scripts:
            self.script_dropdown.current(0)

        self.script_dropdown.bind("<<ComboboxSelected>>", self.on_script_selected)

        # Options Frame
        self.options_frame = tk.Frame(self)
        self.options_frame.pack(pady=10)

        self.option_widgets = {}  # To keep track of dynamically created option widgets

        # Process Button
        self.process_button = tk.Button(self, text="Process Files", command=self.process_selected_files)
        self.process_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        # Reset Output Directory Button (Optional)
        reset_button = tk.Button(self, text="Reset Output Directory", command=self.reset_output_directory)
        reset_button.pack(pady=5)

        # Initialize options based on the first script
        self.on_script_selected(None)

    def reset_output_directory(self):
        """Reset the output directory to the default behavior."""
        self.output_dir_set_manually = False
        self.output_directory = Path.home()
        self.output_dir_label.config(text=f"Output Directory: {self.output_directory}")
        messagebox.showinfo("Reset", "Output directory has been reset to the default.")

    def on_script_selected(self, event):
        # Clear previous option widgets
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_widgets.clear()

        script_name = self.script_var.get()
        script = next((s for s in self.scripts if s["name"] == script_name), None)
        if script:
            options = script.get("options", {})
            row = 0
            for option_key, option_values in options.items():
                label = tk.Label(self.options_frame, text=f"{option_key.upper()}:")
                label.grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)

                var = tk.StringVar(self)
                if isinstance(option_values, list):
                    if all(isinstance(item, (int, float)) for item in option_values):
                        # For numeric options, use Entry widget
                        entry = tk.Entry(self.options_frame, textvariable=var, width=10)
                        entry.grid(row=row, column=1, padx=5, pady=5)
                        var.set(str(option_values[0]))
                        self.option_widgets[option_key] = var
                    else:
                        # For string options, use Combobox
                        combobox = ttk.Combobox(
                            self.options_frame, 
                            textvariable=var, 
                            values=option_values,
                            state="readonly"
                        )
                        combobox.grid(row=row, column=1, padx=5, pady=5)
                        combobox.current(0)
                        self.option_widgets[option_key] = var
                else:
                    # Handle other types if necessary
                    entry = tk.Entry(self.options_frame, textvariable=var, width=10)
                    entry.grid(row=row, column=1, padx=5, pady=5)
                    var.set(str(option_values))
                    self.option_widgets[option_key] = var
                row += 1

    def select_files(self):
        filetypes = [("Video Files", "*.mp4 *.avi *.mov *.webm *.gif *.webp"), ("All Files", "*.*")]
        selected_files = filedialog.askopenfilenames(title="Select Input Files", filetypes=filetypes)
        for file in selected_files:
            if file not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, file)

        if selected_files and not self.output_dir_set_manually:
            # Set output directory to the directory of the first selected file only if not set manually
            first_file = selected_files[0]
            new_output_dir = Path(first_file).parent
            self.output_directory = new_output_dir
            self.output_dir_label.config(text=f"Output Directory: {self.output_directory}")
            logging.debug(f"Output directory auto-set to: {self.output_directory}")

    def select_output_directory(self):
        # Determine initial directory
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            first_selected_file = self.file_listbox.get(selected_indices[0])
            initial_dir = Path(first_selected_file).parent
        else:
            initial_dir = self.output_directory

        selected_dir = filedialog.askdirectory(title="Select Output Directory", initialdir=str(initial_dir))
        if selected_dir:
            self.output_directory = Path(selected_dir)
            self.output_dir_label.config(text=f"Output Directory: {self.output_directory}")
            self.output_dir_set_manually = True  # Mark that user has set it manually
            logging.debug(f"User set output directory to: {self.output_directory}")

    def process_selected_files(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("No Files Selected", "Please select files to process.")
            return

        selected_files = [self.file_listbox.get(i) for i in selected_indices]

        # Disable buttons during processing
        self.select_input_button.config(state=tk.DISABLED)
        self.select_output_button.config(state=tk.DISABLED)
        self.process_button.config(state=tk.DISABLED)

        for input_file in selected_files:
            self.status_label.config(text=f"Processing {input_file}")
            self.update_idletasks()
            self.process_file(input_file)

        self.status_label.config(text="Processing completed")
        messagebox.showinfo("Done", "All selected files have been processed.")

        # Enable buttons after processing
        self.select_input_button.config(state=tk.NORMAL)
        self.select_output_button.config(state=tk.NORMAL)
        self.process_button.config(state=tk.NORMAL)

    def process_file(self, input_file):
        try:
            script_name = self.script_var.get()
            script = next((s for s in self.scripts if s["name"] == script_name), None)
            if script:
                output_extension = script_name.lower()

                # Corrected Output File Path Construction
                if script_name.upper() == "WEBP":
                    output_filename = Path(input_file).stem + '.webp'
                    output_file = self.output_directory / output_filename
                else:
                    output_filename = Path(input_file).stem + f'.{output_extension}'
                    output_file = self.output_directory / output_filename

                # For GIF, define a palette file
                if script_name.upper() == "GIF":
                    palette_filename = Path(input_file).stem + '.palette.png'
                    palette_file = self.output_directory / palette_filename
                else:
                    palette_file = None

                options = script.get("options", {})
                
                # Gather selected options
                option_values = {key: var.get() for key, var in self.option_widgets.items()}

                # Convert Path objects to strings to avoid issues in formatting
                input_file_str = str(Path(input_file).resolve())
                output_file_str = str(output_file.resolve())
                palette_file_str = str(palette_file.resolve()) if palette_file else None

                # Log output directory and file paths
                logging.debug(f"Processing file: {input_file_str}")
                logging.debug(f"Output directory: {self.output_directory}")
                logging.debug(f"Output file: {output_file_str}")
                if palette_file_str:
                    logging.debug(f"Palette file: {palette_file_str}")

                # Update command formatting
                if palette_file_str:
                    ffmpeg_cmd = script["command"].format(
                        input_file=input_file_str, 
                        output_file=output_file_str,
                        palette_file=palette_file_str,
                        **option_values
                    )
                else:
                    ffmpeg_cmd = script["command"].format(
                        input_file=input_file_str, 
                        output_file=output_file_str,
                        **option_values
                    )
                
                # Log the command
                logging.info(f"Executing command: {ffmpeg_cmd}")
                print(f"Executing command: {ffmpeg_cmd}")  # For real-time feedback

                # Execute the command
                subprocess.run(ffmpeg_cmd, shell=True, check=True)

                if script_name.upper() == "WEBP":
                    messagebox.showinfo(
                        "WebP Conversion",
                        f"WebP file generated successfully:\n{output_file_str}"
                    )

            else:
                messagebox.showerror("Error", "Invalid script selected.")
                logging.error("Invalid script selected.")
        except subprocess.CalledProcessError as e:
            # Capture and decode stderr if available
            try:
                stderr = e.stderr.decode('utf-8') if e.stderr else str(e)
            except Exception:
                stderr = str(e)
            logging.error(f"FFmpeg Error for {input_file}: {stderr}")
            messagebox.showerror("FFmpeg Error", f"An error occurred while processing {input_file}:\n{stderr}")
        except Exception as e:
            logging.exception(f"Unexpected error for {input_file}: {e}")
            messagebox.showerror("Exception", f"An unexpected error occurred:\n{e}")

def main():
    if not check_ffmpeg():
        return

    app = App()
    app.mainloop()

if __name__ == '__main__':
    main() 
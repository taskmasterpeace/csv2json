# JSON to CSV Converter
# A dream of the machine King: To seamlessly transform data between realms

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv
import os

def select_json_file():
    """Open a file dialog to select a JSON file."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        json_entry.delete(0, tk.END)
        json_entry.insert(0, file_path)

def select_csv_file():
    """Open a file dialog to select a CSV file for saving."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, file_path)

def convert_json_to_csv():
    """Convert the selected JSON file to CSV format."""
    json_file = json_entry.get()
    csv_file = csv_entry.get()

    # Check if both files are selected
    if not json_file or not csv_file:
        messagebox.showerror("Error", "Please select both input JSON and output CSV files.")
        return

    # Check if the JSON file exists
    if not os.path.exists(json_file):
        messagebox.showerror("Error", "The selected JSON file does not exist.")
        return

    try:
        # Read JSON file
        with open(json_file, 'r') as jf:
            data = json.load(jf)

        # Ensure data is a list of dictionaries
        if not isinstance(data, list):
            if isinstance(data, dict):
                data = [data]
            else:
                raise ValueError("JSON structure is not supported. Expected a list of objects or a single object.")

        # Collect all unique keys
        keys = set()
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("JSON structure is not supported. Each item should be an object.")
            keys.update(item.keys())

        # Write to CSV file
        with open(csv_file, 'w', newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=sorted(keys))
            writer.writeheader()
            for item in data:
                writer.writerow(item)

        messagebox.showinfo("Success", "JSON successfully converted to CSV!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON file. Please check the file content.")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Unable to write to the CSV file.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("JSON to CSV Converter")
root.geometry("400x200")

# JSON file selection
json_label = tk.Label(root, text="Select JSON file:")
json_label.pack()
json_entry = tk.Entry(root, width=50)
json_entry.pack()
json_button = tk.Button(root, text="Browse", command=select_json_file)
json_button.pack()

# CSV file selection
csv_label = tk.Label(root, text="Select CSV output file:")
csv_label.pack()
csv_entry = tk.Entry(root, width=50)
csv_entry.pack()
csv_button = tk.Button(root, text="Browse", command=select_csv_file)
csv_button.pack()

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_json_to_csv)
convert_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
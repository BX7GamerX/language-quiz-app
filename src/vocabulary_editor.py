#!/usr/bin/env python3
"""
Vocabulary Database Editor
==========================
A GUI application for managing the language quiz vocabulary database.
Provides functionality to add, edit, delete, and manage vocabulary words
across multiple languages and word types.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import csv
import os
import sys
from datetime import datetime
import json

# Add the src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app_variables import CSVPaths, wordlib_location

class VocabularyDatabaseEditor:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Vocabulary Database Editor - Language Quiz App")
        self.root.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.setup_ui()
        self.load_vocabulary_data()
        
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(self.main_container, 
                                  text="Vocabulary Database Editor", 
                                  font=("Arial", 24, "bold"))
        title_label.pack(pady=(10, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for each word type
        self.tabs = {}
        self.data = {}
        
        word_types = [("Nouns", "nouns"), ("Verbs", "verbs"), 
                     ("Adjectives", "adjectives"), ("Adverbs", "adverbs")]
        
        for display_name, key in word_types:
            self.create_word_type_tab(display_name, key)
            
        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self.main_container)
        self.controls_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons
        save_btn = ctk.CTkButton(self.controls_frame, text="Save All Changes", 
                                command=self.save_all_data, width=150, height=32)
        save_btn.pack(side="left", padx=5, pady=5)
        
        export_btn = ctk.CTkButton(self.controls_frame, text="Export Backup", 
                                  command=self.export_backup, width=150, height=32)
        export_btn.pack(side="left", padx=5, pady=5)
        
        import_btn = ctk.CTkButton(self.controls_frame, text="Import Backup", 
                                  command=self.import_backup, width=150, height=32)
        import_btn.pack(side="left", padx=5, pady=5)
        
        stats_btn = ctk.CTkButton(self.controls_frame, text="Show Statistics", 
                                 command=self.show_statistics, width=150, height=32)
        stats_btn.pack(side="left", padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ctk.CTkLabel(self.controls_frame, textvariable=self.status_var,
                                 font=("Arial", 10), anchor="w")
        status_bar.pack(side="right", padx=5, pady=5)
    
    def create_word_type_tab(self, display_name, key):
        # Create tab frame
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=display_name)
        self.tabs[key] = tab_frame
        
        # Create main container for tab
        main_frame = ctk.CTkFrame(tab_frame)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Controls frame
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Add/Edit controls
        add_btn = ctk.CTkButton(controls_frame, text=f"Add New {display_name[:-1]}", 
                               command=lambda: self.add_word_dialog(key), width=120, height=28)
        add_btn.pack(side="left", padx=5, pady=5)
        
        edit_btn = ctk.CTkButton(controls_frame, text="Edit Selected", 
                                command=lambda: self.edit_selected_word(key), width=120, height=28)
        edit_btn.pack(side="left", padx=5, pady=5)
        
        delete_btn = ctk.CTkButton(controls_frame, text="Delete Selected", 
                                  command=lambda: self.delete_selected_word(key), width=120, height=28)
        delete_btn.pack(side="left", padx=5, pady=5)
        
        # Search frame
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(side="right", padx=5, pady=5)
        
        search_label = ctk.CTkLabel(search_frame, text="Search:")
        search_label.pack(side="left", padx=5)
        
        search_entry = ctk.CTkEntry(search_frame, width=200)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_words(key, search_entry.get()))
        
        # Create treeview for displaying words
        tree_frame = ctk.CTkFrame(main_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure columns based on word type
        if key == "nouns":
            columns = ("Pronoun", "German", "English", "French", "Spanish")
        else:
            columns = ("German", "English", "French", "Spanish")
            
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure column headings and widths
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Store references
        setattr(self, f"{key}_tree", tree)
        setattr(self, f"{key}_search_entry", search_entry)
        
    def load_vocabulary_data(self):
        """Load vocabulary data from CSV files"""
        self.data = {"nouns": [], "verbs": [], "adjectives": [], "adverbs": []}
        
        for file_path, word_type in wordlib_location:
            try:
                # Adjust path if needed
                if not os.path.exists(file_path):
                    file_path = file_path.replace("src/../", "")
                
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        self.data[word_type] = list(reader)
                    self.update_tree_display(word_type)
                    self.status_var.set(f"Loaded {len(self.data[word_type])} {word_type}")
                else:
                    self.status_var.set(f"File not found: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load {word_type}: {str(e)}")
                
    def update_tree_display(self, word_type, filter_text=""):
        """Update the treeview display for a specific word type"""
        tree = getattr(self, f"{word_type}_tree")
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Filter data if search text provided
        data_to_show = self.data[word_type]
        if filter_text:
            data_to_show = [word for word in self.data[word_type] 
                           if any(filter_text.lower() in str(value).lower() 
                                for value in word.values())]
        
        # Insert data
        for word_data in data_to_show:
            if word_type == "nouns":
                values = (word_data.get("Pronoun", ""), word_data.get("German", ""),
                         word_data.get("English", ""), word_data.get("French", ""),
                         word_data.get("Spanish", ""))
            else:
                values = (word_data.get("German", ""), word_data.get("English", ""),
                         word_data.get("French", ""), word_data.get("Spanish", ""))
            
            tree.insert("", "end", values=values)
    
    def filter_words(self, word_type, search_text):
        """Filter words based on search text"""
        self.update_tree_display(word_type, search_text)
    
    def add_word_dialog(self, word_type):
        """Show dialog to add a new word"""
        dialog = WordEditDialog(self.root, word_type)
        result = dialog.show()
        
        if result:
            self.data[word_type].append(result)
            self.update_tree_display(word_type)
            self.status_var.set(f"Added new {word_type[:-1]}")
    
    def edit_selected_word(self, word_type):
        """Edit the selected word"""
        tree = getattr(self, f"{word_type}_tree")
        selection = tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a word to edit")
            return
        
        # Get selected item data
        item = tree.item(selection[0])
        values = item['values']
        
        # Find the corresponding data entry
        word_data = None
        for i, data in enumerate(self.data[word_type]):
            if word_type == "nouns":
                if (data.get("German", "") == values[1] and 
                    data.get("English", "") == values[2]):
                    word_data = data
                    data_index = i
                    break
            else:
                if (data.get("German", "") == values[0] and 
                    data.get("English", "") == values[1]):
                    word_data = data
                    data_index = i
                    break
        
        if word_data:
            dialog = WordEditDialog(self.root, word_type, word_data)
            result = dialog.show()
            
            if result:
                self.data[word_type][data_index] = result
                self.update_tree_display(word_type)
                self.status_var.set(f"Updated {word_type[:-1]}")
    
    def delete_selected_word(self, word_type):
        """Delete the selected word"""
        tree = getattr(self, f"{word_type}_tree")
        selection = tree.selection()
        
        if not selection:
            messagebox.showwarning("Warning", "Please select a word to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this word?"):
            # Get selected item data
            item = tree.item(selection[0])
            values = item['values']
            
            # Find and remove the corresponding data entry
            for i, data in enumerate(self.data[word_type]):
                if word_type == "nouns":
                    if (data.get("German", "") == values[1] and 
                        data.get("English", "") == values[2]):
                        del self.data[word_type][i]
                        break
                else:
                    if (data.get("German", "") == values[0] and 
                        data.get("English", "") == values[1]):
                        del self.data[word_type][i]
                        break
            
            self.update_tree_display(word_type)
            self.status_var.set(f"Deleted {word_type[:-1]}")
    
    def save_all_data(self):
        """Save all vocabulary data back to CSV files"""
        try:
            for file_path, word_type in wordlib_location:
                # Adjust path if needed
                if not os.path.exists(os.path.dirname(file_path)):
                    file_path = file_path.replace("src/../", "")
                
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    if word_type == "nouns":
                        fieldnames = ["Pronoun", "German", "English", "French", "Spanish"]
                    else:
                        fieldnames = ["German", "English", "French", "Spanish"]
                    
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data[word_type])
            
            messagebox.showinfo("Success", "All vocabulary data saved successfully!")
            self.status_var.set("All data saved")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def export_backup(self):
        """Export vocabulary data as JSON backup"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Vocabulary Backup"
            )
            
            if filename:
                backup_data = {
                    "export_date": datetime.now().isoformat(),
                    "vocabulary": self.data
                }
                
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(backup_data, file, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Backup exported to {filename}")
                self.status_var.set("Backup exported")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export backup: {str(e)}")
    
    def import_backup(self):
        """Import vocabulary data from JSON backup"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import Vocabulary Backup"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    backup_data = json.load(file)
                
                if "vocabulary" in backup_data:
                    if messagebox.askyesno("Confirm Import", 
                                         "This will replace all current vocabulary data. Continue?"):
                        self.data = backup_data["vocabulary"]
                        
                        # Update all tree displays
                        for word_type in self.data.keys():
                            self.update_tree_display(word_type)
                        
                        messagebox.showinfo("Success", "Backup imported successfully!")
                        self.status_var.set("Backup imported")
                else:
                    messagebox.showerror("Error", "Invalid backup file format")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import backup: {str(e)}")
    
    def show_statistics(self):
        """Show vocabulary statistics"""
        stats = []
        total_words = 0
        
        for word_type, words in self.data.items():
            count = len(words)
            total_words += count
            stats.append(f"{word_type.title()}: {count} words")
        
        stats.append(f"\nTotal vocabulary: {total_words} words")
        
        # Check for completeness
        incomplete_words = []
        for word_type, words in self.data.items():
            for word in words:
                if word_type == "nouns":
                    required_fields = ["Pronoun", "German", "English", "French", "Spanish"]
                else:
                    required_fields = ["German", "English", "French", "Spanish"]
                
                for field in required_fields:
                    if not word.get(field, "").strip():
                        incomplete_words.append(f"{word_type}: Missing {field} for {word.get('German', 'Unknown')}")
                        break
        
        if incomplete_words:
            stats.append(f"\nIncomplete entries: {len(incomplete_words)}")
            if len(incomplete_words) <= 10:
                stats.extend(incomplete_words)
            else:
                stats.extend(incomplete_words[:10])
                stats.append(f"... and {len(incomplete_words) - 10} more")
        else:
            stats.append("\nAll entries are complete!")
        
        messagebox.showinfo("Vocabulary Statistics", "\n".join(stats))
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


class WordEditDialog:
    def __init__(self, parent, word_type, word_data=None):
        self.parent = parent
        self.word_type = word_type
        self.word_data = word_data or {}
        self.result = None
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(f"{'Edit' if word_data else 'Add'} {word_type.title()[:-1]}")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        
        # Set close protocol
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.setup_dialog()
        
        # Center dialog and make modal after it's visible
        self.dialog.after(100, self.center_and_focus)
    
    def center_and_focus(self):
        """Center dialog and make it modal safely"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Now make it modal safely
        try:
            self.dialog.grab_set()
            self.dialog.focus_set()
        except tk.TclError:
            # If grab_set fails, just focus without modal behavior
            self.dialog.focus_set()
    
    def setup_dialog(self):
        # Main container
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_text = f"{'Edit' if self.word_data else 'Add New'} {self.word_type.title()[:-1]}"
        title_label = ctk.CTkLabel(main_frame, text=title_text, font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Form fields
        self.entries = {}
        
        if self.word_type == "nouns":
            fields = [("Pronoun", "German article (Der/Die/Das)"),
                     ("German", "German word"),
                     ("English", "English translation"),
                     ("French", "French translation"),
                     ("Spanish", "Spanish translation")]
        else:
            fields = [("German", "German word"),
                     ("English", "English translation"),
                     ("French", "French translation"),
                     ("Spanish", "Spanish translation")]
        
        for field, description in fields:
            # Field frame
            field_frame = ctk.CTkFrame(main_frame)
            field_frame.pack(fill="x", pady=5)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=f"{field}:", width=80, anchor="w")
            label.pack(side="left", padx=5, pady=5)
            
            # Entry
            entry = ctk.CTkEntry(field_frame, width=300, placeholder_text=description)
            entry.pack(side="right", padx=5, pady=5)
            entry.insert(0, self.word_data.get(field, ""))
            
            self.entries[field] = entry
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        # Save button
        save_btn = ctk.CTkButton(buttons_frame, text="Save", command=self.save_word, width=100)
        save_btn.pack(side="left", padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancel", command=self.cancel, width=100)
        cancel_btn.pack(side="right", padx=5)
        
        # Focus first entry
        if fields:
            self.entries[fields[0][0]].focus()
    
    def save_word(self):
        """Save the word data"""
        word_data = {}
        
        # Validate and collect data
        for field, entry in self.entries.items():
            value = entry.get().strip()
            if not value and field in ["German", "English"]:  # Required fields
                messagebox.showerror("Error", f"{field} is required!")
                entry.focus()
                return
            word_data[field] = value
        
        self.result = word_data
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result"""
        self.dialog.wait_window()
        return self.result


if __name__ == "__main__":
    app = VocabularyDatabaseEditor()
    app.run()

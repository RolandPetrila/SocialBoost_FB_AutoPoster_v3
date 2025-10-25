#!/usr/bin/env python3
"""
SocialBoost Facebook AutoPoster v3 - Main GUI Application
Tkinter-based GUI for managing Facebook automated posting and content generation.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import pathlib
from dotenv import load_dotenv
from queue import Queue
from typing import Optional, Dict, Any


class SocialBoostApp(tk.Tk):
    """Main application class for SocialBoost Facebook AutoPoster GUI."""
    
    def __init__(self) -> None:
        """Initialize the main application window."""
        super().__init__()
        
        # Load environment variables
        load_dotenv()
        
        # Set up project root path
        self.PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
        
        # Initialize GUI components
        self.setup_window()
        self.setup_notebook()
        self.setup_tabs()
        self.setup_queue()
        
    def setup_window(self) -> None:
        """Configure the main window properties."""
        self.title("SocialBoost Facebook AutoPoster v3")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Center the window
        self.center_window()
        
    def center_window(self) -> None:
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_notebook(self) -> None:
        """Create the main notebook widget for tabs."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
    def setup_tabs(self) -> None:
        """Create and configure all tabs."""
        # Create tab frames
        self.control_frame = ttk.Frame(self.notebook)
        self.schedule_frame = ttk.Frame(self.notebook)
        self.assets_frame = ttk.Frame(self.notebook)
        self.generate_frame = ttk.Frame(self.notebook)
        self.logs_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.control_frame, text="Control/Status")
        self.notebook.add(self.schedule_frame, text="Programare")
        self.notebook.add(self.assets_frame, text="Assets")
        self.notebook.add(self.generate_frame, text="Generare Text")
        self.notebook.add(self.logs_frame, text="Logs")
        
        # Setup individual tabs
        self.setup_control_tab()
        self.setup_schedule_tab()
        self.setup_assets_tab()
        self.setup_generate_tab()
        self.setup_logs_tab()
        
    def setup_control_tab(self) -> None:
        """Setup the Control/Status tab."""
        # Title
        title_label = ttk.Label(self.control_frame, text="Control Panel", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.control_frame, text="Status", padding=10)
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground='green')
        self.status_label.pack()
        
        # Action buttons frame
        actions_frame = ttk.LabelFrame(self.control_frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        # Test post button
        self.test_post_btn = ttk.Button(
            actions_frame, 
            text="Postează Text Test", 
            command=self.run_post_text
        )
        self.test_post_btn.pack(side='left', padx=5)
        
        # Generate test button
        self.test_generate_btn = ttk.Button(
            actions_frame, 
            text="Generează Text Test", 
            command=self.run_generate_text_test
        )
        self.test_generate_btn.pack(side='left', padx=5)
        
    def setup_schedule_tab(self) -> None:
        """Setup the Programare (Scheduling) tab."""
        title_label = ttk.Label(self.schedule_frame, text="Programare Postări", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        info_label = ttk.Label(
            self.schedule_frame, 
            text="Funcționalitatea de programare va fi implementată în versiunile viitoare.",
            foreground='gray'
        )
        info_label.pack(pady=20)
        
    def setup_assets_tab(self) -> None:
        """Setup the Assets tab."""
        title_label = ttk.Label(self.assets_frame, text="Gestionare Assets", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        info_label = ttk.Label(
            self.assets_frame, 
            text="Gestionarea imaginilor și videoclipurilor va fi implementată în versiunile viitoare.",
            foreground='gray'
        )
        info_label.pack(pady=20)
        
    def setup_generate_tab(self) -> None:
        """Setup the Generare Text tab."""
        title_label = ttk.Label(self.generate_frame, text="Generare Conținut AI", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.generate_frame, text="Prompt pentru Generare", padding=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Prompt input
        prompt_label = ttk.Label(input_frame, text="Introduceți promptul:")
        prompt_label.pack(anchor='w')
        
        self.prompt_text = scrolledtext.ScrolledText(input_frame, height=6, wrap=tk.WORD)
        self.prompt_text.pack(fill='both', expand=True, pady=5)
        
        # Generate button
        self.generate_btn = ttk.Button(
            input_frame, 
            text="Generează Text", 
            command=self.run_generate_text
        )
        self.generate_btn.pack(pady=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(self.generate_frame, text="Rezultat Generare", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Result display
        self.result_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD, state='disabled')
        self.result_text.pack(fill='both', expand=True)
        
    def setup_logs_tab(self) -> None:
        """Setup the Logs tab."""
        title_label = ttk.Label(self.logs_frame, text="Loguri Sistem", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Logs display
        logs_frame = ttk.LabelFrame(self.logs_frame, text="Loguri Recente", padding=10)
        logs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=15, wrap=tk.WORD, state='disabled')
        self.logs_text.pack(fill='both', expand=True)
        
        # Add some sample logs
        self.add_log("Aplicația SocialBoost a fost inițializată cu succes.")
        self.add_log("GUI-ul este gata pentru utilizare.")
        
    def setup_queue(self) -> None:
        """Setup the queue for thread-safe GUI updates."""
        self.queue: Queue[Dict[str, Any]] = Queue()
        self.check_queue()
        
    def check_queue(self) -> None:
        """Check for messages in the queue and update GUI accordingly."""
        try:
            while True:
                message = self.queue.get_nowait()
                self.handle_queue_message(message)
        except:
            pass
        finally:
            self.after(100, self.check_queue)
            
    def handle_queue_message(self, message: Dict[str, Any]) -> None:
        """Handle messages from the queue."""
        msg_type = message.get('type')
        
        if msg_type == 'status':
            self.status_label.config(text=message.get('text', ''), foreground=message.get('color', 'black'))
        elif msg_type == 'result':
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, message.get('text', ''))
            self.result_text.config(state='disabled')
        elif msg_type == 'log':
            self.add_log(message.get('text', ''))
        elif msg_type == 'error':
            messagebox.showerror("Eroare", message.get('text', 'A apărut o eroare necunoscută.'))
        elif msg_type == 'success':
            messagebox.showinfo("Succes", message.get('text', 'Operațiunea a fost finalizată cu succes.'))
            
    def add_log(self, message: str) -> None:
        """Add a log message to the logs tab."""
        self.logs_text.config(state='normal')
        self.logs_text.insert(tk.END, f"{message}\n")
        self.logs_text.see(tk.END)
        self.logs_text.config(state='disabled')
        
    def run_generate_text(self) -> None:
        """Run the text generation script in a separate thread."""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Avertisment", "Vă rugăm să introduceți un prompt.")
            return
            
        # Disable button during execution
        self.generate_btn.config(state='disabled')
        self.queue.put({'type': 'status', 'text': 'Se generează text...', 'color': 'blue'})
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_generate_text_thread, args=(prompt,))
        thread.daemon = True
        thread.start()
        
    def _run_generate_text_thread(self, prompt: str) -> None:
        """Thread function for running text generation."""
        try:
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "auto_generate.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Scriptul nu a fost găsit: {script_path}'})
                return
                
            # Run the script
            result = subprocess.run(
                [sys.executable, str(script_path), "--prompt", prompt],
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'result', 'text': result.stdout})
                self.queue.put({'type': 'success', 'text': 'Textul a fost generat cu succes!'})
                self.queue.put({'type': 'log', 'text': f'Generare text completată pentru prompt: {prompt[:50]}...'})
            else:
                error_msg = result.stderr or "Eroare necunoscută la generarea textului."
                self.queue.put({'type': 'error', 'text': error_msg})
                self.queue.put({'type': 'log', 'text': f'Eroare la generarea textului: {error_msg}'})
                
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Eroare la executarea scriptului: {str(e)}'})
            self.queue.put({'type': 'log', 'text': f'Eroare critică: {str(e)}'})
        finally:
            self.queue.put({'type': 'status', 'text': 'Ready', 'color': 'green'})
            self.after(0, lambda: self.generate_btn.config(state='normal'))
            
    def run_generate_text_test(self) -> None:
        """Run a test text generation with a predefined prompt."""
        test_prompt = "Generează un post Facebook despre importanța tehnologiei în viața de zi cu zi."
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(1.0, test_prompt)
        self.run_generate_text()
        
    def run_post_text(self) -> None:
        """Run the post text script in a separate thread."""
        # Disable button during execution
        self.test_post_btn.config(state='disabled')
        self.queue.put({'type': 'status', 'text': 'Se postează textul...', 'color': 'blue'})
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_post_text_thread)
        thread.daemon = True
        thread.start()
        
    def _run_post_text_thread(self) -> None:
        """Thread function for running text posting."""
        try:
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "auto_post.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Scriptul nu a fost găsit: {script_path}'})
                return
                
            # Run the script with test message
            test_message = "Mesaj test din GUI - SocialBoost Facebook AutoPoster v3"
            result = subprocess.run(
                [sys.executable, str(script_path), "--message", test_message],
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'success', 'text': 'Textul a fost postat cu succes pe Facebook!'})
                self.queue.put({'type': 'log', 'text': f'Postare completată: {test_message}'})
            else:
                error_msg = result.stderr or "Eroare necunoscută la postarea textului."
                self.queue.put({'type': 'error', 'text': error_msg})
                self.queue.put({'type': 'log', 'text': f'Eroare la postarea textului: {error_msg}'})
                
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Eroare la executarea scriptului: {str(e)}'})
            self.queue.put({'type': 'log', 'text': f'Eroare critică: {str(e)}'})
        finally:
            self.queue.put({'type': 'status', 'text': 'Ready', 'color': 'green'})
            self.after(0, lambda: self.test_post_btn.config(state='normal'))


def main() -> None:
    """Main entry point for the GUI application."""
    try:
        app = SocialBoostApp()
        app.mainloop()
    except Exception as e:
        print(f"Eroare la inițializarea aplicației: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

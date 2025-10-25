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
import json
from dotenv import load_dotenv
from queue import Queue
from typing import Optional, Dict, Any, List
from PIL import Image, ImageTk
import datetime


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
        
        # Initialize assets tracking
        self.assets_dict: Dict[str, str] = {}
        self.preview_image: Optional[ImageTk.PhotoImage] = None
        
    def setup_control_tab(self) -> None:
        """Setup the Control/Status tab."""
        # Title
        title_label = ttk.Label(self.control_frame, text="Control Panel", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Main container with two sections
        main_container = ttk.Frame(self.control_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left side - Status Information
        left_frame = ttk.LabelFrame(main_container, text="Project Status", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Project information labels
        self.project_name_label = ttk.Label(left_frame, text="Project: Loading...", font=('Arial', 10, 'bold'))
        self.project_name_label.pack(anchor='w', pady=2)
        
        self.current_stage_label = ttk.Label(left_frame, text="Stage: Loading...")
        self.current_stage_label.pack(anchor='w', pady=2)
        
        self.last_commit_label = ttk.Label(left_frame, text="Last Commit: Loading...")
        self.last_commit_label.pack(anchor='w', pady=2)
        
        self.last_run_label = ttk.Label(left_frame, text="Last Run: Loading...")
        self.last_run_label.pack(anchor='w', pady=2)
        
        # Health status
        self.health_status_label = ttk.Label(left_frame, text="Health: Unknown", font=('Arial', 10, 'bold'))
        self.health_status_label.pack(anchor='w', pady=(10, 2))
        
        self.health_score_label = ttk.Label(left_frame, text="Score: 0.00")
        self.health_score_label.pack(anchor='w', pady=2)
        
        # Refresh status button
        refresh_status_btn = ttk.Button(left_frame, text="Refresh Status", command=self.load_project_status_gui)
        refresh_status_btn.pack(pady=10)
        
        # Right side - Quick Actions
        right_frame = ttk.LabelFrame(main_container, text="Quick Actions", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Health check button
        self.health_check_btn = ttk.Button(
            right_frame, 
            text="Run Health Check", 
            command=self.run_health_check
        )
        self.health_check_btn.pack(fill='x', pady=5)
        
        # Backup button
        self.backup_btn = ttk.Button(
            right_frame, 
            text="Create Backup", 
            command=self.run_backup
        )
        self.backup_btn.pack(fill='x', pady=5)
        
        # Scheduler control buttons
        scheduler_frame = ttk.LabelFrame(right_frame, text="Scheduler Control", padding=5)
        scheduler_frame.pack(fill='x', pady=5)
        
        self.start_scheduler_btn = ttk.Button(
            scheduler_frame, 
            text="Start Scheduler", 
            command=self.start_scheduler
        )
        self.start_scheduler_btn.pack(fill='x', pady=2)
        
        self.stop_scheduler_btn = ttk.Button(
            scheduler_frame, 
            text="Stop Scheduler", 
            command=self.stop_scheduler,
            state='disabled'
        )
        self.stop_scheduler_btn.pack(fill='x', pady=2)
        
        # Test actions frame
        test_frame = ttk.LabelFrame(right_frame, text="Test Actions", padding=5)
        test_frame.pack(fill='x', pady=5)
        
        # Test post button
        self.test_post_btn = ttk.Button(
            test_frame, 
            text="Postează Text Test", 
            command=self.run_post_text
        )
        self.test_post_btn.pack(fill='x', pady=2)
        
        # Generate test button
        self.test_generate_btn = ttk.Button(
            test_frame, 
            text="Generează Text Test", 
            command=self.run_generate_text_test
        )
        self.test_generate_btn.pack(fill='x', pady=2)
        
        # Recent logs frame
        logs_frame = ttk.LabelFrame(self.control_frame, text="Recent Logs", padding=10)
        logs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Logs text widget
        logs_text_frame = ttk.Frame(logs_frame)
        logs_text_frame.pack(fill='both', expand=True)
        
        self.control_logs_text = tk.Text(
            logs_text_frame, 
            height=8, 
            wrap=tk.WORD, 
            state='disabled',
            font=('Consolas', 9), 
            bg='#f8f8f8'
        )
        logs_scrollbar = ttk.Scrollbar(logs_text_frame, orient='vertical', command=self.control_logs_text.yview)
        self.control_logs_text.configure(yscrollcommand=logs_scrollbar.set)
        
        self.control_logs_text.pack(side='left', fill='both', expand=True)
        logs_scrollbar.pack(side='right', fill='y')
        
        # Initialize running processes tracking
        self.running_processes: Dict[str, subprocess.Popen] = {}
        
        # Load initial status
        self.load_project_status_gui()
        self.load_recent_logs()
        
    def setup_schedule_tab(self) -> None:
        """Setup the Programare (Scheduling) tab."""
        title_label = ttk.Label(self.schedule_frame, text="Programare Postări", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Main container with two sections
        main_container = ttk.Frame(self.schedule_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left side - Job list
        left_frame = ttk.LabelFrame(main_container, text="Joburi Programate", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Treeview for jobs
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill='both', expand=True)
        
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        vsb.pack(side='right', fill='y')
        
        self.schedule_tree = ttk.Treeview(
            tree_frame,
            columns=('type', 'time', 'task', 'enabled', 'last_run'),
            show='tree headings',
            selectmode='browse',
            yscrollcommand=vsb.set
        )
        self.schedule_tree.heading('#0', text='#')
        self.schedule_tree.heading('type', text='Tip')
        self.schedule_tree.heading('time', text='Ora/Interval')
        self.schedule_tree.heading('task', text='Task')
        self.schedule_tree.heading('enabled', text='Activat')
        self.schedule_tree.heading('last_run', text='Ultima Rulare')
        
        self.schedule_tree.column('#0', width=30, anchor='center')
        self.schedule_tree.column('type', width=80, anchor='center')
        self.schedule_tree.column('time', width=120, anchor='center')
        self.schedule_tree.column('task', width=150, anchor='center')
        self.schedule_tree.column('enabled', width=70, anchor='center')
        self.schedule_tree.column('last_run', width=150, anchor='center')
        
        self.schedule_tree.pack(side='left', fill='both', expand=True)
        vsb.config(command=self.schedule_tree.yview)
        
        # Buttons frame
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        ttk.Button(buttons_frame, text="Refresh List", command=self.load_schedule_gui).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Delete Selected", command=self.delete_schedule_job).pack(side='left', padx=5)
        
        # Right side - Add new job
        right_frame = ttk.LabelFrame(main_container, text="Adăugare Job Nou", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Job type
        ttk.Label(right_frame, text="Tip Job:").grid(row=0, column=0, sticky='w', pady=5)
        self.job_type_var = tk.StringVar(value='daily')
        job_type_combo = ttk.Combobox(right_frame, textvariable=self.job_type_var, 
                                      values=['daily', 'weekly', 'interval', 'once'], state='readonly', width=30)
        job_type_combo.grid(row=0, column=1, pady=5, padx=5)
        job_type_combo.bind('<<ComboboxSelected>>', self.on_job_type_change)
        
        # Dynamic fields container
        self.dynamic_fields = ttk.Frame(right_frame)
        self.dynamic_fields.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Daily fields
        self.daily_time_label = ttk.Label(self.dynamic_fields, text="Ora (HH:MM):")
        self.daily_time_entry = ttk.Entry(self.dynamic_fields, width=30)
        
        # Weekly fields
        self.weekly_day_label = ttk.Label(self.dynamic_fields, text="Ziua:")
        self.weekly_day_var = tk.StringVar(value='monday')
        self.weekly_day_combo = ttk.Combobox(self.dynamic_fields, textvariable=self.weekly_day_var,
                                             values=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                                             state='readonly', width=27)
        self.weekly_time_label = ttk.Label(self.dynamic_fields, text="Ora (HH:MM):")
        self.weekly_time_entry = ttk.Entry(self.dynamic_fields, width=30)
        
        # Interval fields
        self.interval_minutes_label = ttk.Label(self.dynamic_fields, text="Interval (minute):")
        self.interval_minutes_entry = ttk.Entry(self.dynamic_fields, width=30)
        
        # Once fields
        self.once_datetime_label = ttk.Label(self.dynamic_fields, text="Data și Ora (YYYY-MM-DD HH:MM):")
        self.once_datetime_entry = ttk.Entry(self.dynamic_fields, width=30)
        
        # Task
        ttk.Label(right_frame, text="Task:").grid(row=2, column=0, sticky='w', pady=5)
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(right_frame, textvariable=self.task_var, width=30)
        task_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Enabled checkbox
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_frame, text="Activat", variable=self.enabled_var).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Add button
        ttk.Button(right_frame, text="Add Job", command=self.add_schedule_job).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Load initial data
        self.on_job_type_change(None)
        self.load_schedule_gui()
        
    def setup_assets_tab(self) -> None:
        """Setup the Assets tab."""
        title_label = ttk.Label(self.assets_frame, text="Gestionare Assets", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Main container
        main_container = ttk.Frame(self.assets_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left side - File listing
        left_frame = ttk.LabelFrame(main_container, text="Fișiere Disponibile", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Treeview for file listing
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal')
        hsb.pack(side='bottom', fill='x')
        
        # Treeview
        self.assets_tree = ttk.Treeview(
            tree_frame,
            columns=('type',),
            show='tree headings',
            selectmode='extended',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        self.assets_tree.heading('#0', text='Nume Fișier')
        self.assets_tree.heading('type', text='Tip')
        self.assets_tree.column('type', width=100, anchor='center')
        self.assets_tree.pack(side='left', fill='both', expand=True)
        
        vsb.config(command=self.assets_tree.yview)
        hsb.config(command=self.assets_tree.xview)
        
        # Bind selection event for preview
        self.assets_tree.bind('<<TreeviewSelect>>', self.on_asset_select)
        
        # Buttons frame
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        self.refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh List",
            command=self.load_assets
        )
        self.refresh_btn.pack(side='left', padx=5)
        
        self.save_selection_btn = ttk.Button(
            buttons_frame,
            text="Save Selection",
            command=self.save_selected_assets
        )
        self.save_selection_btn.pack(side='left', padx=5)
        
        self.post_selected_btn = ttk.Button(
            buttons_frame,
            text="Post Selected Assets",
            command=self.run_post_selected_assets
        )
        self.post_selected_btn.pack(side='left', padx=5)
        
        # Right side - Preview
        right_frame = ttk.LabelFrame(main_container, text="Preview Imagine", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        self.preview_label = ttk.Label(
            right_frame,
            text="Selectați o imagine pentru preview",
            foreground='gray'
        )
        self.preview_label.pack(pady=50)
        
        # Load assets on initialization
        self.load_assets()
        
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
        
        # Selected assets info label
        self.assets_info_label = ttk.Label(input_frame, text="Va genera text pentru 0 imagini și 0 video-uri selectate.", foreground='gray')
        self.assets_info_label.pack(anchor='w', pady=(0, 5))
        
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
        
        # Update assets info on initialization
        self.update_assets_info()
        
    def update_assets_info(self) -> None:
        """Update the assets info label with current selection."""
        try:
            selected_assets_path = self.PROJECT_ROOT / "selected_assets.json"
            if selected_assets_path.exists():
                with open(selected_assets_path, 'r', encoding='utf-8') as f:
                    selected_data = json.load(f)
                    images = selected_data.get('images', [])
                    videos = selected_data.get('videos', [])
                    
                    # Count image and video files
                    image_count = len(images)
                    video_count = len(videos)
                    
                    self.assets_info_label.config(
                        text=f"Va genera text pentru {image_count} imagini și {video_count} video-uri selectate.",
                        foreground='blue' if (image_count + video_count) > 0 else 'gray'
                    )
            else:
                self.assets_info_label.config(
                    text="Va genera text pentru 0 imagini și 0 video-uri selectate.",
                    foreground='gray'
                )
        except Exception:
            self.assets_info_label.config(
                text="Eroare la citirea selecției de asset-uri.",
                foreground='red'
            )
        
    def setup_logs_tab(self) -> None:
        """Setup the Logs tab."""
        title_label = ttk.Label(self.logs_frame, text="Loguri Sistem", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Control frame for refresh button
        control_frame = ttk.Frame(self.logs_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        refresh_button = ttk.Button(control_frame, text="Refresh Logs", command=self.load_logs)
        refresh_button.pack(side='left', padx=(0, 10))
        
        # Log file path label
        self.log_file_path = self.PROJECT_ROOT / "Logs" / "system.log"
        self.log_path_label = ttk.Label(control_frame, text=f"Log file: {self.log_file_path.name}")
        self.log_path_label.pack(side='left')
        
        # Logs display
        logs_frame = ttk.LabelFrame(self.logs_frame, text="Loguri Recente", padding=10)
        logs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(logs_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.logs_text = tk.Text(text_frame, height=15, wrap=tk.WORD, state='disabled', 
                                font=('Consolas', 9), bg='#f8f8f8')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=scrollbar.set)
        
        self.logs_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initialize logs
        self.load_logs()
        
        # Start auto-refresh
        self.schedule_log_refresh()
        
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
            # Update control tab status if it exists
            if hasattr(self, 'health_status_label'):
                self.health_status_label.config(text=f"Status: {message.get('text', '')}", foreground=message.get('color', 'black'))
        elif msg_type == 'result':
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, message.get('text', ''))
            self.result_text.config(state='disabled')
        elif msg_type == 'log':
            self.add_log(message.get('text', ''))
            # Also add to control tab logs
            if hasattr(self, 'control_logs_text'):
                self.add_control_log(message.get('text', ''))
        elif msg_type == 'error':
            messagebox.showerror("Eroare", message.get('text', 'A apărut o eroare necunoscută.'))
        elif msg_type == 'success':
            messagebox.showinfo("Succes", message.get('text', 'Operațiunea a fost finalizată cu succes.'))
    
    def load_project_status_gui(self) -> None:
        """Load project status from PROJECT_CONTEXT.json and health check results."""
        try:
            # Load PROJECT_CONTEXT.json
            context_path = self.PROJECT_ROOT / "PROJECT_CONTEXT.json"
            if context_path.exists():
                with open(context_path, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
                
                self.project_name_label.config(text=f"Project: {context_data.get('project_name', 'Unknown')}")
                self.current_stage_label.config(text=f"Stage: {context_data.get('current_stage', 'Unknown')}")
                self.last_commit_label.config(text=f"Last Commit: {context_data.get('last_commit', 'Unknown')}")
                self.last_run_label.config(text=f"Last Run: {context_data.get('last_run', 'Unknown')}")
            else:
                self.project_name_label.config(text="Project: PROJECT_CONTEXT.json not found")
                self.current_stage_label.config(text="Stage: Unknown")
                self.last_commit_label.config(text="Last Commit: Unknown")
                self.last_run_label.config(text="Last Run: Unknown")
            
            # Load health check results
            health_path = self.PROJECT_ROOT / "Logs" / "health_check.json"
            if health_path.exists():
                with open(health_path, 'r', encoding='utf-8') as f:
                    health_data = json.load(f)
                
                overall_health = health_data.get('overall_health', 'Unknown')
                health_score = health_data.get('health_score', 0.0)
                
                # Set color based on health status
                color = 'green' if overall_health == 'Healthy' else 'orange' if overall_health == 'Degraded' else 'red'
                
                self.health_status_label.config(text=f"Health: {overall_health}", foreground=color)
                self.health_score_label.config(text=f"Score: {health_score:.2f}")
            else:
                self.health_status_label.config(text="Health: No health check data", foreground='gray')
                self.health_score_label.config(text="Score: N/A")
                
        except Exception as e:
            self.project_name_label.config(text=f"Error loading status: {str(e)}")
            self.health_status_label.config(text="Health: Error loading data", foreground='red')
    
    def load_recent_logs(self) -> None:
        """Load recent logs into the control tab logs widget."""
        try:
            self.control_logs_text.config(state='normal')
            self.control_logs_text.delete('1.0', tk.END)
            
            log_file_path = self.PROJECT_ROOT / "Logs" / "system.log"
            if log_file_path.exists():
                with open(log_file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                # Get last 20 lines
                lines = content.split('\n')
                if len(lines) > 20:
                    content = '\n'.join(lines[-20:])
                
                self.control_logs_text.insert(tk.END, content)
            else:
                self.control_logs_text.insert(tk.END, "No system log file found.")
            
            self.control_logs_text.see(tk.END)
            
        except Exception as e:
            self.control_logs_text.insert(tk.END, f"Error loading logs: {str(e)}")
        finally:
            self.control_logs_text.config(state='disabled')
    
    def add_control_log(self, message: str) -> None:
        """Add a log message to the control tab logs."""
        try:
            self.control_logs_text.config(state='normal')
            self.control_logs_text.insert(tk.END, f"{message}\n")
            self.control_logs_text.see(tk.END)
        finally:
            self.control_logs_text.config(state='disabled')
    
    def run_health_check(self) -> None:
        """Run health check script in a separate thread."""
        self.health_check_btn.config(state='disabled')
        self.queue.put({'type': 'log', 'text': 'Starting health check...'})
        
        thread = threading.Thread(target=self._run_health_check_thread)
        thread.daemon = True
        thread.start()
    
    def _run_health_check_thread(self) -> None:
        """Thread function for running health check."""
        try:
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "health_check.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Health check script not found: {script_path}'})
                return
            
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'success', 'text': 'Health check completed successfully!'})
                self.queue.put({'type': 'log', 'text': 'Health check completed - see Logs/health_check.json for details'})
                # Refresh status after health check
                self.after(0, self.load_project_status_gui)
            else:
                error_msg = result.stderr or "Unknown error during health check"
                self.queue.put({'type': 'error', 'text': f'Health check failed: {error_msg}'})
                self.queue.put({'type': 'log', 'text': f'Health check error: {error_msg}'})
                
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Error running health check: {str(e)}'})
            self.queue.put({'type': 'log', 'text': f'Health check exception: {str(e)}'})
        finally:
            self.after(0, lambda: self.health_check_btn.config(state='normal'))
    
    def run_backup(self) -> None:
        """Run backup script in a separate thread."""
        self.backup_btn.config(state='disabled')
        self.queue.put({'type': 'log', 'text': 'Starting backup...'})
        
        thread = threading.Thread(target=self._run_backup_thread)
        thread.daemon = True
        thread.start()
    
    def _run_backup_thread(self) -> None:
        """Thread function for running backup."""
        try:
            script_path = self.PROJECT_ROOT / "backup_manager.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Backup script not found: {script_path}'})
                return
            
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'success', 'text': 'Backup created successfully!'})
                self.queue.put({'type': 'log', 'text': 'Backup completed successfully'})
            else:
                error_msg = result.stderr or "Unknown error during backup"
                self.queue.put({'type': 'error', 'text': f'Backup failed: {error_msg}'})
                self.queue.put({'type': 'log', 'text': f'Backup error: {error_msg}'})
                
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Error running backup: {str(e)}'})
            self.queue.put({'type': 'log', 'text': f'Backup exception: {str(e)}'})
        finally:
            self.after(0, lambda: self.backup_btn.config(state='normal'))
    
    def start_scheduler(self) -> None:
        """Start the scheduler process."""
        try:
            # Check if scheduler is already running
            if 'scheduler' in self.running_processes:
                process = self.running_processes['scheduler']
                if process.poll() is None:  # Process is still running
                    messagebox.showwarning("Warning", "Scheduler is already running!")
                    return
            
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "scheduler.py"
            
            if not script_path.exists():
                messagebox.showerror("Error", f"Scheduler script not found: {script_path}")
                return
            
            # Start scheduler process
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                cwd=str(self.PROJECT_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_processes['scheduler'] = process
            
            # Update button states
            self.start_scheduler_btn.config(state='disabled')
            self.stop_scheduler_btn.config(state='normal')
            
            self.queue.put({'type': 'success', 'text': 'Scheduler started successfully!'})
            self.queue.put({'type': 'log', 'text': f'Scheduler started with PID: {process.pid}'})
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scheduler: {str(e)}")
            self.queue.put({'type': 'log', 'text': f'Scheduler start error: {str(e)}'})
    
    def stop_scheduler(self) -> None:
        """Stop the scheduler process."""
        try:
            if 'scheduler' not in self.running_processes:
                messagebox.showwarning("Warning", "No scheduler process found!")
                return
            
            process = self.running_processes['scheduler']
            
            if process.poll() is None:  # Process is still running
                # Try graceful termination first
                process.terminate()
                
                # Wait a bit for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful termination failed
                    process.kill()
                    process.wait()
                
                self.queue.put({'type': 'success', 'text': 'Scheduler stopped successfully!'})
                self.queue.put({'type': 'log', 'text': 'Scheduler stopped'})
            else:
                self.queue.put({'type': 'log', 'text': 'Scheduler was not running'})
            
            # Remove from tracking
            del self.running_processes['scheduler']
            
            # Update button states
            self.start_scheduler_btn.config(state='normal')
            self.stop_scheduler_btn.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop scheduler: {str(e)}")
            self.queue.put({'type': 'log', 'text': f'Scheduler stop error: {str(e)}'})
            
    def load_logs(self) -> None:
        """Load log content from the log file."""
        try:
            # Enable text widget for editing
            self.logs_text.config(state='normal')
            
            # Clear current content
            self.logs_text.delete('1.0', tk.END)
            
            # Check if log file exists
            if not self.log_file_path.exists():
                # Create a sample log file if it doesn't exist
                self.create_sample_log()
            
            # Read log file content
            try:
                with open(self.log_file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    
                # If file is too large, read only last 1000 lines
                lines = content.split('\n')
                if len(lines) > 1000:
                    content = '\n'.join(lines[-1000:])
                    content = f"... (showing last 1000 lines)\n{content}"
                
                # Insert content
                self.logs_text.insert(tk.END, content)
                
            except FileNotFoundError:
                self.logs_text.insert(tk.END, f"Log file not found: {self.log_file_path}\n")
            except Exception as e:
                self.logs_text.insert(tk.END, f"Error reading log file: {str(e)}\n")
            
            # Auto-scroll to end
            self.logs_text.see(tk.END)
            
        except Exception as e:
            # Fallback error handling
            self.logs_text.insert(tk.END, f"Error loading logs: {str(e)}\n")
        finally:
            # Disable text widget
            self.logs_text.config(state='disabled')
    
    def create_sample_log(self) -> None:
        """Create a sample log file if it doesn't exist."""
        try:
            # Ensure Logs directory exists
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create sample log content
            sample_content = f"""2025-10-25 20:00:00 - SocialBoost - INFO - Application started
2025-10-25 20:00:01 - SocialBoost - INFO - GUI initialized successfully
2025-10-25 20:00:02 - SocialBoost - INFO - Logs tab loaded
2025-10-25 20:00:03 - SocialBoost - INFO - Auto-refresh enabled
"""
            
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                f.write(sample_content)
                
        except Exception as e:
            print(f"Error creating sample log: {e}")
    
    def schedule_log_refresh(self) -> None:
        """Schedule the next log refresh."""
        self.load_logs()
        # Schedule next refresh in 5 seconds
        self.after(5000, self.schedule_log_refresh)
    
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
        
        # Read selected assets from selected_assets.json
        selected_assets_path = self.PROJECT_ROOT / "selected_assets.json"
        selected_paths = []
        
        try:
            if selected_assets_path.exists():
                with open(selected_assets_path, 'r', encoding='utf-8') as f:
                    selected_data = json.load(f)
                    # Combine images and videos lists
                    images = selected_data.get('images', [])
                    videos = selected_data.get('videos', [])
                    selected_paths = images + videos
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Eroare la citirea selected_assets.json: {str(e)}'})
            return
        
        # Check if any assets are selected
        if not selected_paths:
            messagebox.showwarning("Avertisment", "Niciun asset selectat în tab-ul Assets!")
            return
            
        # Disable button during execution
        self.generate_btn.config(state='disabled')
        self.queue.put({'type': 'status', 'text': f'Se generează text pentru {len(selected_paths)} asset-uri...', 'color': 'blue'})
        
        # Run in separate thread
        thread = threading.Thread(target=self._run_generate_text_thread, args=(prompt, selected_paths))
        thread.daemon = True
        thread.start()
        
    def _run_generate_text_thread(self, prompt: str, selected_paths: List[str]) -> None:
        """Thread function for running text generation."""
        try:
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "auto_generate.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Scriptul nu a fost găsit: {script_path}'})
                return
            
            # Build command arguments
            args = [sys.executable, str(script_path), "--prompt", prompt, "--assets"] + selected_paths
            
            # Run the script
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'result', 'text': result.stdout})
                self.queue.put({'type': 'success', 'text': f'Textul a fost generat cu succes pentru {len(selected_paths)} asset-uri!'})
                self.queue.put({'type': 'log', 'text': f'Generare text completată pentru {len(selected_paths)} asset-uri cu prompt: {prompt[:50]}...'})
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
    
    def load_assets(self) -> None:
        """Load assets from Assets/Images and Assets/Videos folders."""
        # Clear existing items
        for item in self.assets_tree.get_children():
            self.assets_tree.delete(item)
        self.assets_dict.clear()
        
        # Define asset directories
        images_dir = self.PROJECT_ROOT / "Assets" / "Images"
        videos_dir = self.PROJECT_ROOT / "Assets" / "Videos"
        
        # Image extensions
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        # Video extensions
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        
        # Scan Images folder
        if images_dir.exists():
            for ext in image_extensions:
                for file_path in images_dir.glob(f"*{ext}"):
                    if file_path.is_file():
                        file_name = file_path.name
                        absolute_path = str(file_path.resolve())
                        item_id = self.assets_tree.insert('', 'end', text=file_name, values=('Imagine',))
                        self.assets_dict[item_id] = absolute_path
        
        # Scan Videos folder
        if videos_dir.exists():
            for ext in video_extensions:
                for file_path in videos_dir.glob(f"*{ext}"):
                    if file_path.is_file():
                        file_name = file_path.name
                        absolute_path = str(file_path.resolve())
                        item_id = self.assets_tree.insert('', 'end', text=file_name, values=('Video',))
                        self.assets_dict[item_id] = absolute_path
    
    def on_asset_select(self, event: Any) -> None:
        """Handle asset selection for preview."""
        selected_items = self.assets_tree.selection()
        
        if not selected_items:
            return
        
        # Only show preview for single image selection
        if len(selected_items) != 1:
            self.preview_label.config(text="Selectați o imagine pentru preview", foreground='gray')
            self.preview_image = None
            return
        
        item_id = selected_items[0]
        file_path = self.assets_dict.get(item_id)
        
        if not file_path:
            return
        
        # Check if it's an image
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        if not any(file_path.lower().endswith(ext) for ext in image_extensions):
            self.preview_label.config(text="Preview disponibil doar pentru imagini", foreground='gray')
            self.preview_image = None
            return
        
        # Load and display image
        try:
            img = Image.open(file_path)
            
            # Resize while maintaining aspect ratio
            max_size = 300
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(img)
            
            # Update preview label
            self.preview_label.config(image=self.preview_image, text='')
            
        except Exception as e:
            self.preview_label.config(
                text=f"Eroare la încărcarea imaginii:\n{str(e)}",
                foreground='red',
                image=''
            )
            self.preview_image = None
    
    def save_selected_assets(self) -> None:
        """Save selected assets to selected_assets.json."""
        selected_items = self.assets_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Avertisment", "Vă rugăm să selectați cel puțin un fișier.")
            return
        
        # Separate images and videos
        selected_images: List[str] = []
        selected_videos: List[str] = []
        
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        
        for item_id in selected_items:
            file_path = self.assets_dict.get(item_id)
            if not file_path:
                continue
            
            file_path_lower = file_path.lower()
            if any(file_path_lower.endswith(ext) for ext in image_extensions):
                selected_images.append(file_path)
            elif any(file_path_lower.endswith(ext) for ext in video_extensions):
                selected_videos.append(file_path)
        
        # Create data dictionary
        data = {
            "images": selected_images,
            "videos": selected_videos
        }
        
        # Write to JSON file
        json_path = self.PROJECT_ROOT / "selected_assets.json"
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            total = len(selected_images) + len(selected_videos)
            messagebox.showinfo(
                "Succes",
                f"Selecția a fost salvată!\n{len(selected_images)} imagini, {len(selected_videos)} videoclipuri"
            )
            self.add_log(f"Assets salvate: {total} fișiere în selected_assets.json")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvarea selecției:\n{str(e)}")
            self.add_log(f"Eroare la salvarea assets: {str(e)}")
    
    def run_post_selected_assets(self) -> None:
        """Run posting of selected assets in a separate thread."""
        # Check if selected_assets.json exists and has content
        json_path = self.PROJECT_ROOT / "selected_assets.json"
        
        try:
            if not json_path.exists():
                messagebox.showwarning("Avertisment", "Nu există fișierul selected_assets.json. Vă rugăm să salvați mai întâi o selecție.")
                return
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            images = data.get('images', [])
            videos = data.get('videos', [])
            total_assets = len(images) + len(videos)
            
            if total_assets == 0:
                messagebox.showwarning("Avertisment", "Nu există asset-uri selectate în selected_assets.json.")
                return
            
            # Confirm posting
            confirm_msg = f"Postați {len(images)} imagini și {len(videos)} videoclipuri?"
            if not messagebox.askyesno("Confirmare", confirm_msg):
                return
            
            # Disable button during execution
            self.post_selected_btn.config(state='disabled')
            self.queue.put({'type': 'status', 'text': 'Se postează asset-urile selectate...', 'color': 'blue'})
            
            # Run in separate thread
            thread = threading.Thread(target=self._run_post_selected_assets_thread)
            thread.daemon = True
            thread.start()
            
        except json.JSONDecodeError:
            messagebox.showerror("Eroare", "Fișierul selected_assets.json este corupt.")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la citirea selected_assets.json:\n{str(e)}")
    
    def _run_post_selected_assets_thread(self) -> None:
        """Thread function for posting selected assets."""
        try:
            script_path = self.PROJECT_ROOT / "Automatizare_Completa" / "auto_post.py"
            
            if not script_path.exists():
                self.queue.put({'type': 'error', 'text': f'Scriptul nu a fost găsit: {script_path}'})
                return
            
            # Run the script with --selected-only flag
            result = subprocess.run(
                [sys.executable, str(script_path), "--selected-only"],
                capture_output=True,
                text=True,
                cwd=str(self.PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                self.queue.put({'type': 'success', 'text': 'Asset-urile selectate au fost postate cu succes!'})
                self.queue.put({'type': 'log', 'text': 'Postare asset-uri selectate completată'})
                self.queue.put({'type': 'log', 'text': result.stdout})
            else:
                error_msg = result.stderr or "Eroare necunoscută la postarea asset-urilor."
                self.queue.put({'type': 'error', 'text': error_msg})
                self.queue.put({'type': 'log', 'text': f'Eroare la postarea asset-urilor: {error_msg}'})
                if result.stdout:
                    self.queue.put({'type': 'log', 'text': result.stdout})
                
        except Exception as e:
            self.queue.put({'type': 'error', 'text': f'Eroare la executarea scriptului: {str(e)}'})
            self.queue.put({'type': 'log', 'text': f'Eroare critică: {str(e)}'})
        finally:
            self.queue.put({'type': 'status', 'text': 'Ready', 'color': 'green'})
            self.after(0, lambda: self.post_selected_btn.config(state='normal'))
    
    def on_job_type_change(self, event: Any) -> None:
        """Handle job type selection change to show/hide relevant fields."""
        # Clear all dynamic fields
        for widget in self.dynamic_fields.winfo_children():
            widget.grid_remove()
        
        job_type = self.job_type_var.get()
        
        if job_type == 'daily':
            self.daily_time_label.grid(row=0, column=0, sticky='w', pady=5)
            self.daily_time_entry.grid(row=0, column=1, pady=5, padx=5)
        elif job_type == 'weekly':
            self.weekly_day_label.grid(row=0, column=0, sticky='w', pady=5)
            self.weekly_day_combo.grid(row=0, column=1, pady=5, padx=5)
            self.weekly_time_label.grid(row=1, column=0, sticky='w', pady=5)
            self.weekly_time_entry.grid(row=1, column=1, pady=5, padx=5)
        elif job_type == 'interval':
            self.interval_minutes_label.grid(row=0, column=0, sticky='w', pady=5)
            self.interval_minutes_entry.grid(row=0, column=1, pady=5, padx=5)
        elif job_type == 'once':
            self.once_datetime_label.grid(row=0, column=0, sticky='w', pady=5)
            self.once_datetime_entry.grid(row=0, column=1, pady=5, padx=5)
    
    def load_schedule_gui(self) -> None:
        """Load schedule jobs from Config/schedule.json and populate treeview."""
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        schedule_path = self.PROJECT_ROOT / "Config" / "schedule.json"
        
        try:
            if not schedule_path.exists():
                self.add_log("Fișierul schedule.json nu a fost găsit.")
                return
            
            with open(schedule_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            jobs = data.get('jobs', [])
            
            for idx, job in enumerate(jobs, start=1):
                job_type = job.get('type', '')
                task = job.get('task', '')
                enabled = 'Da' if job.get('enabled', False) else 'Nu'
                last_run = job.get('last_run') or 'Niciodată'
                
                # Format time/interval based on job type
                time_display = ''
                if job_type == 'daily':
                    time_display = job.get('time', '')
                elif job_type == 'weekly':
                    time_display = f"{job.get('day', '')} {job.get('time', '')}"
                elif job_type == 'interval':
                    time_display = f"{job.get('every_minutes', 0)} min"
                elif job_type == 'once':
                    time_display = job.get('run_at_datetime', '')
                
                self.schedule_tree.insert('', 'end', text=str(idx), values=(job_type, time_display, task, enabled, last_run))
            
            self.add_log(f"Încărcate {len(jobs)} joburi din schedule.json")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Eroare", f"Eroare la citirea fișierului JSON: {str(e)}")
            self.add_log(f"Eroare JSON: {str(e)}")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea programării: {str(e)}")
            self.add_log(f"Eroare la încărcarea programării: {str(e)}")
    
    def add_schedule_job(self) -> None:
        """Add a new schedule job."""
        job_type = self.job_type_var.get()
        task = self.task_var.get().strip()
        enabled = self.enabled_var.get()
        
        # Validate task
        if not task:
            messagebox.showerror("Eroare", "Vă rugăm să introduceți numele task-ului.")
            return
        
        # Validate task file exists
        task_path = self.PROJECT_ROOT / "Automatizare_Completa" / task
        if not task_path.exists():
            messagebox.showerror("Eroare", f"Fișierul task nu există: {task}")
            return
        
        # Build job based on type
        job: Dict[str, Any] = {
            'type': job_type,
            'task': task,
            'enabled': enabled,
            'last_run': None
        }
        
        # Add type-specific fields
        if job_type == 'daily':
            time_str = self.daily_time_entry.get().strip()
            if not time_str:
                messagebox.showerror("Eroare", "Vă rugăm să introduceți ora (HH:MM).")
                return
            # Validate time format
            try:
                parts = time_str.split(':')
                if len(parts) != 2 or int(parts[0]) < 0 or int(parts[0]) > 23 or int(parts[1]) < 0 or int(parts[1]) > 59:
                    raise ValueError()
            except (ValueError, IndexError):
                messagebox.showerror("Eroare", "Format oră invalid. Folosiți HH:MM.")
                return
            job['time'] = time_str
        
        elif job_type == 'weekly':
            day = self.weekly_day_var.get()
            time_str = self.weekly_time_entry.get().strip()
            if not time_str:
                messagebox.showerror("Eroare", "Vă rugăm să introduceți ora (HH:MM).")
                return
            try:
                parts = time_str.split(':')
                if len(parts) != 2 or int(parts[0]) < 0 or int(parts[0]) > 23 or int(parts[1]) < 0 or int(parts[1]) > 59:
                    raise ValueError()
            except (ValueError, IndexError):
                messagebox.showerror("Eroare", "Format oră invalid. Folosiți HH:MM.")
                return
            job['day'] = day
            job['time'] = time_str
        
        elif job_type == 'interval':
            minutes_str = self.interval_minutes_entry.get().strip()
            if not minutes_str:
                messagebox.showerror("Eroare", "Vă rugăm să introduceți intervalul în minute.")
                return
            try:
                minutes = int(minutes_str)
                if minutes <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Eroare", "Intervalul trebuie să fie un număr pozitiv.")
                return
            job['every_minutes'] = minutes
        
        elif job_type == 'once':
            datetime_str = self.once_datetime_entry.get().strip()
            if not datetime_str:
                messagebox.showerror("Eroare", "Vă rugăm să introduceți data și ora (YYYY-MM-DD HH:MM).")
                return
            # Basic validation
            try:
                datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            except ValueError:
                messagebox.showerror("Eroare", "Format invalid. Folosiți YYYY-MM-DD HH:MM.")
                return
            job['run_at_datetime'] = datetime_str
            job['executed'] = False
        
        # Load current schedule
        schedule_path = self.PROJECT_ROOT / "Config" / "schedule.json"
        try:
            if schedule_path.exists():
                with open(schedule_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'jobs': []}
            
            # Add new job
            data['jobs'].append(job)
            
            # Save updated schedule
            with open(schedule_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Succes", "Job-ul a fost adăugat cu succes!")
            self.add_log(f"Job adăugat: {job_type} - {task}")
            
            # Refresh list
            self.load_schedule_gui()
            
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvarea jobului: {str(e)}")
            self.add_log(f"Eroare la adăugarea jobului: {str(e)}")
    
    def delete_schedule_job(self) -> None:
        """Delete selected schedule job."""
        selected_item = self.schedule_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Avertisment", "Vă rugăm să selectați un job pentru ștergere.")
            return
        
        # Get job index from treeview
        item_index = int(self.schedule_tree.item(selected_item[0], 'text')) - 1
        
        # Confirm deletion
        if not messagebox.askyesno("Confirmare", "Sigur doriți să ștergeți acest job?"):
            return
        
        # Load current schedule
        schedule_path = self.PROJECT_ROOT / "Config" / "schedule.json"
        
        try:
            with open(schedule_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Remove job
            if 0 <= item_index < len(data['jobs']):
                del data['jobs'][item_index]
                
                # Save updated schedule
                with open(schedule_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Succes", "Job-ul a fost șters cu succes!")
                self.add_log(f"Job șters: index {item_index}")
                
                # Refresh list
                self.load_schedule_gui()
            else:
                messagebox.showerror("Eroare", "Index job invalid.")
                
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la ștergerea jobului: {str(e)}")
            self.add_log(f"Eroare la ștergerea jobului: {str(e)}")


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

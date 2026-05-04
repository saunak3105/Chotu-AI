import customtkinter as ctk
import threading
from speech.stt import listen
from nlp.intent_parser import process_text
from utils.logger import get_logger

logger = get_logger(__name__)

class VoicePanel(ctk.CTkFrame):
    def __init__(self, master, on_command_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.on_command = on_command_callback
        
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="Voice Control Center", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)
        
        # Status Indicator
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.status_label.grid(row=1, column=0, padx=20, pady=5)
        
        # Mic Button
        self.mic_button = ctk.CTkButton(self, text="🎤 Start Listening", command=self.start_listening_thread, height=50)
        self.mic_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Manual Input
        self.entry = ctk.CTkEntry(self, placeholder_text="Or type command here (e.g. 'Add 5 milk')")
        self.entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.process_manual_input())
        
        self.submit_btn = ctk.CTkButton(self, text="Execute", command=self.process_manual_input)
        self.submit_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def set_status(self, text, color=None):
        self.status_label.configure(text=text)
        if color:
            self.status_label.configure(text_color=color)

    def start_listening_thread(self):
        self.mic_button.configure(state="disabled", text="👂 Listening...")
        self.set_status("Listening to your voice...", "#3498db")
        threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        try:
            from core.inventory import list_inventory
            # Get current items for grammar
            items = [item[0] for item in list_inventory()]
            
            text = listen(item_list=items)
            if text:
                self.master.after(0, lambda: self.set_status(f"Processing: '{text}'", "#f39c12"))
                data = process_text(text)
                self.master.after(0, lambda: self.on_command(data))
            else:
                self.master.after(0, lambda: self.set_status("No speech detected", "#e74c3c"))
        except Exception as e:
            logger.error(f"Voice panel error: {e}")
            self.master.after(0, lambda: self.set_status("Voice Error", "#e74c3c"))
        finally:
            self.master.after(0, self.reset_button)

    def reset_button(self):
        self.mic_button.configure(state="normal", text="🎤 Start Listening")
        self.set_status("Ready", "#2ecc71")

    def process_manual_input(self):
        text = self.entry.get()
        if text:
            self.entry.delete(0, 'end')
            data = process_text(text)
            self.on_command(data)

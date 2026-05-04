import customtkinter as ctk
from core.inventory import list_inventory, add_item, update_stock
from utils.constants import LOW_STOCK_THRESHOLD
from tkinter import messagebox

# Match dashboard theme
COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#10b981",
    "text": "#f8fafc",
    "subtext": "#94a3b8",
    "danger": "#ef4444"
}

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], **kwargs)
        
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # --- LEFT PANEL: ADD/UPDATE FORM ---
        self.form_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color="#334155")
        self.form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.form_frame, text="📦 Manage Item", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLORS["text"]).pack(pady=20)
        
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Item Name", height=40, fg_color="#0f172a")
        self.name_entry.pack(padx=20, pady=10, fill="x")
        
        self.price_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Price (₹)", height=40, fg_color="#0f172a")
        self.price_entry.pack(padx=20, pady=10, fill="x")
        
        self.stock_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Stock Quantity", height=40, fg_color="#0f172a")
        self.stock_entry.pack(padx=20, pady=10, fill="x")
        
        self.save_btn = ctk.CTkButton(self.form_frame, text="Update Inventory", height=45, command=self.save_item_action, fg_color=COLORS["accent"], font=ctk.CTkFont(weight="bold"))
        self.save_btn.pack(padx=20, pady=20, fill="x")
        
        # Divider
        ctk.CTkFrame(self.form_frame, height=2, fg_color="#334155").pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(self.form_frame, text="Quick Adjust Stock", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["subtext"]).pack(pady=(20, 10))
        self.adjust_name = ctk.CTkEntry(self.form_frame, placeholder_text="Enter Name", height=40, fg_color="#0f172a")
        self.adjust_name.pack(padx=20, pady=5, fill="x")
        
        btn_row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_row.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_row, text="+10", width=60, command=lambda: self.quick_adjust(10), fg_color="#334155").pack(side="left", expand=True, padx=2)
        ctk.CTkButton(btn_row, text="-10", width=60, command=lambda: self.quick_adjust(-10), fg_color="#334155").pack(side="left", expand=True, padx=2)

        # --- RIGHT PANEL: INVENTORY TABLE ---
        self.table_container = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color="#334155")
        self.table_container.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(self.table_container, text="Stock Overview", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLORS["text"]).grid(row=0, column=0, pady=20)
        
        self.scrollable_table = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scrollable_table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.scrollable_table.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.refresh()

    def refresh(self):
        for widget in self.scrollable_table.winfo_children(): widget.destroy()
        
        # Headers
        headers = ["ITEM NAME", "UNIT PRICE", "STOCK"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.scrollable_table, text=h, font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["subtext"]).grid(row=0, column=i, pady=10)
            
        items = list_inventory()
        for r, (name, price, stock) in enumerate(items, start=1):
            color = COLORS["danger"] if stock <= LOW_STOCK_THRESHOLD else COLORS["text"]
            
            ctk.CTkLabel(self.scrollable_table, text=name.upper(), text_color=color, font=ctk.CTkFont(size=13)).grid(row=r, column=0, pady=8)
            ctk.CTkLabel(self.scrollable_table, text=f"₹{price:.2f}", text_color=color, font=ctk.CTkFont(size=13)).grid(row=r, column=1, pady=8)
            ctk.CTkLabel(self.scrollable_table, text=str(stock), text_color=color, font=ctk.CTkFont(size=13, weight="bold")).grid(row=r, column=2, pady=8)

    def save_item_action(self):
        name = self.name_entry.get().strip().lower()
        price = self.price_entry.get().strip()
        stock = self.stock_entry.get().strip()
        
        if not name or not price or not stock:
            messagebox.showwarning("Incomplete Form", "Please fill all fields to update inventory.")
            return
            
        try:
            add_item(name, float(price), int(stock))
            self.name_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            self.stock_entry.delete(0, 'end')
            self.refresh()
            if hasattr(self.master.master.master, 'update_all_views'):
                self.master.master.master.update_all_views()
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and stock must be a whole number.")

    def quick_adjust(self, amount):
        name = self.adjust_name.get().strip().lower()
        if not name:
            messagebox.showwarning("Item Missing", "Enter item name to adjust stock.")
            return
            
        if update_stock(name, amount):
            self.refresh()
            if hasattr(self.master.master.master, 'update_all_views'):
                self.master.master.master.update_all_views()
        else:
            messagebox.showerror("Stock Error", f"Insufficient stock or item '{name}' not found.")

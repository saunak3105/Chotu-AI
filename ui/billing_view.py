import customtkinter as ctk
from core.inventory import get_item_price, get_stock
from core.billing import create_bill
from tkinter import messagebox

COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#10b981",
    "text": "#f8fafc",
    "subtext": "#94a3b8",
    "danger": "#ef4444"
}

class BillingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], **kwargs)
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.current_bill_items = []

        # --- LEFT: POS FORM ---
        self.pos_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color="#334155")
        self.pos_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.pos_frame, text="🛒 Quick Billing", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        input_row = ctk.CTkFrame(self.pos_frame, fg_color="transparent")
        input_row.pack(padx=20, pady=10, fill="x")
        
        self.item_name_entry = ctk.CTkEntry(input_row, placeholder_text="Item Name", height=45, fg_color="#0f172a")
        self.item_name_entry.pack(side="left", padx=5, expand=True, fill="x")
        
        self.item_qty_entry = ctk.CTkEntry(input_row, placeholder_text="Qty", width=80, height=45, fg_color="#0f172a")
        self.item_qty_entry.pack(side="left", padx=5)
        
        self.add_btn = ctk.CTkButton(input_row, text="Add", command=self.add_to_bill_action, width=100, height=45, fg_color=COLORS["accent"], font=ctk.CTkFont(weight="bold"))
        self.add_btn.pack(side="left", padx=5)
        
        # Table
        self.bill_table = ctk.CTkScrollableFrame(self.pos_frame, fg_color="transparent")
        self.bill_table.pack(padx=20, pady=10, fill="both", expand=True)
        self.bill_table.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # --- RIGHT: SUMMARY ---
        self.summary_frame = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12, border_width=1, border_color="#334155")
        self.summary_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.summary_frame, text="Summary", font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["subtext"]).pack(pady=20)
        
        self.total_label = ctk.CTkLabel(self.summary_frame, text="₹ 0.00", font=ctk.CTkFont(size=42, weight="bold"), text_color=COLORS["accent"])
        self.total_label.pack(pady=40)
        
        self.complete_btn = ctk.CTkButton(self.summary_frame, text="Finalize Sale", height=55, command=self.complete_sale_action, fg_color=COLORS["accent"], font=ctk.CTkFont(size=16, weight="bold"))
        self.complete_btn.pack(padx=20, pady=10, fill="x")
        
        self.clear_btn = ctk.CTkButton(self.summary_frame, text="Clear All", height=40, command=self.clear_bill, fg_color="#334155", text_color=COLORS["danger"])
        self.clear_btn.pack(padx=20, pady=10, fill="x")

        self.render_bill_table()

    def render_bill_table(self):
        for widget in self.bill_table.winfo_children(): widget.destroy()
        
        headers = ["ITEM", "QTY", "PRICE", "TOTAL"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(self.bill_table, text=h, font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["subtext"]).grid(row=0, column=i, pady=10)
            
        total = 0
        for r, item in enumerate(self.current_bill_items, start=1):
            ctk.CTkLabel(self.bill_table, text=item[0].upper()).grid(row=r, column=0, pady=5)
            ctk.CTkLabel(self.bill_table, text=str(item[1])).grid(row=r, column=1, pady=5)
            ctk.CTkLabel(self.bill_table, text=f"₹{item[2]:.2f}").grid(row=r, column=2, pady=5)
            ctk.CTkLabel(self.bill_table, text=f"₹{item[3]:.2f}", font=ctk.CTkFont(weight="bold")).grid(row=r, column=3, pady=5)
            total += item[3]
            
        self.total_label.configure(text=f"₹ {total:.2f}")

    def add_to_bill_action(self):
        name = self.item_name_entry.get().strip().lower()
        qty_str = self.item_qty_entry.get().strip()
        if not name or not qty_str: return
        
        try:
            qty = int(qty_str)
            price = get_item_price(name)
            if price is None:
                messagebox.showerror("Not Found", f"'{name}' is not in inventory.")
                return
            
            stock = get_stock(name)
            if stock < qty:
                messagebox.showwarning("Stock Low", f"Only {stock} units available.")
                return
                
            self.current_bill_items.append([name, qty, price, price * qty])
            self.render_bill_table()
            self.item_name_entry.delete(0, 'end')
            self.item_qty_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Check quantity format.")

    def clear_bill(self):
        self.current_bill_items = []
        self.render_bill_table()

    def complete_sale_action(self):
        if not self.current_bill_items: return
            
        res = create_bill([(i[0], i[1]) for i in self.current_bill_items])
        if res:
            messagebox.showinfo("Success", "Transaction recorded successfully.")
            self.clear_bill()
            if hasattr(self.master.master.master, 'update_all_views'):
                self.master.master.master.update_all_views()
        else:
            messagebox.showerror("Error", "Stock update failed.")

import customtkinter as ctk
from analytics.insights import top_selling_products, daily_sales_summary
from core.expense import total_expense

class AnalyticsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="Business Analytics", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Stats Grid
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.refresh()

    def refresh(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        sales = daily_sales_summary()
        expenses = total_expense()
        profit = sales - expenses
        
        # Summary Row
        ctk.CTkLabel(self.stats_frame, text=f"Total Sales: ₹ {sales:.2f}", font=ctk.CTkFont(size=18)).grid(row=0, column=0, padx=20, pady=20)
        ctk.CTkLabel(self.stats_frame, text=f"Total Expenses: ₹ {expenses:.2f}", font=ctk.CTkFont(size=18), text_color="#e74c3c").grid(row=0, column=1, padx=20, pady=20)
        
        ctk.CTkLabel(self.stats_frame, text=f"Estimated Profit: ₹ {profit:.2f}", font=ctk.CTkFont(size=22, weight="bold"), text_color="#2ecc71").grid(row=1, column=0, columnspan=2, pady=20)
        
        # Top Products
        ctk.CTkLabel(self.stats_frame, text="Top Selling Products", font=ctk.CTkFont(size=20, weight="bold")).grid(row=2, column=0, columnspan=2, pady=(20, 10))
        
        top_items = top_selling_products(5)
        for i, (name, qty, rev) in enumerate(top_items, start=3):
            ctk.CTkLabel(self.stats_frame, text=f"{i-2}. {name.capitalize()} — {qty} units (₹{rev:.2f})").grid(row=i, column=0, columnspan=2, pady=5)
            
        if not top_items:
            ctk.CTkLabel(self.stats_frame, text="No sales data yet.").grid(row=3, column=0, columnspan=2, pady=10)

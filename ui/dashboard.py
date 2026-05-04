import customtkinter as ctk
from analytics.insights import daily_stats, top_selling_products, low_stock_items, get_actionable_insights, last_7_days_sales
from datetime import datetime

# Pro Color Palette
COLORS = {
    "bg": "#020617",       # Slate 950 (Deep Dark)
    "card": "#0f172a",     # Slate 900 (Card Bg)
    "border": "#1e293b",   # Slate 800 (Border)
    "accent": "#10b981",   # Emerald 500
    "text_p": "#f8fafc",   # Slate 50 (Primary Text)
    "text_s": "#64748b",   # Slate 500 (Secondary Text)
    "danger": "#f43f5e",   # Rose 500
    "info": "#0ea5e9",     # Sky 500
    "warning": "#f59e0b"   # Amber 500
}

class GlassCard(ctk.CTkFrame):
    def __init__(self, master, title, value, color, icon, **kwargs):
        super().__init__(master, fg_color=COLORS["card"], corner_radius=16, border_width=1, border_color=COLORS["border"], **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Icon & Title Row
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 0))
        
        ctk.CTkLabel(header, text=icon, font=ctk.CTkFont(size=20)).pack(side="left")
        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLORS["text_s"]).pack(side="left", padx=10)
        
        # Value
        self.val_label = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color=color)
        self.val_label.pack(fill="x", padx=15, pady=(5, 15), anchor="w")

    def set_value(self, val):
        self.val_label.configure(text=val)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"], **kwargs)
        
        # Parent layout
        self.grid_columnconfigure(0, weight=3) # Main content
        self.grid_columnconfigure(1, weight=1) # Sidebar content
        self.grid_rowconfigure(1, weight=1)
        
        # --- TOP HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(30, 20))
        
        self.title_lbl = ctk.CTkLabel(self.header_frame, text="Business Dashboard", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORS["text_p"])
        self.title_lbl.pack(side="left")
        
        self.date_lbl = ctk.CTkLabel(self.header_frame, text=datetime.now().strftime("%A, %d %B %Y"), font=ctk.CTkFont(size=14), text_color=COLORS["text_s"])
        self.date_lbl.pack(side="right")

        # --- MAIN CONTENT (LEFT) ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=(0, 30))
        self.main_content.grid_columnconfigure((0, 1), weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        # Stat Cards Grid
        self.stats_grid = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.stats_grid.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_sales = GlassCard(self.stats_grid, "DAILY REVENUE", "₹ 0", COLORS["accent"], "💰")
        self.card_sales.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")

        self.card_expense = GlassCard(self.stats_grid, "EXPENSES", "₹ 0", COLORS["danger"], "📉")
        self.card_expense.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_profit = GlassCard(self.stats_grid, "NET PROFIT", "₹ 0", COLORS["info"], "📈")
        self.card_profit.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.card_orders = GlassCard(self.stats_grid, "ORDERS", "0", COLORS["warning"], "🛒")
        self.card_orders.grid(row=0, column=3, padx=(10, 0), pady=10, sticky="nsew")

        # Chart Section
        self.chart_card = ctk.CTkFrame(self.main_content, fg_color=COLORS["card"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        self.chart_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        
        ctk.CTkLabel(self.chart_card, text="Weekly Sales Performance", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLORS["text_p"]).pack(anchor="w", padx=20, pady=20)
        
        self.chart_area = ctk.CTkFrame(self.chart_card, fg_color="transparent", height=200)
        self.chart_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- SIDEBAR CONTENT (RIGHT) ---
        self.side_content = ctk.CTkFrame(self, fg_color="transparent")
        self.side_content.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=(0, 30))
        
        # Insights
        self.insight_card = ctk.CTkFrame(self.side_content, fg_color=COLORS["card"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        self.insight_card.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(self.insight_card, text="💡 AI Insights", font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=15)
        self.insight_box = ctk.CTkFrame(self.insight_card, fg_color="transparent")
        self.insight_box.pack(fill="x", padx=15, pady=(0, 15))

        # Low Stock
        self.stock_card = ctk.CTkFrame(self.side_content, fg_color=COLORS["card"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        self.stock_card.pack(fill="both", expand=True)
        ctk.CTkLabel(self.stock_card, text="⚠️ Critical Stock", font=ctk.CTkFont(size=15, weight="bold"), text_color=COLORS["danger"]).pack(anchor="w", padx=15, pady=15)
        self.stock_box = ctk.CTkFrame(self.stock_card, fg_color="transparent")
        self.stock_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Initial Refresh
        self.refresh()

    def refresh(self):
        # 1. Update Stats
        data = daily_stats()
        self.card_sales.set_value(f"₹ {data['sales']:.0f}")
        self.card_expense.set_value(f"₹ {data['expenses']:.0f}")
        self.card_profit.set_value(f"₹ {data['profit']:.0f}")
        self.card_orders.set_value(str(data['transactions']))

        # 2. Render Chart
        self.draw_chart()

        # 3. Update Insights
        for w in self.insight_box.winfo_children(): w.destroy()
        insights = get_actionable_insights()
        for text in insights[:4]:
            lbl = ctk.CTkLabel(self.insight_box, text=text, font=ctk.CTkFont(size=12), wraplength=180, justify="left", anchor="w")
            lbl.pack(fill="x", pady=5)

        # 4. Update Stock
        for w in self.stock_box.winfo_children(): w.destroy()
        low = low_stock_items()[:6]
        for name, qty in low:
            row = ctk.CTkFrame(self.stock_box, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=name.capitalize(), font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkLabel(row, text=str(qty), text_color=COLORS["danger"], font=ctk.CTkFont(weight="bold")).pack(side="right")
        if not low:
            ctk.CTkLabel(self.stock_box, text="Inventory is full! ✅", text_color=COLORS["accent"]).pack(pady=20)

    def draw_chart(self):
        for w in self.chart_area.winfo_children(): w.destroy()
        trend = last_7_days_sales()
        if not trend: return
        
        max_sale = max([s for d, s in trend]) if any(s > 0 for d, s in trend) else 100
        
        container = ctk.CTkFrame(self.chart_area, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(list(range(len(trend))), weight=1)
        container.grid_rowconfigure(0, weight=1)

        for i, (date, val) in enumerate(trend):
            day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a').upper()
            pct = (val / max_sale)
            
            bar_col = ctk.CTkFrame(container, fg_color="transparent")
            bar_col.grid(row=0, column=i, sticky="ns")
            
            # Using absolute pixel sizing for bars in a fixed-height container
            bar_h = int(pct * 140) if pct > 0 else 4
            
            # Spacer to push bar down
            ctk.CTkLabel(bar_col, text="", height=(140 - bar_h)).pack(side="top")
            
            # The actual bar
            bar = ctk.CTkFrame(bar_col, fg_color=COLORS["accent"] if val > 0 else COLORS["border"], width=35, height=bar_h, corner_radius=6)
            bar.pack(side="top")
            
            # Label
            ctk.CTkLabel(bar_col, text=day_name, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS["text_s"]).pack(side="top", pady=10)

    def add_log(self, msg):
        # We removed the log box for a cleaner look, but we can print to console or add a toast
        print(f"[DASHBOARD LOG] {msg}")

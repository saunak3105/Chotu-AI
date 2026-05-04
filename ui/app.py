import customtkinter as ctk
import threading
from ui.dashboard import DashboardFrame
from ui.inventory_view import InventoryFrame
from ui.analytics_view import AnalyticsFrame
from ui.billing_view import BillingFrame
from ui.voice_panel import VoicePanel
from speech.tts import speak
from core.inventory import update_stock, get_stock
from core.billing import create_bill
from core.expense import add_expense
from analytics.insights import low_stock_items, daily_sales_summary
from utils.constants import *
from utils.logger import get_logger

logger = get_logger(__name__)

# Match modern theme
COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#10b981",
    "sidebar": "#020617"
}

class ChotuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chotu AI - Kirana Assistant Pro")
        self.geometry("1240x820")
        self.configure(fg_color=COLORS["bg"])
        
        ctk.set_appearance_mode("dark")

        # Main Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLORS["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="🏪 CHOTU AI", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["accent"])
        self.logo.pack(padx=20, pady=40)
        
        btn_opts = {"anchor": "w", "height": 45, "corner_radius": 8, "font": ctk.CTkFont(size=14, weight="bold")}
        
        self.btn_dash = ctk.CTkButton(self.sidebar, text="  📊 Dashboard", command=lambda: self.show_frame("dash"), fg_color="transparent", text_color="#94a3b8", hover_color="#1e293b", **btn_opts)
        self.btn_dash.pack(padx=15, pady=5, fill="x")
        
        self.btn_bill = ctk.CTkButton(self.sidebar, text="  🛒 Billing (POS)", command=lambda: self.show_frame("bill"), fg_color="transparent", text_color="#94a3b8", hover_color="#1e293b", **btn_opts)
        self.btn_bill.pack(padx=15, pady=5, fill="x")
        
        self.btn_inv = ctk.CTkButton(self.sidebar, text="  📦 Inventory", command=lambda: self.show_frame("inv"), fg_color="transparent", text_color="#94a3b8", hover_color="#1e293b", **btn_opts)
        self.btn_inv.pack(padx=15, pady=5, fill="x")
        
        self.btn_analytics = ctk.CTkButton(self.sidebar, text="  📈 Analytics", command=lambda: self.show_frame("analytics"), fg_color="transparent", text_color="#94a3b8", hover_color="#1e293b", **btn_opts)
        self.btn_analytics.pack(padx=15, pady=5, fill="x")
        
        # Voice Panel
        self.voice_panel = VoicePanel(self.sidebar, on_command_callback=self.handle_command)
        self.voice_panel.pack(padx=10, pady=20, side="bottom", fill="x")

        # --- MAIN CONTAINER ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.frames["dash"] = DashboardFrame(self.container)
        self.frames["bill"] = BillingFrame(self.container)
        self.frames["inv"] = InventoryFrame(self.container)
        self.frames["analytics"] = AnalyticsFrame(self.container)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("dash")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def update_all_views(self):
        for frame in self.frames.values():
            if hasattr(frame, 'refresh'):
                frame.refresh()

    def handle_command(self, data):
        intent = data.get("intent")
        item = data.get("item")
        qty = data.get("quantity", 1)
        amount = data.get("amount", 0.0)
        
        response = ""
        success = False

        if intent == INTENT_ADD_ITEM:
            if item:
                if update_stock(item, qty):
                    response = f"Added {qty} {item} to stock."
                    success = True
                else: response = f"Error updating stock for {item}."
            else: response = "Could not identify item to add."

        elif intent == INTENT_REMOVE_ITEM:
            if item:
                if update_stock(item, -qty):
                    response = f"Removed {qty} {item} from stock."
                    success = True
                else: response = f"Not enough stock for {item}."
            else: response = "Could not identify item to remove."

        elif intent == INTENT_CREATE_BILL:
            if item:
                bill = create_bill([(item, qty)])
                if bill:
                    response = f"Bill created: {qty} {item}. Total: ₹{bill['total']}."
                    success = True
                else: response = f"Failed to create bill. Check stock for {item}."
            else: response = "Item not found for billing."

        elif intent == INTENT_QUERY_STOCK:
            if item:
                stock = get_stock(item)
                response = f"Stock of {item} is {stock}." if stock is not None else f"{item} not found."
                success = stock is not None
                if success: self.show_frame("inv")
            else:
                low = low_stock_items()
                response = f"Found {len(low)} low stock items."
                success = True
                self.show_frame("dash")

        elif intent == INTENT_ADD_EXPENSE:
            if amount > 0:
                add_expense(amount, data.get("category", "general"))
                response = f"Recorded expense of ₹{amount}."
                success = True
            else: response = "Invalid expense amount."

        elif intent == INTENT_SHOW_SALES:
            total = daily_sales_summary()
            response = f"Today's total sales are ₹{total:.2f}."
            success = True
            self.show_frame("analytics")

        else:
            response = "I'm not sure how to help with that. Please try again."

        # Feedback to UI
        self.frames["dash"].add_log(response)
        self.voice_panel.set_status("Done", "#2ecc71" if success else "#e74c3c")
        
        # Speak response
        threading.Thread(target=speak, args=(response,), daemon=True).start()
        
        # Real-time refresh
        self.update_all_views()

if __name__ == "__main__":
    app = ChotuApp()
    app.mainloop()

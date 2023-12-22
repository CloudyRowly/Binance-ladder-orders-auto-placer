import datetime
from decimal import Decimal
from decimal import InvalidOperation
from tkinter import Misc
import customtkinter as ctk

from accounts import Accounts
from order import Order
from values import Symbol
from custom_textbox import CustomTextBox as CTB

class Broker(ctk.CTk):

    def __init__(self):
        super().__init__()

        ### Default values for textboxes ###
        self.default_price_steps = "0.1"
        self.default_steps = "3"

        # Accounts instance
        self.acc = Accounts()
        
        # Set app basic UI config
        self.title("Cloudy Binance broker")
        self.geometry("400x330")
        self.resizable(False, False)
        
        # Basic parameters and initializations
        # Supported modes : Light, Dark, System
        ctk.set_appearance_mode("System")
        # Supported themes : green, dark-blue, blue
        ctk.set_default_color_theme("blue")
    
        # Create user's order instance
        self.order = Order(self.acc.accounts[0])
        # Setup
        self.setup_ui()

    
    def setup_ui(self):
        """
        Setup app's UI element
        """
        self.make_control_frame()
        self.make_buttons()
        self.make_labels()
        self.make_text_boxes()
        self.make_message_box()


    ### Control Frame setting ###
    def make_control_frame(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row = 1, column = 0, padx = (5,5), pady = (5,0), sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight = 2, uniform="frame_col")
        self.control_frame.grid_columnconfigure(1, weight = 2, uniform="frame_col")


    def show_message(self, message):
        self.textbox_message.configure(state="normal")
        self.textbox_message.delete("0.0", "end")
        self.textbox_message.insert("0.0", datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " - " + message)
        self.textbox_message.configure(state="disabled")


    def update_total(self, event):
        try:
            total = self.get_text_to_decimal(self.textbox_price) * self.get_text_to_decimal(self.textbox_amount)
            if total > 0:
                self.show_message("Total: " + str(total) + " USDT")
        except InvalidOperation:
            return
            # do nothing


    def get_text_to_decimal(self, textbox):
        output = -1
        try:
            output = Decimal(textbox.get("0.0", "end"))
        except InvalidOperation:
            self.show_message("kiểm tra lại só liệu nhập vào!")
        return output


    def get_text_to_int(self, textbox):
        output = -1
        try:
            output = int(textbox.get("0.0", "end"))
        except InvalidOperation:
            self.show_message("kiểm tra lại só liệu nhập vào!")
        return output


    def fetch_info(self):
        price = self.get_text_to_decimal(self.textbox_price)
        amount = self.get_text_to_decimal(self.textbox_amount)
        price_step = self.get_text_to_decimal(self.textbox_price_step)
        step = self.get_text_to_int(self.textbox_steps)
        return price, price_step, step, amount


    def evaluate_order_response(self, target_count, count_before, count_after, message = ""):
        difference = int(count_after) - int(count_before)
        self.show_message("Đã đặt " + str(difference) + "/" + str(target_count) + " lệnh: " + message)

    def button_sell_event(self):
        self.button_sell.configure(state="disabled")
        price, price_step, step, amount = self.fetch_info()
        if price == -1 or price_step == -1 or step == -1 or amount == -1:
            app.after(300, self.button_sell.configure(state="normal"))
            return
        order_count_before = self.order.count_open_margin_orders(Symbol.LTCUSDT)
        response = self.order.sell_margin_multiple(Symbol.LTCUSDT, price, price_step, step, amount)
        app.after(300, self.evaluate_order_response(step, order_count_before, 
                                                    self.order.count_open_margin_orders(Symbol.LTCUSDT), response[5:]))
        # if response != None:
        #     self.show_message(response)
        app.after(300, self.button_sell.configure(state="normal"))


    def button_buy_event(self):
        self.button_buy.configure(state="disabled")
        price, price_step, step, amount = self.fetch_info()
        if price == -1 or price_step == -1 or step == -1 or amount == -1:
            app.after(300, self.button_buy.configure(state="normal"))
            return
        order_count_before = self.order.count_open_margin_orders(Symbol.LTCUSDT)
        response = self.order.buy_margin_multiple(Symbol.LTCUSDT, price, price_step, step, amount)
        app.after(300, self.evaluate_order_response(step, order_count_before, 
                                                    self.order.count_open_margin_orders(Symbol.LTCUSDT), response[5:]))
        app.after(300, self.button_buy.configure(state="normal"))


    def switch_account(self, user):
        self.order = Order(user)


    def switch_account_event(self, value):
        self.show_message("switched to " + value.get() + " account")
        # switch account on the backend
        self.switch_account(value.get())


    ###################################### BUTTONS ######################################
    def make_buttons(self):
        self.button_sell = ctk.CTkButton(self.control_frame, text="SELL", command=self.button_sell_event, fg_color="red4", hover_color="brown3", width=185)
        self.button_sell.grid(row=4, column = 1, padx=5, pady = 10)

        self.button_buy = ctk.CTkButton(self.control_frame, text="BUY", command=self.button_buy_event, fg_color="green4", hover_color="SpringGreen3", width=185)
        self.button_buy.grid(row=4, column = 0, padx=5, pady = 10)

        ### Account select segmented button ###
        self.account_selection = ctk.CTkSegmentedButton(self, values = self.acc.accounts, command = self.switch_account)
        self.account_selection.set(self.acc.accounts[0])
        self.account_selection.grid(row = 0, column = 0, padx = (5,5), pady = (5,0), sticky="ew")


    ########################################## LABELS ###########################################
    def make_labels(self):
        self.label_price = ctk.CTkLabel(self.control_frame, text="Price", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
        self.label_price.grid(row=0, column = 0, padx=0, pady = 10, sticky="ew")

        self.label_amount = ctk.CTkLabel(self.control_frame, text="Amount", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
        self.label_amount.grid(row=1, column = 0, padx=0, pady = 10, sticky="ew")

        self.label_price_step = ctk.CTkLabel(self.control_frame, text="Price step", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
        self.label_price_step.grid(row=2, column = 0, padx=0, pady = 10, sticky="ew")

        self.label_step = ctk.CTkLabel(self.control_frame, text="Steps", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
        self.label_step.grid(row=3, column = 0, padx=0, pady = 10, sticky="ew")


    ################################# TEXT BOXES #################################
    def make_text_boxes(self):
        self.box_height = self.label_price.cget("height")

        self.textbox_price = CTB(self.control_frame, height = self.box_height, width=185)
        self.textbox_price.insert("0.0", "price")
        self.textbox_price.grid(row=0, column = 1, padx=5, pady = 10, sticky="ew")

        self.textbox_amount = CTB(self.control_frame, height = self.box_height, width=185)
        self.textbox_amount.insert("0.0", "amount")
        self.textbox_amount.grid(row=1, column = 1, padx=5, pady = 10, sticky="ew")

        self.textbox_price_step = CTB(self.control_frame, height = self.box_height, width=185)
        self.textbox_price_step.insert("0.0", self.default_price_steps)
        self.textbox_price_step.grid(row=2, column = 1, padx=5, pady = 10, sticky="ew")

        self.textbox_steps = CTB(self.control_frame, height = self.box_height, width=185)
        self.textbox_steps.insert("0.0", self.default_steps)
        self.textbox_steps.grid(row=3, column = 1, padx=5, pady = 10, sticky="ew")

        # Setting "return" traversal order
        self.textbox_price.set_next(self.textbox_amount)
        self.textbox_amount.set_next(self.textbox_price_step)
        self.textbox_price_step.set_next(self.textbox_steps)
        self.textbox_steps.set_next(self.textbox_price)

        # Bind event to update total
        self.textbox_price.bind("<KeyRelease>", self.update_total)
        self.textbox_amount.bind("<KeyRelease>", self.update_total)


    # textbox_total = ctk.CTkTextbox(app, height = box_height)
    # textbox_total.grid(row=1, padx=5, pady = 5, sticky="ew")
    # textbox_total.configure(state="disabled")

    ################################# debug text box #################################
    def make_message_box(self):
        self.textbox_message = ctk.CTkTextbox(self, height = self.box_height)
        self.textbox_message.grid(row=3, padx=5, pady = 5, sticky="ew")
        self.textbox_message.configure(state="disabled")


app = Broker()
app.mainloop()
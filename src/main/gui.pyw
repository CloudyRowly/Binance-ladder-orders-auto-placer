import datetime
from decimal import Decimal
from decimal import InvalidOperation
import tkinter
import customtkinter as ctk
from utils import get_api_key
from binance.spot import Spot

from values import Side, Symbol
from main import buy_margin_multiple, sell_margin_multiple


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

### App window ###
app = ctk.CTk()
app.title("Cloudy ultimate broker")
app.geometry("400x300")
app.resizable(False, False)


### Control Frame setting
control_frame = ctk.CTkFrame(app)
control_frame.grid(row = 0, column = 0, padx = (5,5), pady = (5,0), sticky="ew")
control_frame.grid_columnconfigure(0, weight = 2, uniform="frame_col")
control_frame.grid_columnconfigure(1, weight = 2, uniform="frame_col")


def show_message(message):
    textbox_message.configure(state="normal")
    textbox_message.delete("0.0", "end")
    textbox_message.insert("0.0", datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " - " + message)
    textbox_message.configure(state="disabled")


# def update_total(total):
#     textbox_total.configure(state="normal")
#     textbox_total.delete("0.0", "end")
#     textbox_total.insert("Total: " + str(total) + " USDT")
#     textbox_total.configure(state="disabled")


def get_text_to_decimal(textbox):
    output = -1
    try:
        output = Decimal(textbox.get("0.0", "end"))
    except InvalidOperation:
        show_message("kiểm tra lại só liệu nhập vào!")
    return output


def get_text_to_int(textbox):
    output = -1
    try:
        output = int(textbox.get("0.0", "end"))
    except InvalidOperation:
        show_message("kiểm tra lại só liệu nhập vào!")
    return output


def fetch_info():
    price = get_text_to_decimal(textbox_price)
    amount = get_text_to_decimal(textbox_amount)
    price_step = get_text_to_decimal(textbox_price_step)
    step = get_text_to_int(textbox_steps)
    return price, price_step, step, amount


def button_sell_event():
    button_sell.configure(state="disabled")
    price, price_step, step, amount = fetch_info()
    if price == -1 or price_step == -1 or step == -1 or amount == -1:
        app.after(500, button_sell.configure(state="normal"))
        return
    
    success = sell_margin_multiple(Symbol.LTCUSDT, price, price_step, step, amount)
    if not success:
        show_message("Error: chưa đặt được lệnh")
    else:
        show_message("Đặt lệnh thành công!")
    app.after(500, button_sell.configure(state="normal"))



def button_buy_event():
    button_buy.configure(state="disabled")
    price, price_step, step, amount = fetch_info()
    if price == -1 or price_step == -1 or step == -1 or amount == -1:
        app.after(500, button_buy.configure(state="normal"))
        return
    
    success = buy_margin_multiple(Symbol.LTCUSDT, price, price_step, step, amount)

    if not success:
        show_message("Error: chưa đặt được lệnh")
    else:
        show_message("Đặt lệnh thành công!")
    app.after(500, button_buy.configure(state="normal"))


button_sell = ctk.CTkButton(control_frame, text="SELL", command=button_sell_event, fg_color="red4", hover_color="brown3", width=185)
button_sell.grid(row=4, column = 1, padx=5, pady = 10)

button_buy = ctk.CTkButton(control_frame, text="BUY", command=button_buy_event, fg_color="green4", hover_color="SpringGreen3", width=185)
button_buy.grid(row=4, column = 0, padx=5, pady = 10)


########################################## LABELS ###########################################
label_price = ctk.CTkLabel(control_frame, text="Price", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
label_price.grid(row=0, column = 0, padx=0, pady = 10, sticky="ew")

label_amount = ctk.CTkLabel(control_frame, text="Amount", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
label_amount.grid(row=1, column = 0, padx=0, pady = 10, sticky="ew")

label_price_step = ctk.CTkLabel(control_frame, text="Price step", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
label_price_step.grid(row=2, column = 0, padx=0, pady = 10, sticky="ew")

label_step = ctk.CTkLabel(control_frame, text="Steps", font=("Arial Rounded MT Bold", 22), fg_color="transparent", width=185)
label_step.grid(row=3, column = 0, padx=0, pady = 10, sticky="ew")


################################# TEXT BOXES #################################
box_height = label_price.cget("height")

textbox_price = ctk.CTkTextbox(control_frame, height = box_height, width=185)
textbox_price.insert("0.0", "price")
textbox_price.grid(row=0, column = 1, padx=5, pady = 10, sticky="ew")

textbox_amount = ctk.CTkTextbox(control_frame, height = box_height, width=185)
textbox_amount.insert("0.0", "amount")
textbox_amount.grid(row=1, column = 1, padx=5, pady = 10, sticky="ew")

textbox_price_step = ctk.CTkTextbox(control_frame, height = box_height, width=185)
textbox_price_step.insert("0.0", "bước giá")
textbox_price_step.grid(row=2, column = 1, padx=5, pady = 10, sticky="ew")

textbox_steps = ctk.CTkTextbox(control_frame, height = box_height, width=185)
textbox_steps.insert("0.0", "3")
textbox_steps.grid(row=3, column = 1, padx=5, pady = 10, sticky="ew")


# textbox_total = ctk.CTkTextbox(app, height = box_height)
# textbox_total.grid(row=1, padx=5, pady = 5, sticky="ew")
# textbox_total.configure(state="disabled")

### debug text box
textbox_message = ctk.CTkTextbox(app, height = box_height)
textbox_message.grid(row=2, padx=5, pady = 5, sticky="ew")
textbox_message.configure(state="disabled")


app.mainloop()
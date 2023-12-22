import customtkinter as ctk
from decimal import InvalidOperation
from decimal import Decimal

class CustomTextBox(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<FocusIn>", self.on_focus)
        self.bind("<Down>", self.on_return)
    
    
    def on_focus(self, event):
        try:
            Decimal(self.get("0.0", "end"))
        except InvalidOperation:
            self.delete("0.0", "end")

    
    def on_return(self, event):
        """Focus to next widget when "return" is pressed

        Args:
            event (<<RETURN>>): event generated when "return" is pressed
        """
        if self.next_widget:
            self.event_generate('<<TraverseOut>>')
            self.next_widget.focus()
            self.next_widget.event_generate('<<TraverseIn>>')
        else:
            self.event_generate('<<NextWindow>>')

    
    def set_next(self, widget):
        self.next_widget = widget
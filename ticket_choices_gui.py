import tkinter as tk
from tkinter import ttk

PRICES = {"standard": 12, "member": 10}
SESSIONS = ("Morning", "Afternoon")
EMPTY_QUOTE = "Quote: --"
START_PROMPT = "Enter 1 to 5 tickets and choose a session."
CHANGED_PROMPT = "Inputs changed. Calculate a new quote."


def calculate_total(quantity, ticket_type):
    """Receive a validated quantity and supported ticket type."""
    return quantity * PRICES[ticket_type]


def on_inputs_changed(_name, _index, _operation):
    # A previous quote no longer represents the current inputs.
    quote_var.set(EMPTY_QUOTE)
    status_var.set(CHANGED_PROMPT)


def on_calculate():
    quote_var.set(EMPTY_QUOTE)
    raw_quantity = quantity_var.get().strip()

    if raw_quantity == "":
        status_var.set("Enter the number of tickets.")
        return

    try:
        quantity = int(raw_quantity)
    except ValueError:
        status_var.set("Enter a whole number.")
        return

    if quantity < 1 or quantity > 5:
        status_var.set("Enter a quantity from 1 to 5.")
        return

    ticket_type = ticket_type_var.get()
    session = session_var.get()
    if ticket_type not in PRICES:
        status_var.set("Choose Standard or Member.")
        return
    if session not in SESSIONS:
        status_var.set("Choose Morning or Afternoon.")
        return

    total = calculate_total(quantity, ticket_type)
    ticket_word = "ticket" if quantity == 1 else "tickets"
    quote_var.set(
        f"Quote: {quantity} {ticket_type} {ticket_word}, "
        f"{session}: ${total:.2f}"
    )
    status_var.set("Quote ready.")


def on_clear():
    # Each input write can run on_inputs_changed immediately.
    quantity_var.set("")
    ticket_type_var.set("standard")
    session_var.set("")
    # Set the intended final feedback after the input writes.
    quote_var.set(EMPTY_QUOTE)
    status_var.set(START_PROMPT)
    quantity_entry.focus_set()


def on_cancel():
    window.destroy()


window = tk.Tk()
window.title("Club ticket calculator")
window.columnconfigure(1, weight=1)

quantity_var = tk.StringVar(master=window, value="")
ticket_type_var = tk.StringVar(master=window, value="standard")
session_var = tk.StringVar(master=window, value="")
quote_var = tk.StringVar(master=window, value=EMPTY_QUOTE)
status_var = tk.StringVar(master=window, value=START_PROMPT)

ttk.Label(window, text="Number of tickets (1-5):").grid(
    row=0, column=0, padx=12, pady=12, sticky="w"
)
quantity_entry = ttk.Entry(
    window, textvariable=quantity_var, width=12
)
quantity_entry.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

ttk.Label(window, text="Ticket type:").grid(
    row=1, column=0, padx=12, pady=6, sticky="w"
)
standard_radio = ttk.Radiobutton(
    window, text="Standard ($12)",
    variable=ticket_type_var, value="standard"
)
standard_radio.grid(row=1, column=1, padx=12, pady=6, sticky="w")
member_radio = ttk.Radiobutton(
    window, text="Member ($10)",
    variable=ticket_type_var, value="member"
)
member_radio.grid(row=2, column=1, padx=12, pady=6, sticky="w")

ttk.Label(window, text="Session:").grid(
    row=3, column=0, padx=12, pady=12, sticky="w"
)
session_combo = ttk.Combobox(
    window, textvariable=session_var,
    values=SESSIONS, state="readonly", width=18
)
session_combo.grid(row=3, column=1, padx=12, pady=12, sticky="ew")

actions = ttk.Frame(window)
actions.grid(row=4, column=0, columnspan=2, padx=12, pady=12, sticky="w")
calculate_button = ttk.Button(
    actions, text="Calculate total", command=on_calculate
)
calculate_button.grid(row=0, column=0, padx=(0, 8))
clear_button = ttk.Button(actions, text="Clear", command=on_clear)
clear_button.grid(row=0, column=1, padx=(0, 8))
cancel_button = ttk.Button(actions, text="Cancel", command=on_cancel)
cancel_button.grid(row=0, column=2)

quote_label = ttk.Label(window, textvariable=quote_var, wraplength=520)
quote_label.grid(row=5, column=0, columnspan=2, padx=12, pady=6, sticky="w")
status_label = ttk.Label(window, textvariable=status_var, wraplength=520)
status_label.grid(row=6, column=0, columnspan=2, padx=12, pady=(6, 12), sticky="w")

quantity_var.trace_add("write", on_inputs_changed)
ticket_type_var.trace_add("write", on_inputs_changed)
session_var.trace_add("write", on_inputs_changed)

quantity_entry.focus_set()
window.mainloop()

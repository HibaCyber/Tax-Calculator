import customtkinter as ctk
import datetime


class TaxCalculator:
    def __init__(self):
        # Initialize our window
        ctk.set_appearance_mode("dark")  # Default dark mode
        self.window = ctk.CTk()
        self.window.title("Advanced Tax Calculator")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        # Widget padding
        self.padding = {'padx': 10, 'pady': 10}

        # Title
        self.title_label = ctk.CTkLabel(self.window, text="💰 Advanced Tax Calculator 💰", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Income label and entry
        self.income_label = ctk.CTkLabel(self.window, text="Enter Income (Rs):")
        self.income_label.grid(row=1, column=0, sticky="w", **self.padding)
        self.income_entry = ctk.CTkEntry(self.window, placeholder_text="e.g. 50000")
        self.income_entry.grid(row=1, column=1, **self.padding)

        # Tax rate label and entry
        self.tax_rate_label = ctk.CTkLabel(self.window, text="Enter Tax Rate (%):")
        self.tax_rate_label.grid(row=2, column=0, sticky="w", **self.padding)
        self.tax_rate_entry = ctk.CTkEntry(self.window, placeholder_text="e.g. 15")
        self.tax_rate_entry.grid(row=2, column=1, **self.padding)

        # Dropdown for tax mode
        self.mode_label = ctk.CTkLabel(self.window, text="Select Mode:")
        self.mode_label.grid(row=3, column=0, sticky="w", **self.padding)
        self.tax_modes = ["Flat Tax", "Sales Tax", "Progressive Tax Brackets"]
        self.mode_option = ctk.CTkOptionMenu(self.window, values=self.tax_modes)
        self.mode_option.grid(row=3, column=1, **self.padding)

        # Result label and entry
        self.result_label = ctk.CTkLabel(self.window, text="Calculated Tax:")
        self.result_label.grid(row=4, column=0, sticky="w", **self.padding)
        self.result_entry = ctk.CTkEntry(self.window)
        self.result_entry.insert(0, "0")
        self.result_entry.grid(row=4, column=1, **self.padding)

        # Buttons
        self.calculate_button = ctk.CTkButton(self.window, text="Calculate", command=self.calculate_tax)
        self.calculate_button.grid(row=5, column=0, **self.padding)

        self.reset_button = ctk.CTkButton(self.window, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=5, column=1, **self.padding)

        self.save_button = ctk.CTkButton(self.window, text="Save Result", command=self.save_result)
        self.save_button.grid(row=5, column=2, **self.padding)

        # Appearance mode toggle
        self.theme_button = ctk.CTkButton(self.window, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.grid(row=6, column=1, pady=10)

        # History section
        self.history_label = ctk.CTkLabel(self.window, text="Calculation History:")
        self.history_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=10)

        self.history_textbox = ctk.CTkTextbox(self.window, width=550, height=150)
        self.history_textbox.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    def update_result(self, text: str):
        """Updates the result field."""
        self.result_entry.delete(0, ctk.END)
        self.result_entry.insert(0, text)

    def calculate_tax(self):
        """Performs tax calculations based on selected mode."""
        try:
            income = float(self.income_entry.get())
            mode = self.mode_option.get()

            # Flat Tax
            if mode == "Flat Tax":
                tax_rate = float(self.tax_rate_entry.get())
                tax = income * (tax_rate / 100)

            # Sales Tax (only applied on part of income like purchases)
            elif mode == "Sales Tax":
                tax_rate = float(self.tax_rate_entry.get())
                tax = income * (tax_rate / 100)

            # Progressive Tax Brackets (example system)
            elif mode == "Progressive Tax Brackets":
                tax = 0
                if income <= 50000:
                    tax = income * 0.05
                elif income <= 100000:
                    tax = 50000 * 0.05 + (income - 50000) * 0.10
                else:
                    tax = 50000 * 0.05 + 50000 * 0.10 + (income - 100000) * 0.20

            else:
                tax = 0

            result_text = f"Rs {tax:,.2f}"
            self.update_result(result_text)

            # Add to history
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_textbox.insert("end", f"[{timestamp}] Mode: {mode} | Income: Rs {income:,.2f} | Tax: {result_text}\n")
            self.history_textbox.see("end")

        except ValueError:
            self.update_result("Invalid input")

    def reset_fields(self):
        """Clears all input fields and results."""
        self.income_entry.delete(0, ctk.END)
        self.tax_rate_entry.delete(0, ctk.END)
        self.result_entry.delete(0, ctk.END)
        self.result_entry.insert(0, "0")

    def save_result(self):
        """Saves the history log to a text file."""
        try:
            with open("tax_calculation_history.txt", "a", encoding="utf-8") as f:
                history = self.history_textbox.get("1.0", "end").strip()
                f.write(history + "\n")
            self.update_result("Saved to file ✅")
        except Exception as e:
            self.update_result(f"Error: {e}")

    def toggle_theme(self):
        """Switch between light and dark themes."""
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def run(self):
        """Runs the tkinter app."""
        self.window.mainloop()


if __name__ == "__main__":
    tc = TaxCalculator()
    tc.run()

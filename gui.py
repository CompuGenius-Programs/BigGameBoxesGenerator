from tkinter import ttk, StringVar

from ttkthemes import ThemedTk

total_boxes = 100


class Row:
    def __init__(self, parent, command, default_value):
        self.name_label = ttk.Label(parent, text="Enter Name")
        self.name_entry = ttk.Entry(parent)
        self.amount_label = ttk.Label(parent, text="Amount")

        def validate(p):
            if p.isdigit():
                total = sum(int(row.amount_entry.get()) for row in parent.rows if row != self)
                if total + int(p) > total_boxes:
                    self.amount_entry.delete(0, 'end')
                    self.amount_entry.insert(0, str(total_boxes - total))
                    return False
            return True

        vcmd = parent.register(validate)

        self.amount_entry = ttk.Spinbox(parent, from_=1, to=total_boxes, command=command,
                                        validate="key", validatecommand=(vcmd, '%P'))
        self.amount_entry.insert(0, default_value)

        self.add_button = ttk.Button(parent, text="+", command=parent.create_row)
        self.remove_button = ttk.Button(parent, text="-", command=lambda: parent.remove_row(self))

    def grid(self, row):
        row += 1
        self.name_label.grid(row=row, column=0)
        self.name_entry.grid(row=row, column=1)
        self.amount_label.grid(row=row, column=2)
        self.amount_entry.grid(row=row, column=3)
        self.add_button.grid(row=row, column=4)
        self.remove_button.grid(row=row, column=5)


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.default_value_label = ttk.Label(self, text="Default Value")
        self.default_value_label.grid(row=0, column=0)
        self.default_value_entry = ttk.Spinbox(self, from_=1, to=total_boxes)
        self.default_value_entry.grid(row=0, column=1)
        self.default_value_entry.insert(0, '1')

        self.grid()
        self.rows = []

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=len(self.rows) + 2, column=0)
        self.people = []

        self.create_row()

    def validate_spinboxes(self):
        total = sum(int(row.amount_entry.get()) for row in self.rows)
        for row in self.rows:
            row.amount_entry.config(to=max(0, total_boxes - total + int(row.amount_entry.get())))

    def create_row(self):
        if len(self.rows) < total_boxes:
            default_value = self.default_value_entry.get()
            row = Row(self, self.validate_spinboxes, default_value)
            row.grid(len(self.rows))
            self.rows.append(row)
            self.update_submit_button_position()

    def remove_row(self, row):
        if len(self.rows) > 1:
            self.rows.remove(row)
            for widget in vars(row).values():
                widget.destroy()
            self.update_submit_button_position()

    def update_submit_button_position(self):
        self.submit_button.grid_forget()
        self.submit_button.grid(row=len(self.rows) + 1, column=0)

    def submit(self):
        self.people = [(row.name_entry.get(), row.amount_entry.get()) for row in self.rows]
        self.master.destroy()


root = ThemedTk(theme="arc")
root.resizable(False, False)
app = Application(master=root)

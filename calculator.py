import tkinter as tk


class Calculator(tk.Frame):
    input_text = '0'
    operator_stack = []
    number_queue = []
    is_inputting_num = False

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_lbl = tk.Label(self, text=self.input_text)
        self.input_lbl.grid(row=0, column=0, columnspan=3, sticky='e')

        i = 1
        for r in reversed(range(3)):
            for c in range(3):
                btn = tk.Button(self, text=str(i), fg='blue')
                btn['command'] = lambda num=str(i): self.num_command(num)
                btn.grid(row=1 + r, column=0 + c, sticky='news')
                setattr(self, f'num{str(i)}_btn', btn)
                i += 1

        self.plus_btn = tk.Button(self, text='+', fg='red')
        self.plus_btn['command'] = lambda oper='+': self.operator_command(oper)
        self.plus_btn.grid(row=1, column=3)
        self.plus_btn = tk.Button(self, text='-', fg='red')
        self.plus_btn['command'] = lambda oper='-': self.operator_command(oper)
        self.plus_btn.grid(row=1, column=4)
        self.plus_btn = tk.Button(self, text='*', fg='red')
        self.plus_btn['command'] = lambda oper='*': self.operator_command(oper)
        self.plus_btn.grid(row=2, column=3)
        self.plus_btn = tk.Button(self, text='/', fg='red')
        self.plus_btn['command'] = lambda oper='/': self.operator_command(oper)
        self.plus_btn.grid(row=2, column=4)

        self.submit_btn = tk.Button(self, text='=')
        self.submit_btn['command'] = self.calculate
        self.submit_btn.grid(row=3, column=3)
    
    def update_inpute_lbl(self):
        result_string = ''
        numbers = self.number_queue[:]
        operators = self.operator_stack[:]
        for i in range(len(self.number_queue)):
            try:
                result_string += str(numbers.pop(0))
                result_string += str(operators.pop(0))
            except:
                pass
        self.input_text = result_string
        self.input_lbl.configure(text=self.input_text)
    
    def operator_command(self, operator):
        if not self.is_inputting_num:
            return
        self.operator_stack.append(operator)
        self.is_inputting_num = False
        self.update_inpute_lbl()

    def num_command(self, num):
        if self.is_inputting_num:
            self.number_queue[-1] += num
        else:
            self.number_queue.append(num)
            self.is_inputting_num = True
        self.update_inpute_lbl()

    def calculate(self):
        if not self.is_inputting_num:
            return
        pass
        self.update_inpute_lbl()


root = tk.Tk()
app = Calculator(master=root)
app.mainloop()

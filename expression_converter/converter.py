import tkinter as tk
from tkinter import ttk

class ExpressionConverter:
    def __init__(self):
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def isOperator(self, c):
        return (not (c >= 'a' and c <= 'z') and not (c >= '0' and c <= '9') and not (c >= 'A' and c <= 'Z'))

    def getPriority(self, C):
        if C in ('-', '+'):
            return 1
        elif C in ('*', '/'):
            return 2
        elif C == '^':
            return 3
        return 0

    def infix_to_postfix(self, expression):
        output = []
        stack = []
        for char in expression:
            if char.isalnum():  # Operand
                output.append(char)
            elif char in self.precedence:  # Operator
                while (stack and stack[-1] != '(' and
                       self.precedence[char] <= self.precedence[stack[-1]]):
                    output.append(stack.pop())
                stack.append(char)
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Pop '('
        while stack:
            output.append(stack.pop())
        return ''.join(output)

    def infix_to_prefix(self, infix):
        # Stack for operators.
        operators = []
        # Stack for operands.
        operands = []

        for i in range(len(infix)):
            if infix[i] == '(':  # Opening bracket
                operators.append(infix[i])
            elif infix[i] == ')':  # Closing bracket
                while operators and operators[-1] != '(':
                    op1 = operands.pop()
                    op2 = operands.pop()
                    op = operators.pop()
                    operands.append(op + op2 + op1)  # Note the order for prefix
                operators.pop()  # Pop the '('
            elif not self.isOperator(infix[i]):  # Operand
                operands.append(infix[i])
            else:  # Operator
                while (operators and self.getPriority(infix[i]) <= self.getPriority(operators[-1])):
                    op1 = operands.pop()
                    op2 = operands.pop()
                    op = operators.pop()
                    operands.append(op + op2 + op1)  # Note the order for prefix
                operators.append(infix[i])

        while operators:
            op1 = operands.pop()
            op2 = operands.pop()
            op = operators.pop()
            operands.append(op + op2 + op1)  # Note the order for prefix

        return operands[-1]

    def postfix_to_infix(self, expression):
        stack = []
        for char in expression:
            if char.isalnum():  # Operand
                stack.append(char)
            else:  # Operator
                right = stack.pop()
                left = stack.pop()
                stack.append(f'({left}{char}{right})')
        return stack[-1]

    def prefix_to_infix(self, expression):
        stack = []
        for char in reversed(expression):
            if char.isalnum():  # Operand
                stack.append(char)
            else:  # Operator
                left = stack.pop()
                right = stack.pop()
                stack.append(f'({left}{char}{right})')
        return stack[-1]

    def postfix_to_prefix(self, expression):
        infix = self.postfix_to_infix(expression)
        return self.infix_to_prefix(infix)

    def prefix_to_postfix(self, expression):
        infix = self.prefix_to_infix(expression)
        return self.infix_to_postfix(infix)

def select(event):
    global s1,s2
    s1=box1.get()
    s2=box2.get()
        

def act():
    cnvrt=ExpressionConverter()
    if(s1 =='Infix' and s2 == "Prefix"):
        result=cnvrt.infix_to_prefix(expression.get())
        entry.delete(0, tk.END)  # Clear the current text
        entry.insert(0, result) 
    elif(s1 == 'Infix' and s2 == "Postfix"):
        result=cnvrt.infix_to_postfix(expression.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    elif(s1 == 'Prefix' and s2 == "Postfix"):
        result=cnvrt.prefix_to_postfix(expression.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    elif(s1 == 'Prefix' and s2 == "Infix"):
        result=cnvrt.prefix_to_infix(expression.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    elif(s1 == 'Postfix' and s2 == "Infix"):
        result=cnvrt.postfix_to_infix(expression.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    elif(s1 == 'Postfix' and s2 == "Prefix"):
        result=cnvrt.postfix_to_prefix(expression.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    elif(s1 =="" and s2 ==""):
        entry.delete(0,tk.END)
        entry.insert(0,"NOT_SELECTED")
    else:
        entry.delete(0,tk.END)
        entry.insert(0,"SAME_TYPE")


win=tk.Tk()
win.title("Converter")
width=300
height=400
sys_w=win.winfo_screenwidth()
sys_h=win.winfo_screenheight()
w=int(sys_w/2-width/2)
h=int(sys_h/2-height/2)
s1=""
s2=""
expression=tk.StringVar()
result=""
# fr = tk.frame(win, bg="lightgrey", padx=10, pady=10)
# fr.pack(padx=15, pady=20)

lbl=tk.Label(win,text="Convert Expression",font=("Calibere",15,"bold"))
frst=tk.Label(win,text="From: ",font=("Calibere",15))
scnd=tk.Label(win,text="To: ")
combo=["Infix","Prefix","Postfix"]
box1=ttk.Combobox(win,values=combo)
box2=ttk.Combobox(win,values=combo)
btn=tk.Button(win,text="Convert",command=act)
entry=tk.Entry(win,textvariable=expression)
win.geometry(f"{width}x{height}+{w}+{h}")

lbl.grid(row=0,column=2,pady=5)
entry.grid(row=1,column=2,pady=5)
frst.grid(row=2,column=1,pady=5)
box1.grid(row=2,column=2,pady=5)
scnd.grid(row=3,column=1,pady=5)
box2.grid(row=3,column=2,pady=5)
btn.grid(row=4,column=2)

box1.bind("<<ComboboxSelected>>",select)
box2.bind("<<ComboboxSelected>>",select)

win.mainloop()

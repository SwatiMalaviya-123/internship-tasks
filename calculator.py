import ast
import operator
import tkinter as tk
from tkinter import messagebox
import re


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Invalid calculation")

    return evaluate(ast.parse(expression, mode="eval"))


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.expression = tk.StringVar()

        self.display = tk.Entry(
            root, textvariable=self.expression, font=("Arial", 24),
            justify="right", state="readonly"
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=6, pady=6)

        buttons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", "00", ".", "="],
        ]

        for row_index, row in enumerate(buttons, start=1):
            for column_index, label in enumerate(row):
                if not label:
                    continue

                command = self.clear if label == "C" else (
                    self.backspace if label == "⌫" else (
                        self.percent if label == "%" else (
                            self.calculate_result if label == "=" else
                            lambda value=label: self.press(value)
                        )
                    )
                )

                tk.Button(
                    root, text=label, font=("Arial", 18),
                    command=command
                ).grid(
                    row=row_index, column=column_index,
                    sticky="nsew", padx=3, pady=3
                )

        for column in range(4):
            root.columnconfigure(column, weight=1)
        for row in range(6):
            root.rowconfigure(row, weight=1)

    def press(self, value):
        self.expression.set(self.expression.get() + value)

    def clear(self):
        self.expression.set("")

    def backspace(self):
        self.expression.set(self.expression.get()[:-1])

    def percent(self):
        expression = self.expression.get()
        match = re.search(r"(\d+(?:\.\d+)?)([+\-*/])(\d+(?:\.\d+)?)$", expression)

        if match:
            left = float(match.group(1))
            operator_symbol = match.group(2)
            right = float(match.group(3))

            value = left * right / 100 if operator_symbol in "+-" else right / 100
            replacement = f"{match.group(1)}{operator_symbol}({value})"
            expression = expression[:match.start()] + replacement
        else:
            match = re.search(r"(\d+(?:\.\d+)?)$", expression)
            if not match:
                return

            value = float(match.group(1)) / 100
            expression = expression[:match.start()] + f"({value})"

        self.expression.set(expression)

    def calculate_result(self):
        try:
            result = calculate(self.expression.get())
            self.expression.set(str(result))
        except (SyntaxError, ValueError, ZeroDivisionError):
            messagebox.showerror("Calculation error", "Please check the expression.")
            self.clear()


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
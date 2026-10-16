import random
import tkinter as tk
from tkinter import messagebox


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("380x300")
        self.root.resizable(False, False)

        tk.Label(
            root,
            text="Guess a number from 1 to 100",
            font=("Arial", 16, "bold"),
        ).pack(pady=18)

        self.guess_entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.guess_entry.pack(pady=8)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        tk.Button(root, text="Check", command=self.check_guess).pack(pady=5)

        self.feedback = tk.Label(root, text="Enter a number to begin.", font=("Arial", 12))
        self.feedback.pack(pady=10)

        self.attempts_label = tk.Label(root, text="Attempts: 0", font=("Arial", 11))
        self.attempts_label.pack()

        tk.Button(root, text="New Game", command=self.new_game).pack(pady=12)

        self.new_game()

    def new_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.guess_entry.delete(0, tk.END)
        self.feedback.config(text="Enter a number to begin.", fg="black")
        self.attempts_label.config(text="Attempts: 0")
        self.guess_entry.focus()

    def check_guess(self):
        value = self.guess_entry.get().strip()

        try:
            guess = int(value)
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter a whole number.")
            return

        if not 1 <= guess <= 100:
            messagebox.showwarning("Out of range", "Enter a number from 1 to 100.")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.secret_number:
            self.feedback.config(text="Too low. Try again!", fg="blue")
        elif guess > self.secret_number:
            self.feedback.config(text="Too high. Try again!", fg="orange")
        else:
            self.feedback.config(
                text=f"Correct! You got it in {self.attempts} tries!",
                fg="green",
            )


if __name__ == "__main__":
    window = tk.Tk()
    NumberGuessingGame(window)
    window.mainloop()
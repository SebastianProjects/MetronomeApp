import tkinter as tk

class BlinkingDot:
    def __init__(self, root, interval=500):
        self.root = root
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack()

        # Create a red dot
        self.dot = self.canvas.create_oval(90, 90, 110, 110, fill='red')

        # Blinking interval in milliseconds
        self.interval = interval
        self.is_visible = True

        # Start the blinking
        self.blink()

    def blink(self):
        if self.is_visible:
            self.canvas.itemconfig(self.dot, state='hidden')
        else:
            self.canvas.itemconfig(self.dot, state='normal')

        self.is_visible = not self.is_visible

        # Schedule the next blink
        self.root.after(self.interval, self.blink)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Blinking Red Dot")

    blinking_dot = BlinkingDot(root)

    root.mainloop()
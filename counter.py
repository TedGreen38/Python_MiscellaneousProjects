import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Counter")

    count = 0
    value_label = tk.Label(root, text=str(count), font=("TkDefaultFont", 24))
    value_label.pack(padx=24, pady=(24, 12))

    def increment():
        nonlocal count
        count += 1
        value_label.config(text=str(count))

    def handle_space(_event):
        increment()
        return "break"

    button = tk.Button(root, text="Increment", command=increment)
    button.pack(padx=24, pady=(0, 24))

    root.bind("<space>", handle_space)
    button.bind("<space>", handle_space)
    root.mainloop()

if __name__ == "__main__":
    main()
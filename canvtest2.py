import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, background="white")
canvas.pack(fill="both", expand=True)

text_item = canvas.create_text(20, 20, anchor="w", text="Hello world!", fill="white")
bbox = canvas.bbox(text_item)
rect_item = canvas.create_rectangle(bbox, outline="red", fill="black")
canvas.tag_raise(text_item,rect_item)

root.mainloop()
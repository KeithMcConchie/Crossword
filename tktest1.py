from tkinter import *

root = Tk()
def fun1():
    print("hello1")
def fun2():
    print("hello2")
def fun3():
    print("hello3")

# top_frame = Frame(root)
# top_frame.pack(side=RIGHT)
# bottom_frame = Frame(root)
# bottom_frame.pack(side=LEFT)
# button1 = Button(top_frame, text="foo1", fg="red")
# button2 = Button(top_frame, text="foo2", fg="blue")
# button3 = Button(top_frame, text="foo3", fg="green")
# button4 = Button(bottom_frame, text="foo4", fg="purple")

# button1.pack(side=LEFT)
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack()
one = Label(root, text="one", bg="red", fg="white")
two = Label(root, text="two", bg="green", fg="black")
three = Label(root, text="three", bg="blue", fg="white")
one.pack()
two.pack(fill=X)
three.pack(side=LEFT, fill=Y)
root.resizable(True, True)
# menubar = Menu(root)
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="Reveal Letter", command=fun1)
# filemenu.add_command(label="Reveal Word", command=fun2)
# filemenu.add_command(label="Reveal Puzzle", command=fun3)
# menubar.add_cascade(label="Reveal", menu=filemenu)
# root.config(menu=menubar)


root.mainloop()
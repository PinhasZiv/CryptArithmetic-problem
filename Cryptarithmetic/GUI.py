from tkinter import *
from Main import getLegalMessage, solveProblem, getStringAnswer

root = Tk()
root.title("CryptArithmetic problem")
root.geometry("450x280")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_columnconfigure(10, weight=1)

Font_tuple = ("Comic Sans MS", 10)

titleMessageText = "Enter 3 Words:"
titleMessage = Label(root, text=titleMessageText)
titleMessage.configure(font=Font_tuple, anchor="center")
titleMessage.grid(column=1, row=1, columnspan=5)

messageLabel = Label(root, text="")
messageLabel.configure(font=Font_tuple, anchor="center")
messageLabel.grid(row=3, column=1, columnspan=5, pady=10)

resultLabel = Label(root, text="", fg="blue")


def onClick():
    first, second, third = firstInput.get(), secondInput.get(), thirdInput.get()
    legal = getLegalMessage(first, second, third)
    if legal != "legal":
        resultLabel['text'] = ""
        messageLabel['text'] = legal
        messageLabel['fg'] = "red"
        messageLabel.grid(row=3, column=1, columnspan=5, pady=0)
    else:
        messageLabel['text'] = ""
        res = solveProblem(first, second, third)

        if res == -1:
            resultLabel['text'] = "There is no solution"
        else:
            resultLabel['text'] = getStringAnswer(res, first, second, third)
        resultLabel.grid(row=5, column=2, columnspan=3)
        resultLabel.configure(font=Font_tuple, anchor="center")


firstInput = Entry(root, width=10, borderwidth=3)
secondInput = Entry(root, width=10, borderwidth=3)
thirdInput = Entry(root, width=10, borderwidth=3)

plusLabel = Label(root, text="+")
plusLabel.grid(column=2, row=2, pady=5)
plusLabel.configure(font=Font_tuple)

equalLabel = Label(root, text="=")
equalLabel.grid(row=2, column=4)
equalLabel.configure(font=Font_tuple)

firstInput.grid(column=1, row=2)
secondInput.grid(column=3, row=2)
thirdInput.grid(column=5, row=2)

buttonConfirm = Button(root, text="Find", padx=20, command=onClick)
buttonConfirm.grid(column=3, row=4)

root.mainloop()


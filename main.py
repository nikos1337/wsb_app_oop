import string
import secrets
from importlib.metadata import files
from tkinter import *
from tkinter import filedialog

class PasswordGenerator:
    def __init__(self, root):
        self.checkChar = BooleanVar(value=True)
        self.checkNum = BooleanVar(value=True)
        self.length_pass = None
        self.received_pass = None
        self.root = root

    def contains_number(self, value):
        for character in value:
            if character.isdigit():
                return True
        return False

    def list_to_string(self, array):
        return "".join(array)

    def generate_password(self):
        self.received_pass.delete(0, END)
        i = 0
        password = []

        if self.length_pass.get() == "":
            length = 0
        elif not self.contains_number(self.length_pass.get()):
            length = 0
        else:
            length = int(self.length_pass.get())

        while length > len(password):
            if not self.checkChar.get() and not self.checkNum.get():
                print(self.checkNum.get())
                print(self.checkChar.get())

                chars = string.ascii_letters
            elif not self.checkChar.get():
                chars = string.ascii_letters + string.digits
            elif not self.checkNum.get():
                chars = string.ascii_letters + string.punctuation
            else:
                chars = string.ascii_letters + string.digits + string.punctuation

            char = list(chars)
            rand = secrets.choice(char)
            password.append(rand)

            if length == 1:
                break
            i += 1
            if len(password) == 1:
                rand2 = secrets.choice(char)
                password.append(rand2)

            if len(password) > 1:
                if password[i] == password[i - 1]:
                    print("zduplikowane: ", password[i], password[i - 1])
                    del password[i]
                    i -= 1

        self.received_pass.insert(0, self.list_to_string(password))


class ClipboardManager:
    def __init__(self, root):
        self.root = root

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)


class FileManager:
    def save_to_file(self, text):
        try:
            path = filedialog.asksaveasfile(filetypes=(("Text document", "*.txt"), ("All Files", "*.*")),
                                            defaultextension=files)
            f = open(getattr(path, "name"), "w")
            f.write(text)
            f.close()
        except AttributeError:
            pass


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Generator silnego hasła!")
        self.root.geometry("650x450")
        self.root.configure(bg="#D3D3D3")

        self.password_generator = PasswordGenerator(self.root)
        self.clipboard_manager = ClipboardManager(self.root)
        self.file_manager = FileManager()

        label_frame = LabelFrame(self.root, text="Podaj długość hasła", font=20)
        label_frame.pack(pady=20)
        label_frame.configure(bg="gray")

        self.password_generator.length_pass = Entry(label_frame, font=("Verdana", 17))
        self.password_generator.length_pass.pack(pady=20, padx=50)

        label_frame2 = LabelFrame(self.root, text="Otrzymane hasło", font=20)
        label_frame2.pack(pady=30)
        label_frame2.configure(bg="orange")

        self.password_generator.received_pass = Entry(label_frame2, text="", font=("Verdana", 15), bd=0,
                                                      bg="systembuttonface")
        self.password_generator.received_pass.pack(pady=20, padx=40)

        check_box = Checkbutton(self.root, text="Znaki specjalne", variable=self.password_generator.checkChar,
                                onvalue=True, offvalue=False)
        check_box.pack(pady=10)

        check_number = Checkbutton(self.root, text="Liczby", variable=self.password_generator.checkNum,
                                onvalue=True, offvalue=False)
        check_number.pack(pady=20)

        my_frame = Frame(self.root)
        my_frame.pack()
        my_frame.configure(bg="#D3D3D3")

        generate_button = Button(my_frame, borderwidth='0', text="Generuj", font=22,
                                 command=self.password_generator.generate_password,
                                 activebackground="orange", width=7)
        generate_button.grid(row=0, column=0)
        generate_button.configure(bg="gray", font=("calibri", 12, "bold"))

        copy_button = Button(my_frame, borderwidth='0', text="Skopiuj", font=22,
                             command=self.copy_password, activebackground="orange",
                             width=7)
        copy_button.grid(row=0, column=1, padx=10)
        copy_button.configure(bg="gray", font=("calibri", 12, "bold"))

        save_button = Button(my_frame, borderwidth="0", text="Zapisz", font=22,
                             command=self.save_password, activebackground="orange",
                             width=7)
        save_button.grid(row=0, column=2)
        save_button.configure(bg="gray", font=("calibri", 12, "bold"))

        self.root.mainloop()

    def copy_password(self):
        text = self.password_generator.received_pass.get()
        self.clipboard_manager.copy_to_clipboard(text)

    def save_password(self):
        text = self.password_generator.received_pass.get()
        self.file_manager.save_to_file(text)


gui = GUI()
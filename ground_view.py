import tkinter

from tkinter import messagebox, simpledialog

import parametr
import messages
from model import Message

LABEL_TEXT = "ПОМНИ ПИЛОТ НЕ МОЖЕШЬ МГНОВЕННО ИЗМЕНИТЬ СВОЮ СКОРОСТЬ!"
LABEL_X_TEXT = "Горизонтальная скорость: X"
LABEL_Y_TEXT = "Вертикальная скорость: Y"
LABEL_R_TEXT = "Вращение: rotation"
LABEL_L1 = "Точка Лагранжа L1"
LABEL_POS = "Позиция корабля"

CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"


class GroundUI():
    def __init__(self, application, parent=None):
        self.application = application
        self.gui = parent
        self.frame = None
        self.left_frame = None
        self.speed_label = dict()
        self.pos_label = None
        self.lagrange_pos = None

    def show(self):
        self.gui = tkinter.Tk() if self.gui is None else self.gui
        self.gui.title(messages.TITLE)
        self.fill_frame()
        self.gui.protocol(CLOSING_PROTOCOL, self.on_closing)
        return self.input_dialogs()

    def fill_frame(self):

        self.left_frame = tkinter.Frame(self.gui)

        # LABELS
        label = tkinter.Label(self.left_frame, text=LABEL_TEXT)
        labelX = tkinter.Label(self.left_frame, text=LABEL_X_TEXT)
        labelY = tkinter.Label(self.left_frame, text=LABEL_Y_TEXT)
        labelR = tkinter.Label(self.left_frame, text=LABEL_R_TEXT)
        label_L1 = tkinter.Label(self.left_frame, text=LABEL_L1)
        label_pos_info = tkinter.Label(self.left_frame, text=LABEL_POS)
        self.pos_label = tkinter.Label(self.left_frame, text="*")
        self.lagrange_pos = tkinter.Label(self.left_frame, text="*")

        label.grid(column=0, row=0, columnspan=2)
        labelX.grid(column=0, row=2)
        labelY.grid(column=0, row=3)
        labelR.grid(column=0, row=4)
        label_L1.grid(column=0, row=5)
        self.lagrange_pos.grid(column=1, row=5)
        label_pos_info.grid(column=0, row=6)
        self.pos_label.grid(column=1, row=6)

        for index, param in enumerate(parametr.XYR):
            self.speed_label[param] = tkinter.Label(self.left_frame, text=param)
            self.speed_label[param].grid(column=1, row=(2 + index))

        # Menu
        menubar = tkinter.Menu(self.gui)
        menu = tkinter.Menu(menubar, tearoff=0)
        menu.add_command(label="Сохранить", command=self.application.send_save_state)
        menu.add_command(label="Загрузить", command=self.application.send_load_state)
        menubar.add_cascade(label="Игра", menu=menu)


        self.left_frame.grid(column=0, row=0, columnspan=2, rowspan=8)

        # chat
        self.frame = tkinter.Frame(self.gui)
        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame, state=TEXT_STATE_DISABLED)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message = tkinter.StringVar()
        self.frame.grid(column=2, row=0, columnspan=2, rowspan=4)
        self.input_field = tkinter.Entry(self.gui, textvariable=self.message, width=100)
        self.input_field.grid(column=2, row=5, columnspan=2)
        self.input_field.bind(KEY_RETURN, self.application.send)
        self.send_button = tkinter.Button(self.gui, text=messages.SEND, command=self.application.send)
        self.send_button.grid(column=2, row=6, columnspan=2)

        self.gui.config(menu=menubar)

    def input_dialogs(self):
        self.gui.lower()
        self.application.host = simpledialog.askstring(messages.SERVER_HOST, messages.INPUT_SERVER_HOST,
                                                       parent=self.gui)
        if self.application.host is None:
            return False
        self.application.port = simpledialog.askinteger(messages.SERVER_PORT, messages.INPUT_SERVER_PORT,
                                                        parent=self.gui)
        if self.application.port is None:
            return False
        return True


    def alert(self, title, message):
        messagebox.showerror(title, message)

    def show_speed_or_message(self, message: Message):
        if message.rocket_speed is not None:
            for param in parametr.XYR:
                self.speed_label[param]["text"] = message.rocket_speed[param]
        if message.rocket_pos is not None:
            self.pos_label["text"] = tuple(message.rocket_pos)
        if message.Lagrange_pos is not None:
            self.lagrange_pos["text"] = tuple(message.Lagrange_pos)
        if message.message is not None:
            self.show_message(message)

    def show_message(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)
        self.message_list.configure(state=TEXT_STATE_DISABLED)

    def loop(self):
        self.gui.mainloop()

    def on_closing(self):
        self.application.exit()
        self.gui.destroy()


if __name__ == '__main__':
    main_obj = GroundUI(None)
    main_obj.show()
    main_obj.loop()

# -*- coding: utf-8 -*-
import random
import tkinter
from tkinter import messagebox, simpledialog

import parametr
import messages

LABEL_TEXT = "ПОМНИ ПИЛОТ!\n ТЫ НЕ МОЖЕШЬ МГНОВЕННО ИЗМЕНИТЬ СВОЮ СКОРОСТЬ!"
LABEL_X_TEXT = "Изменить горизонтальную скорость: X"
LABEL_Y_TEXT = "Изменить вертикальную скорость: Y"
LABEL_R_TEXT = "Изменить вращение: rotation"

CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"


class RocketUI():
    def __init__(self, application, parent=None):
        self.application = application
        self.gui = parent
        self.frame = None

        self.input_fields = dict()
        self.left_frame = None
        self.right_frame = None
        self.send_speed_btn = None

        self.input_field = None
        self.speed = dict()
        self.message = None
        self.message_list = None
        self.scrollbar = None
        self.send_msg_btn = None

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

        label.grid(column=0, row=0, columnspan=2)
        labelX.grid(column=0, row=2)
        labelY.grid(column=0, row=3)
        labelR.grid(column=0, row=4)

        # SpinBoxes
        for index, param in enumerate(parametr.XYR):
            self.speed[param] = tkinter.IntVar()
            self.input_fields[param] = tkinter.Spinbox(self.left_frame,
                                                       increment=1,
                                                       from_=parametr.MIN_SPEED[param],
                                                       to=parametr.MAX_SPEED[param],
                                                       textvariable=self.speed[param],
                                                       state="readonly")
            self.input_fields[param].grid(column=1, row=(2 + index))
        self.reset_values()

        # Buttons
        btn = tkinter.Button(self.left_frame, text="Сбросить значения", command=self.reset_values)
        self.send_speed_btn = tkinter.Button(self.left_frame,
                                             text="Изменить скорость", command=self.application.send_speed)
        # self.send_speed_btn.bind(KEY_RETURN, self.application.send)
        btn.grid(column=0, row=5, columnspan=2)
        self.send_speed_btn.grid(column=0, row=6, columnspan=2)

        self.left_frame.grid(column=0, row=0, columnspan=2, rowspan=6)

        self.right_frame = tkinter.Frame(self.gui)

        # chat
        self.frame = tkinter.Frame(self.right_frame)
        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame, state=TEXT_STATE_DISABLED)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message = tkinter.StringVar()
        self.frame.pack()
        self.input_field = tkinter.Entry(self.right_frame, textvariable=self.message, width=100)
        self.input_field.pack()
        # self.input_field.bind(KEY_RETURN, self.application.send)
        self.send_msg_btn = tkinter.Button(self.right_frame, text=messages.SEND, command=self.application.send)
        self.send_msg_btn.pack()

        self.right_frame.grid(column=2, row=0, columnspan=2, rowspan=6)

    def input_dialogs(self):
        self.gui.lower()
        self.application.username = messages.USERNAME_ROCKET
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

    def show_message(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)
        self.message_list.configure(state=TEXT_STATE_DISABLED)

    def loop(self):
        self.gui.mainloop()

    def reset_values(self):
        self.speed[parametr.X].set(0)
        self.speed[parametr.Y].set(0)
        self.speed[parametr.R].set(0)

    def on_closing(self):
        self.application.exit()
        self.gui.destroy()


if __name__ == '__main__':
    main_obj = RocketUI(None)
    main_obj.show()
    main_obj.loop()

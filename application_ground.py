# -*- coding: utf-8 -*-
import json
import socket
import threading
from tkinter import messagebox

import messages
import model
import parametr
from ground_view import GroundUI


BUFFER_SIZE = 2 ** 10


class Application(object):
    instance = None

    def __init__(self, args):
        self.args = args
        self.closing = False
        self.host = None
        self.port = None
        self.receive_worker = None
        self.sock = None
        self.username = messages.USERNAME_GROUND
        self.ui = GroundUI(self)
        self.rocket_pos = None
        self.rocket_speed = None
        self.L1_pos = None
        Application.instance = self

    def execute(self):
        if not self.ui.show():
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except (socket.error, OverflowError):
            self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
            return
        # send to server msg to say self type
        message = model.Message(username=self.username, quit=False, message="")
        try:
            temp_test = message.marshal()
            print(temp_test)
            self.sock.sendall(temp_test)
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)

        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.ui.loop()

    # ============================= Save and Load State ================================================
    def send_load_state(self):
        if messagebox.askokcancel(messages.USERNAME_VOICE,messages.IS_LOAD_STATE_QUESTION):
            self.send_load_save_msg(parametr.LOAD_STATE)

    def send_save_state(self):
        if messagebox.askokcancel(messages.USERNAME_VOICE,messages.IS_SAVE_STATE_QUESTION):
            self.send_load_save_msg(parametr.SAVE_STATE)

    def send_load_save_msg(self, load_save_param: str):
        message = model.Message(username=messages.USERNAME_ROCKET, save_load_state=load_save_param, message="",
                                quit=False)
        try:
            temp_test = message.marshal()
            print(temp_test)
            self.sock.sendall(temp_test)
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)

    # ====================== receive from server methods ================================================
    def receive(self):
        while True:
            try:
                message = model.Message(**json.loads(self.receive_all()))
            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
                return
            self.ui.show_speed_or_message(message)

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += self.sock.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    # ====================== Send some msg to server methods ============================================
    def get_message(self):
        message = self.ui.message.get()
        if len(message) == 0:
            return
        self.ui.message.set("")
        return model.Message(username=self.username, message=message, quit=False)

    def send(self, event=None):
        message = self.get_message()
        print(message)
        if message is None:
            return
        try:
            temp_test = message.marshal()
            print(temp_test)
            self.sock.sendall(temp_test)
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)

    def exit(self):
        self.closing = True
        try:
            self.sock.sendall(model.Message(username=self.username, message="", quit=True).marshal())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print(messages.CONNECTION_ERROR)
        finally:
            self.sock.close()

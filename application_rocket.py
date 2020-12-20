# -*- coding: utf-8 -*-
import json
import socket
import threading

import messages
import parametr
import model
from rocket_view import RocketUI

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
        self.username = messages.USERNAME_ROCKET
        self.r_ui = RocketUI(self)
        Application.instance = self

    def execute(self):
        if not self.r_ui.show():
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except (socket.error, OverflowError):
            self.r_ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
            return

        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.r_ui.loop()

    def receive(self):
        while True:
            try:
                message = model.Message(**json.loads(self.receive_all()))
            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    self.r_ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
                return
            self.r_ui.show_message(message)

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += self.sock.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    def get_message_to_send(self):
        message = self.r_ui.message.get()
        if len(message) == 0:
            return
        self.r_ui.message.set("")
        return model.Message(username=self.username, message=message, quit=False)

    def send(self, event=None):
        message = self.get_message_to_send()
        if message is None:
            return
        try:
            temp_test = message.marshal()
            print(temp_test)
            self.sock.sendall(temp_test)
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.r_ui.alert(messages.ERROR, messages.CONNECTION_ERROR)

    def get_speed_to_send(self):
        speed = self.r_ui.get_speed()
        if all([speed[param] == 0 for param in parametr.XYR]):
            return

        return model.Message(username=self.username, rocket_speed=speed, message="", quit=False)

    def send_speed(self, event=None):
        message = self.get_speed_to_send()
        if message is None:
            return
        try:
            temp_test = message.marshal()
            print(temp_test)
            self.sock.sendall(temp_test)
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.r_ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
        # print message into message list
        msg_to_pilot = "Command of changing speed [on X: %d, on Y: %d, rotation on %d] accepted" % (
            message.get_speed_list_XYR())
        self.r_ui.show_message(msg_to_pilot)

    def exit(self):
        self.closing = True
        try:
            self.sock.sendall(model.Message(username=self.username, message="", quit=True).marshal())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print(messages.CONNECTION_ERROR)
        finally:
            self.sock.close()

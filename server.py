# -*- coding: utf-8 -*-
import json
import socket
import sys
import threading
import time
import random

from jsonschema import validate, Draft4Validator

import state_schema_json
import model
import state
import parametr
import messages

BUFFER_SIZE = 2 ** 10
CLOSING = "Application closing..."
CONNECTION_ABORTED = "Connection aborted"
CONNECTED_PATTERN = "Client connected: {}:{}"
ERROR_ARGUMENTS = "Provide port number as the first command line argument"
ERROR_OCCURRED = "Error Occurred"
EXIT = "exit"
JOIN_PATTERN = "{username} has joined"
RUNNING = "Server is running..."
SERVER = "SERVER"
SHUTDOWN_MESSAGE = "shutdown"
TYPE_EXIT = "Type 'exit' to exit>"


class Server(object):

    def __init__(self, argv):
        self.clients = set()
        self.listen_thread = None
        self.port = None
        self.sock = None
        self.parse_args(argv)
        self.timer_thread = None
        self.timer_tic = parametr.SEND_EVERY_N_TIMER_TIC
        self.ground_client = None

        self.end_of_game = False
        self.is_save_load_state = False
        self.change_of_speed = dict()
        self.speed = dict()
        self.rocket_pos = None
        self.L1 = None
        self.init_random_var()

    def init_random_var(self):
        # speed
        for param in parametr.XYR:
            self.speed[param] = random.randint(parametr.MIN_SPEED[param] // 2, parametr.MAX_SPEED[param] // 2)
            self.change_of_speed[param] = 0
        # pos
        self.rocket_pos = []
        self.L1 = []
        for param in parametr.XY:
            self.rocket_pos.append(
                random.randint(parametr.MIN_VAL_GEN_POS[param], parametr.MAX_VAL_GEN_POS[param])
            )
            self.L1.append(
                random.randint(parametr.MIN_VAL_GEN_POS[param], parametr.MAX_VAL_GEN_POS[param])
            )

    def save_state_to_file(self, stat: state.State):
        if (Draft4Validator(state_schema_json.schema).is_valid(stat)):
            with open(parametr.JSON_FILENAME, "w") as file:
                json.dump(stat, file, indent=4)
        else:
            print("The message doesn't match the schema")

    def load_state_from_file(self):
        stat = None
        try:
            with open(parametr.JSON_FILENAME) as file:
                file_content = file.read().strip()
                if len(file_content):
                    stat = state.State(**json.loads(file_content))
        except FileNotFoundError:
            print("File didn't found")
            return None
        except json.JSONDecodeError:  # Некорректное содержимое файла
            return None

        if not Draft4Validator(state_schema_json.schema).is_valid(stat):
            print("State doesn't math the schema")
            stat = None
        return stat

    def listen(self):
        self.sock.listen(2)
        while len(self.clients) < 2:
            try:
                client, address = self.sock.accept()
                print("Client connect")
            except OSError:
                print(CONNECTION_ABORTED)
                return
            print(CONNECTED_PATTERN.format(*address))
            self.clients.add(client)
            threading.Thread(target=self.handle, args=(client,)).start()

    def get_change_speed(self):
        change_speed_on_server_on = dict()
        for param in parametr.XYR:
            if self.change_of_speed[param] != 0:
                if abs(self.change_of_speed[param]) > parametr.CHANGE_SPEED_PER_UPDATE[param]:
                    cond_int = int(self.change_of_speed[param] > 0)
                    add = parametr.CHANGE_SPEED_PER_UPDATE[param] * (-1) ** cond_int
                    self.change_of_speed[param] = self.change_of_speed[param] + add
                    change_speed_on_server_on[param] = -add
                else:
                    change_speed_on_server_on[param] = self.change_of_speed[param]
                    self.change_of_speed[param] = 0
            else:
                change_speed_on_server_on[param] = 0
        return change_speed_on_server_on

    def update_speed_and_pos(self):

        print("rocket pos old ", self.rocket_pos)
        for i, param in enumerate(parametr.XY):
            self.rocket_pos[i] += self.speed[param]

        print("rocket pos new ", self.rocket_pos)
        print("rocket sped old ", self.speed)
        change_speed_on_server_on = self.get_change_speed()
        for param in parametr.XYR:
            self.speed[param] += change_speed_on_server_on[param]
            change_speed_on_server_on[param] = 0
            print("rocket sped new", self.speed, "\n\n")

    def timer_update_param(self):
        while not self.is_save_load_state:
            self.timer_tic += 1
            self.update_speed_and_pos()
            self.end_of_game = self.is_win()
            if not self.end_of_game:
                if self.timer_tic >= parametr.SEND_EVERY_N_TIMER_TIC:
                    self.timer_tic = 0
                    message = model.Message(username=messages.USERNAME_SERVER, rocket_pos=self.rocket_pos,
                                            rocket_speed=self.speed, Lagrange_pos=self.L1)
                    self.ground_client.sendall(message.marshal())
                time.sleep(parametr.TIME_TO_UPDATE_SPEED_ML / 1000)
            else:
                message = model.Message(username=messages.USERNAME_VOICE, message="YOU WON", quit=False)
                self.broadcast(message)
                break

    def handle_rocket_msg(self, message: model.Message):
        if message.message != "":
            time.sleep(parametr.MESSAGE_DELAY_SEC)
            self.broadcast(message)
        if message.rocket_speed is not None:
            for param in parametr.XYR:
                self.change_of_speed[param] += message.rocket_speed[param]

    def is_win(self):
        ans = True
        for i in range(parametr.DIMENSION):
            if self.rocket_pos[i] != self.L1[i]:
                ans = False
                break
        if ans:
            for param in parametr.XYR:
                if self.speed[param] != 0:
                    ans = False
                    break
        return ans

    def handle_save_load_state(self, message: model.Message):
        answer_msg = ""
        if message.save_load_state == parametr.LOAD_STATE:
            stat = self.load_state_from_file()
            if stat:
                self.speed = stat.speed
                self.rocket_pos = stat.rocket_pos
                self.change_of_speed = stat.change_of_speed
                self.L1 = stat.L1
                answer_msg = f"State of game have loaded by {message.username}"
            else:
                answer_msg = "Could not to load latest state of game"
        elif message.save_load_state == parametr.SAVE_STATE:
            stat = state.State()
            stat.speed = self.speed
            stat.rocket_pos = self.rocket_pos
            stat.change_of_speed = self.change_of_speed
            stat.L1 = self.L1
            self.save_state_to_file(stat)
            answer_msg = f"State of game have saved by {message.username}"

        msg = model.Message(username=messages.USERNAME_VOICE, message=answer_msg, quit=False)
        self.broadcast(msg)

    def handle(self, client):
        while True:
            try:
                message = model.Message(**json.loads(self.receive(client)))
            except (ConnectionAbortedError, ConnectionResetError):
                print(CONNECTION_ABORTED)
                return
            if message.quit:
                client.close()
                self.clients.remove(client)
                return

            print(str(message))
            if SHUTDOWN_MESSAGE.lower() == message.message.lower():
                self.exit()
                return

            if message.save_load_state:
                self.is_save_load_state = True
                self.handle_save_load_state(message)

            if not self.is_save_load_state:
                if message.username == messages.USERNAME_ROCKET:
                    self.handle_rocket_msg(message)
                elif message.username == messages.USERNAME_GROUND:
                    if self.ground_client is None:
                        self.ground_client = client
                        self.timer_thread = threading.Thread(target=self.timer_update_param)
                        self.timer_thread.start()
                    else:
                        time.sleep(parametr.MESSAGE_DELAY_SEC)
                        self.broadcast(message)

    def broadcast(self, message):
        for client in self.clients:
            client.sendall(message.marshal())

    def receive(self, client):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += client.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    def run(self):
        print(RUNNING)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def parse_args(self, argv):
        if len(argv) != 2:
            raise RuntimeError(ERROR_ARGUMENTS)
        try:
            self.port = int(argv[1])
        except ValueError:
            raise RuntimeError(ERROR_ARGUMENTS)

    def exit(self):
        self.sock.close()
        for client in self.clients:
            client.close()
        print(CLOSING)


if __name__ == "__main__":
    try:
        Server(sys.argv).run()
    except RuntimeError as error:
        print(ERROR_OCCURRED)
        print(str(error))

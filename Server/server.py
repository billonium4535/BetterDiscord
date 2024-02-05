import socket
import threading

from server_client_connection import server_socket_setup
from get_version import get_version
import http_server


class Server:
    def __init__(self):
        self.running = True
        self.server_host = '0.0.0.0'
        self.sending_audio_socket = server_socket_setup(self.server_host, 8450, socket.AF_INET, socket.SOCK_STREAM, 5)
        self.receiving_audio_socket = server_socket_setup(self.server_host, 8451, socket.AF_INET, socket.SOCK_STREAM, 5)
        # self.sending_messages_socket = server_socket_setup(self.server_host, 8452, socket.AF_INET, socket.SOCK_STREAM, 5)
        # self.receiving_messages_socket = server_socket_setup(self.server_host, 8453, socket.AF_INET, socket.SOCK_STREAM, 5)
        # self.receiving_old_messages_socket = server_socket_setup(self.server_host, 8454, socket.AF_INET, socket.SOCK_STREAM, 5)
        # self.sending_screenshare_socket = server_socket_setup(self.server_host, 8455, socket.AF_INET, socket.SOCK_STREAM, 5)
        # self.receiving_screenshare_socket = server_socket_setup(self.server_host, 8456, socket.AF_INET, socket.SOCK_STREAM, 5)
        self.updater_socket = server_socket_setup(self.server_host, 8457, socket.AF_INET, socket.SOCK_STREAM, 5)
        self.data_socket = server_socket_setup(self.server_host, 8458, socket.AF_INET, socket.SOCK_STREAM, 5)

        self.http_server_thread = threading.Thread(target=http_server.start_server)

        self.connected_clients = []
        self.connected_addresses = []
        self.client_audio_data = {}
        self.clients_in_call = []

        self.version = get_version()

        self.run()

    def listen_for_clients(self):
        sockets_to_listen = [
            self.sending_audio_socket,
            self.receiving_audio_socket,
            # self.sending_messages_socket,
            # self.receiving_messages_socket,
            # self.receiving_old_messages_socket,
            # self.sending_screenshare_socket,
            # self.receiving_screenshare_socket,
            self.updater_socket,
            self.data_socket
        ]

        for server_socket in sockets_to_listen:
            server_socket.settimeout(1)
            try:
                client_socket, client_address = server_socket.accept()
                self.connected_clients.append(client_socket)
                self.connected_addresses.append(client_address)

                server_socket.settimeout(None)

                if server_socket == self.sending_audio_socket:
                    threading.Thread(target=self.client_sending_audio, args=[client_socket]).start()
                elif server_socket == self.receiving_audio_socket:
                    threading.Thread(target=self.client_receiving_audio, args=[client_socket]).start()
                elif server_socket == self.updater_socket:
                    threading.Thread(target=self.client_updater, args=[client_socket]).start()
                elif server_socket == self.data_socket:
                    threading.Thread(target=self.data_handling, args=[client_socket]).start()
            except:
                pass

    def client_disconnect(self, client_socket):
        if client_socket in self.client_audio_data:
            del self.client_audio_data[client_socket]
        if client_socket.getpeername()[0] in self.clients_in_call:
            self.clients_in_call.remove(client_socket.getpeername()[0])
        client_socket.close()

    def client_sending_audio(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.send(data)
                # self.client_audio_data[client_socket] = data
        except Exception as e:
            print(e)
        finally:
            self.client_disconnect(client_socket)

    def client_receiving_audio(self, client_socket):
        try:
            while self.running:
                pass
                # merged_audio = b"".join([audio_data for sock, audio_data in self.client_audio_data.items() if sock != client_socket])
                # for sock in self.client_audio_data.keys():
                #     if sock != client_socket:
                #         sock.send(merged_audio)
        except Exception as e:
            print(e)
        finally:
            self.client_disconnect(client_socket)

    def client_updater(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024).decode('windows-1252')
                if not data:
                    break
                if data == "CONNECTION_CHECK":
                    client_socket.send("200 OK".encode('windows-1252'))
                if data == "GET_VERSION":
                    client_socket.send(self.version.encode('windows-1252'))
        except Exception as e:
            print(e)
        finally:
            self.client_disconnect(client_socket)

    def data_handling(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(1024).decode('windows-1252')
                if not data:
                    break
                if data == "CONNECTION_CHECK":
                    client_socket.send("200 OK".encode('windows-1252'))
                    client_socket.send(f"{self.clients_in_call}".encode('windows-1252'))
                if data == "JOIN_CALL":
                    if client_socket.getpeername()[0] not in self.clients_in_call:
                        self.clients_in_call.append(client_socket.getpeername()[0])
                    client_socket.send("200 CALL_JOINED".encode('windows-1252'))
                    client_socket.send(f"{self.clients_in_call}".encode('windows-1252'))
                if data == "LEAVE_CALL":
                    self.clients_in_call.remove(client_socket.getpeername()[0])
                    client_socket.send("200 CALL_LEFT".encode('windows-1252'))
                    client_socket.send(f"{self.clients_in_call}".encode('windows-1252'))
        except Exception as e:
            print(e)
        finally:
            self.client_disconnect(client_socket)

    def run(self):
        while self.running:
            self.listen_for_clients()
            if not self.http_server_thread.is_alive():
                self.http_server_thread.start()
                print("started")


Server()

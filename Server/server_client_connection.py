import socket


def server_socket_setup(server_ip, server_port, address_family, socket_kind, max_backlog):
    server_socket = socket.socket(address_family, socket_kind)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(max_backlog)
    return server_socket

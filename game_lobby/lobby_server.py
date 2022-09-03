import socket
import os
import sys
import threading
import json

MAX_PLAYER_NUM = int(os.getenv("MAX_PLAYER_NUM", 4)) # default player num is 4
PLAYER_NUM = 0

GAME_PORT = 8888 # game server port
INFO_PORT = 9999 # port returning current number of players
HOST = '0.0.0.0'

game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
info_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# I N F O   S E R V E R
def info_server(host, port):
    try:
        info_socket.bind((host,port))
    except socket.error as e:
        print('Bind failed. Error Code:'
            + str(e[0]) + ' Message ' + e[1])
        sys.exit()
    
    info_socket.listen()

    while True:
        conn, addr = info_socket.accept()
        send_info(conn, addr)

def send_info(conn, addr):
    conn.send(bytearray(json.dumps({"MAX_PLAYERS": MAX_PLAYER_NUM, "CONNECTED_PLAYERS": PLAYER_NUM}), encoding="utf-8"))

# G A M E   S E R V E R
def game_server(host, port):
    global PLAYER_NUM
    # bind socket
    try:
        game_socket.bind((host, port))
    except socket.error as e:
        print('Bind failed. Error Code:'
            + str(e[0]) + ' Message ' + e[1])
        sys.exit()

    # start listener
    game_socket.listen()

    while True:
        # accept & connect to client
        conn, addr = game_socket.accept()
        PLAYER_NUM += 1
        threading.Thread(None, handle_game_client, args=(conn,addr)).start()

def handle_game_client(conn, addr):
    global PLAYER_NUM
    while True:
        data = conn.recv(1024)
        if not data:
            print('Bye')
            PLAYER_NUM -= 1
            break
        
        data = data[::-1] # reverse string, this is just to test
        conn.send(data)
    conn.close()

threading.Thread(target=game_server, args=(HOST, GAME_PORT)).start()
info_server(HOST, INFO_PORT)
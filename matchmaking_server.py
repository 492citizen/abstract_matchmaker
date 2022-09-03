#! /usr/bin/python3

import time
import docker
import os
import socket

image_name = "game_lobby"
client = docker.from_env()

class game_lobby:
    def __init__(self, container):
        self.container = container

    @property
    def connected_players(self):
        player_probe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player_probe_socket.connect((self.host_ip, int(self.info_port)))
        reply = player_probe_socket.recv(4096)
        player_probe_socket.close()
        return reply

    @property
    def host_ip(self):
        return self.container.ports['8888/tcp'][0]['HostIp']

    @property
    def game_port(self):
        return self.container.ports['8888/tcp'][0]['HostPort']

    @property
    def info_port(self):
        return self.container.ports['9999/tcp'][0]['HostPort']


def list_lobbies(hide_full=False):
    return [container for container in client.containers.list() if container.attrs['Config']['Image'] == "game_lobby"]

def start_new_lobby(player_num, game_port, info_port):
    return client.containers.run("game_lobby", detach=True, environment=[f"MAX_PLAYER_NUM={player_num}"],
                                ports={8888:game_port, 9999:info_port}, remove=True) # bind port 8888 from container to "port" on host machine

start_new_lobby(4, 8880, 8881)
start_new_lobby(2, 8890, 8891)
start_new_lobby(6, 8900, 8901)
start_new_lobby(4, 8910, 8911)

while True:
    time.sleep(2)
    for i in range(100): # clear screen
        print("\n")
    print("Running Containers: ")
    for container in list_lobbies():
        lobby = game_lobby(container)
        print(f"IP: {lobby.host_ip}, GAME_PORT {lobby.game_port}, INFO_PORT {lobby.info_port}, NAME: {lobby.container.attrs['Name']} {lobby.connected_players}")
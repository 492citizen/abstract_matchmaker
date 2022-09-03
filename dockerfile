# This is the dockerfile for one game lobby

FROM ubuntu

RUN apt-get update && apt-get install -y python3 && apt-get clean
RUN mkdir /game_lobby

COPY game_lobby/ /game_lobby

WORKDIR /game_lobby

CMD ["/usr/bin/python3", "lobby_server.py"]

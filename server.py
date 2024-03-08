import socket
from _thread import *
import pickle
from game import Game
import struct

server = "192.168.1.7"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    print("Player",p," connected")

    reply = ""
    while True:
        try:
            data = conn.recv(4096)
            game  = games[gameId]
            # Giải mã dữ liệu nhận được
            received_object = pickle.loads(data)
            if not received_object:
                break
            else:
                # Xác định loại đối tượng nhận được và xử lý tương ứng
                if isinstance(received_object, str):
                    if received_object == "reset":
                        print("reset game")
                        game.resetGame()
                    elif data != "get":
                        pass
                        # game.play(p, data)
                    games[gameId] = game
                    conn.sendall(pickle.dumps(game))
                elif isinstance(received_object, Game):
                    games[gameId] = received_object
                    conn.sendall(pickle.dumps(received_object))

        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


player = ["X","O"]
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, player[p], gameId))
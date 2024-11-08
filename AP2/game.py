import turtle
import time
import random
import mqtt_pub
import mqtt_sub
import threading

delay = 0.01

# Score
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Move Game by @Garrocho")
wn.bgcolor("gray")
wn.setup(width=600, height=600, startx=None, starty=None)
wn.tracer(0) # Turns off the screen updates

players = {}  # Dicionário para armazenar os jogadores (outros)
last_position = (0, 0)  # Para verificar se a posição do jogador mudou

# Função para criar um jogador (bola)
def create_player(color):
    player = turtle.Turtle()
    player.speed(0)
    player.shape("circle")
    player.color(color)
    player.penup()
    player.id = random.randint(1000, 9999)  # Gerar ID único para o jogador
    return player

# Definindo o jogador principal (bola do jogador)
head_color = random.choice(["red", "blue", "green", "yellow", "purple", "black","pink","orange"])  # Cor aleatória
head = create_player(head_color)
head.goto(0, 0)
head.direction = "stop"

def update_players(message):
    global last_position
    if (message["x"], message["y"]) != last_position:
        last_position = (message["x"], message["y"])
        players[message["player_id"]] = message
    else:
       for player_id, player_data in players.items():
            color = player_data["color"]
            print(f"Adicionando jogador {player_id} com cor {color}")
            new_player = create_player(color)
            new_player.goto(player_data["x"], player_data["y"])
            


# Functions
def go_up():
    head.direction = "up"

def go_down():
    head.direction = "down"

def go_left():
    head.direction = "left"

def go_right():
    head.direction = "right"

def stop():
    head.direction = "stop"

def close():
    wn.bye()

def move(pub):
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 2)
        pub.publish(head.id,  head.xcor(), head.ycor(),head.direction,head.color()[0]) 

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 2)
        pub.publish(head.id, head.xcor(), head.ycor(),head.direction,head.color()[0]) 


    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 2)
        pub.publish(head.id, head.xcor(), head.ycor(),head.direction,head.color()[0]) 


    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 2)
        pub.publish(head.id,  head.xcor(), head.ycor(),head.direction,head.color()[0]) 


# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")
wn.onkeypress(stop, "Return")

def main():
    broker = "localhost"  # Endereço do broker MQTT
    port = 1883  # Porta padrão para MQTT
    topic = "game/move"

    actual_player_id = head.id

    pub = mqtt_pub.MQTTPublisher(broker,port,topic)
    sub = mqtt_sub.MQTTSubscriber(broker,port,topic,actual_player_id)

    sub_thread = threading.Thread(target=sub.start)
    sub_thread.start()
    

    # Main game loop
    while True:
        wn.update()
        move(pub)
        time.sleep(delay)

    wn.mainloop()

if __name__ == '__main__':
    main()
from queue import Queue
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
wn.title("Move Game by Gaby and Mariana")
wn.bgcolor("gray")
wn.setup(width=600, height=600, startx=None, starty=None)
wn.tracer(0) # Turns off the screen updates

players = {}  # Dicionário para armazenar os jogadores (outros)
last_position = (0, 0)  # Para verificar se a posição do jogador mudou
# Queue for storing messages from the subscriber
message_queue = Queue()

# Função para criar um jogador (bola)
def create_player(color):
    player = turtle.Turtle()
    player.speed(0)
    player.shape("circle")
    player.color(color)
    player.penup()
    player.id = random.randint(1000, 9999)  # Gerar ID único para o jogador
    player.time = time.time()
    player.goto(0,0)
    player.direction = "stop"
    return player

def create_text():
    text = turtle.Turtle()
    text.color("black")
    text.penup()
    text.hideturtle()
    return text

# Definindo o jogador principal (bola do jogador)
head_color = random.choice(["red", "blue", "green", "yellow", "purple", "black","pink","orange"])  # Cor aleatória
head = create_player(head_color)
text = create_text()

def update_players(message):
    global last_position
    print(f"Update player: {message}")
    player_id = message["player_id"]
    print(f"Players: {players}")
    if player_id in players:
        # Update existing player if position changed
        if (message["x"], message["y"]) != last_position:
            last_position = (message["x"], message["y"])
            players[player_id].goto(message["x"], message["y"])  # Update position directly
    else:
        # Add new player if not already present
        players[player_id] = create_player(message["color"])
        players[player_id].goto(message["x"], message["y"])
        players[player_id].showturtle()
        
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
    move_time = time.time()
    head.time = move_time

    text.clear()
    text.goto(head.xcor(), head.ycor() + 10)  # Posicionar o texto acima do círculo
    text.write(head.id, align="center", font=("Arial", 12, "normal"))

    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 2)
        pub.publish(head.id,  head.xcor(), head.ycor(),head.direction,head.color()[0],move_time) 

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 2)
        pub.publish(head.id, head.xcor(), head.ycor(),head.direction,head.color()[0],move_time) 


    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 2)
        pub.publish(head.id, head.xcor(), head.ycor(),head.direction,head.color()[0],move_time) 


    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 2)
        pub.publish(head.id,  head.xcor(), head.ycor(),head.direction,head.color()[0],move_time) 


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

    global head
    actual_player_id = head.id

    pub = mqtt_pub.MQTTPublisher(broker,port,topic)
    sub = mqtt_sub.MQTTSubscriber(broker,port,topic,actual_player_id,message_queue)

    sub_thread = threading.Thread(target=sub.start)
    sub_thread.start()
    
    while True:
        wn.update()
        move(pub)
        # Check for messages in the queue
        if not message_queue.empty():
            message = message_queue.get()
            update_players(message)

        time.sleep(delay)


if __name__ == '__main__':
    main()
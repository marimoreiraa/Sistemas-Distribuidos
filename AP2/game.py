import turtle
import time
import subprocess

delay = 0.01  # Intervalo para o movimento

# Configuração da tela do jogo
wn = turtle.Screen()
wn.title("Move Game by Gabrielle Fonseca and Mariana Moreira")  # Título da janela
wn.bgcolor("grey")  # Cor de fundo da janela
wn.setup(width=1.0, height=1.0, startx=None, starty=None)  # Ajuste da tela
wn.tracer(0)  # Desativa atualização automática da tela

# Definindo os limites da tela com buffer para evitar colisão direta nas bordas
BORDER_LEFT = -wn.window_width() / 2 + 10
BORDER_RIGHT = wn.window_width() / 2 - 20
BORDER_TOP = wn.window_height() / 2 - 10
BORDER_BOTTOM = -wn.window_height() / 2 + 20

# Jogador principal (a "bola" que se move)
head = turtle.Turtle()
head.speed(0)  # Velocidade do movimento (0 = mais rápido)
head.shape("circle")  # Forma da "bola"
head.color("red")  # Cor da "bola"
head.penup()  # Desativa o rastreamento (não desenha linha)
head.goto(0, 0)  # Posição inicial
head.direction = "stop"  # Direção inicial da "bola"

movimentos_recebidos = []  # Lista para armazenar os movimentos de outros jogadores


# Funções para controle de movimento e publicação no MQTT
def go_up():
    head.direction = "up"  # Define a direção
    subprocess.Popen(
        ["python3", "pub.py", "up"]
    )  # Envia o comando para o servidor MQTT


def go_down():
    head.direction = "down"
    subprocess.Popen(["python3", "pub.py", "down"])


def go_left():
    head.direction = "left"
    subprocess.Popen(["python3", "pub.py", "left"])


def go_right():
    head.direction = "right"
    subprocess.Popen(["python3", "pub.py", "right"])


def close():
    wn.bye()  # Fecha a janela do jogo quando pressionar 'Escape'


# Função para mover a bola
def move():
    # Movimentos locais do jogador, respeitando os limites da tela
    if head.direction == "up" and head.ycor() < BORDER_TOP:
        head.sety(head.ycor() + 2)  # Move para cima
    elif head.direction == "down" and head.ycor() > BORDER_BOTTOM:
        head.sety(head.ycor() - 2)  # Move para baixo
    elif head.direction == "left" and head.xcor() > BORDER_LEFT:
        head.setx(head.xcor() - 2)  # Move para a esquerda
    elif head.direction == "right" and head.xcor() < BORDER_RIGHT:
        head.setx(head.xcor() + 2)  # Move para a direita

    # Movimentos recebidos de outros jogadores (atualização da tela)
    global movimentos_recebidos
    for movimento in movimentos_recebidos:
        device_id, direction = movimento.split(": ")
        if direction == "up" and head.ycor() < BORDER_TOP:
            head.sety(head.ycor() + 2)
        elif direction == "down" and head.ycor() > BORDER_BOTTOM:
            head.sety(head.ycor() - 2)
        elif direction == "left" and head.xcor() > BORDER_LEFT:
            head.setx(head.xcor() - 2)
        elif direction == "right" and head.xcor() < BORDER_RIGHT:
            head.setx(head.xcor() + 2)


# Ligações de teclado para controle do movimento
wn.listen()  # Espera por eventos de teclado
wn.onkeypress(go_up, "w")  # Pressionar 'w' move para cima
wn.onkeypress(go_down, "s")  # Pressionar 's' move para baixo
wn.onkeypress(go_left, "a")  # Pressionar 'a' move para a esquerda
wn.onkeypress(go_right, "d")  # Pressionar 'd' move para a direita
wn.onkeypress(close, "Escape")  # Pressionar 'Escape' fecha o jogo

# Loop principal do jogo
while True:
    wn.update()  # Atualiza a tela
    move()  # Move a bola
    time.sleep(delay)  # Controla a velocidade do movimento

wn.mainloop()  # Executa o jogo (fica esperando por eventos)

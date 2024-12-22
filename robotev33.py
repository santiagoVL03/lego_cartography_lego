#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait


# Inicializar ladrillo EV3 y dispositivos
brick = EV3Brick()
motor_left = Motor(Port.A)
motor_right = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)

# Configuración de movimiento
DRIVE_SPEED = 100
TURN_SPEED = 50
CELL_SIZE = 100

# Configuración de la cuadrícula
GRID_SIZE = 5
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
x, y = 0, 0
direction = "right"


def imprimir_cuadricula():
    brick.screen.clear()
    for fila in grid:
        linea = brick.screen.print(" ".join(fila))
        brick.screen.print(linea)
    wait(500)


def avanzar_10cm():
    motor_left.run_angle(DRIVE_SPEED, 204.5, Stop.BRAKE, wait=False)
    motor_right.run_angle(DRIVE_SPEED, 204.5, Stop.BRAKE, wait=True)
    istrue = detectar_objeto()
    if istrue == True:
        cambiar_direccion_por_objeto()
    actualizar_posicion()


def retroceder():
    motor_left.run_angle(DRIVE_SPEED, -204.5, Stop.BRAKE, wait=False)
    motor_right.run_angle(DRIVE_SPEED, -204.5, Stop.BRAKE, wait=True)


def girar_derecha():
    """Girar 90 grados a la derecha."""
    motor_left.run_angle(TURN_SPEED, 180, Stop.BRAKE, wait=False)
    motor_right.run_angle(TURN_SPEED, -180, Stop.BRAKE, wait=True)


def girar_izquierda():
    """Girar 90 grados a la izquierda."""
    motor_left.run_angle(TURN_SPEED, -180, Stop.BRAKE, wait=False)
    motor_right.run_angle(TURN_SPEED, 180, Stop.BRAKE, wait=True)


def detectar_objeto():
    distancia = ultrasonic_sensor.distance()
    color_detectado = color_sensor.color()

    if distancia < 100:  # Obstáculo cercano
        brick.speaker.beep()
        brick.screen.clear()
        wait(100)
        return True
    if color_detectado == Color.BLACK:  # Color negro detectado
        brick.speaker.beep()
        brick.screen.clear()
        brick.screen.print("Color Negro")
        wait(100)
        return True
    return False


def actualizar_posicion():
    """Actualizar la posición del robot en la cuadrícula."""
    global x, y
    grid[y][x] = "R"
    imprimir_cuadricula()
    grid[y][x] = "O"  # Dejar rastro al moverse


def cambiar_direccion_por_objeto():
    """Retroceder, girar, y cambiar dirección si se encuentra un objeto."""
    global direction
    retroceder()
    if direction == "right":
        girar_derecha()
        avanzar_10cm()
        girar_derecha()
        direction = "left"
    elif direction == "left":
        girar_izquierda()
        avanzar_10cm()
        girar_izquierda()
        direction = "right"


# Bucle principal
while y < GRID_SIZE:
    # Avanzar en la dirección actual
    if direction == "right":
        if x < GRID_SIZE - 1:  # Si no ha llegado al borde derecho
            avanzar_10cm()
            x += 1
        else:  # Límite derecho alcanzado
            # Girar hacia la siguiente fila, primero girar a la izquierda
            girar_izquierda()
            avanzar_10cm()
            y += 1
            girar_izquierda()
            direction = "left"
    elif direction == "left":
        if x > 0:  # Si no ha llegado al borde izquierdo
            avanzar_10cm()
            x -= 1
        else:  # Límite izquierdo alcanzado
            # Girar hacia la siguiente fila, primero girar a la derecha
            girar_derecha()
            avanzar_10cm()
            y += 1
            girar_derecha()
            direction = "right"

    # Actualizar posición en la matriz
    actualizar_posicion()

# Finalización
brick.screen.clear()
brick.screen.print("Habitación completada")
brick.speaker.beep()

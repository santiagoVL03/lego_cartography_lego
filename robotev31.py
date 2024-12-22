#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

# Inicializar ladrillo EV3 y dispositivos
brick = EV3Brick()
motor_left = Motor(Port.A)
motor_right = Motor(Port.B)
ultrasonic_sensor = UltrasonicSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)

# Configuración de movimiento
DRIVE_SPEED = 100  # Velocidad de avance
TURN_SPEED = 50    # Velocidad de giro
CELL_SIZE = 100    # Tamaño de una celda en mm (10 cm)

# Configuración de la cuadrícula
GRID_SIZE = 10  # La habitación es 2x2 m -> 20x20 celdas de 10 cm
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Inicializar la matriz
x, y = 0, 0  # Posición inicial del robot
direction = "right"  # Dirección inicial
# Función para avanzar de forma continua
def imprimir_cuadricula():
    brick.screen.clear()
    for fila in grid:
        linea = brick.screen.print(" ".join(fila))
        brick.screen.print(linea)
    wait(500)

def avanzar_continuo():
    motor_left.run(DRIVE_SPEED)
    motor_right.run(DRIVE_SPEED)
    while True:
        if detectar_objeto():
            #detener()  # Detener el robot si se detecta un objeto negro
            break
        wait(100)  # Breve pausa para no sobrecargar el sistema

def retroceder():
    motor_left.run_angle(DRIVE_SPEED, -204.5, Stop.BRAKE, wait=False)
    motor_right.run_angle(DRIVE_SPEED, -204.5, Stop.BRAKE, wait=True)

def avanzar_10cm():
    motor_left.run_angle(DRIVE_SPEED, 204.5, Stop.BRAKE, wait=False)
    motor_right.run_angle(DRIVE_SPEED, 204.5, Stop.BRAKE, wait=True)
    


def girar_derecha():
    """Girar 90 grados a la derecha."""
    motor_left.run_angle(TURN_SPEED, 180, Stop.BRAKE, wait=False)
    motor_right.run_angle(TURN_SPEED, -180, Stop.BRAKE, wait=True)


def girar_izquierda():
    """Girar 90 grados a la izquierda."""
    motor_left.run_angle(TURN_SPEED, -180, Stop.BRAKE, wait=False)
    motor_right.run_angle(TURN_SPEED, 180, Stop.BRAKE, wait=True)


def actualizar_posicion():
    """Actualizar la posición del robot en la cuadrícula."""
    global x, y
    grid[y][x] = "R"
    imprimir_cuadricula()
    grid[y][x] = "O"  # Dejar rastro al moverse

# Función para detener el robot
def detener():
    motor_left.stop()
    motor_right.stop()

# Función para detectar objetos y colores
def detectar_objeto():
    distancia = ultrasonic_sensor.distance()
    color_detectado = color_sensor.color()

    if color_detectado == Color.RED:  # Si detecta un objeto negro
        detener()
        brick.speaker.beep()  # Emitir un sonido
        brick.screen.clear()
        brick.screen.print("ROJO")
        wait(2000)  # Esperar 2 segundos
        return True  # Indicar que debe detenerse

    elif distancia < 100:  # Si detecta cualquier objeto a menos de 10 cm
        brick.screen.clear()
        brick.screen.print("Obstaculo TwT")
        
        girar_derecha()  # Mostrar mensaje por un segundo
        avanzar_10cm()
        girar_derecha()
        avanzar_continuo()
        return False  # Continuar con el movimiento

    return False  # No hay objeto relevante detectado

# Función para realizar el giro normal
def realizar_giro():
    girar_derecha()  # Ajustar el giro según la lógica del recorrido

# Bucle principal actualizado
while y < GRID_SIZE:  # Mientras no se haya recorrido toda la habitación
    if direction == "right":
        if x < GRID_SIZE - 1:  # Si no ha llegado al borde derecho
            avanzar_continuo()
            x += 1
        else:  # Límite derecho alcanzado
            girar_izquierda()
            avanzar_continuo()
            y += 1
            girar_izquierda()
            direction = "left"
    elif direction == "left":
        if x > 0:  # Si no ha llegado al borde izquierdo
            avanzar_continuo()
            x -= 1
        else:  # Límite izquierdo alcanzado
            girar_derecha()
            avanzar_continuo()
            y += 1
            girar_derecha()
            direction = "right"

    # Actualizar posición en la matriz
    actualizar_posicion()

# Finalización
brick.screen.clear()
brick.screen.print("Completada")
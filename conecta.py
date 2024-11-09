import numpy as np
import pygame
import sys
import math

FILA = 6
COLUMNA = 7

# Colores RGB
NEGRO = (0,0,0)
TAMANIOCAJA = 100
ancho = COLUMNA * TAMANIOCAJA
alto = (FILA + 1) * TAMANIOCAJA
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0,255,0)
pygame.font.init()
MY_FUENTE = pygame.font.SysFont("monospace", 75)


tamanio = (ancho, alto)
RADIO = int(TAMANIOCAJA / 2 - 5)

pantalla = pygame.display.set_mode(tamanio)

def crear_tablero():
    tablero = np.zeros((FILA, COLUMNA))
    return tablero

def lugar_valida(board, col):
    return board[FILA-1][col] == 0

def obtener_siguiente_fila_disponible(board, col):
    for r in range(FILA):
        if board[r][col] == 0:
            return r
        
def soltar_pieza(board, row, col, piece):
    board[row][col] = piece

def es_ganador(board, piece):
    #revisando las posiciones horizontales
    for c in range(COLUMNA-3):
        for r in range(FILA):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # verificando las posiciones verticales
    for c in range(COLUMNA):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # verificando las posiciones verticales
    for c in range(COLUMNA):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # verificando diagonales positivas
    for c in range(COLUMNA-3):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # verificando diagonales positivas
    for c in range(COLUMNA-3):
        for r in range(FILA-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True 

    # verificando diagonales negativas
    for c in range(COLUMNA-3):
        for r in range(3, FILA):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def mostrar_tablero(board):
    print(np.flipud(board))


def dibujar_tablero(board):
    for c in range(COLUMNA):
        for f in range(FILA):
            # Calcular el color del degradado de verde flúor a verde
            r = 0  # Rojo constante
            g = int(255 * (1 - f / FILA))  # Verde que disminuye de 255 a 0
            b = int(255 * (f / FILA))  # Azul que aumenta de 0 a 255
            degrade_color = (r, g, b)

            # Dibujar el rectángulo con el color del degradado
            pygame.draw.rect(pantalla, degrade_color, (c * TAMANIOCAJA, f * TAMANIOCAJA + TAMANIOCAJA, TAMANIOCAJA, TAMANIOCAJA))
            pygame.draw.circle(pantalla, NEGRO, (int(c * TAMANIOCAJA + TAMANIOCAJA / 2), int(f * TAMANIOCAJA + TAMANIOCAJA + TAMANIOCAJA / 2)), RADIO)
    
    for c in range(COLUMNA):
        for f in range(FILA):
            if board[f][c] == 1:
                pygame.draw.circle(pantalla, AMARILLO, (int(c*TAMANIOCAJA+TAMANIOCAJA/2), (alto+TAMANIOCAJA)-int(f*TAMANIOCAJA+TAMANIOCAJA+TAMANIOCAJA/2)), RADIO)
            elif board[f][c] == 2:
                pygame.draw.circle(pantalla, ROJO, (int(c*TAMANIOCAJA+TAMANIOCAJA/2), (alto+TAMANIOCAJA)-int(f*TAMANIOCAJA+TAMANIOCAJA+TAMANIOCAJA/2)), RADIO)



tablero = crear_tablero()
game_over = False
turno = 0
pygame.init()

# Dibujar el tablero
dibujar_tablero(tablero)
#pygame.display.update()

while not game_over:
    # Controlar eventos para evitar que la pantalla se cierre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
        if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(pantalla, NEGRO, (0,0, ancho,TAMANIOCAJA))
                posx = event.pos[0]
                if turno == 0:
                    pygame.draw.circle(pantalla, AMARILLO, (posx, int(TAMANIOCAJA/2)), RADIO)
                else:
                    pygame.draw.circle(pantalla, ROJO, (posx, int(TAMANIOCAJA/2)), RADIO)
                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(pantalla, NEGRO, (0,0, ancho, TAMANIOCAJA))
            
            #solicitando la movida al jugador 1
            if turno == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/TAMANIOCAJA))
                
                if lugar_valida(tablero, col):
                    row = obtener_siguiente_fila_disponible(tablero, col)
                    soltar_pieza(tablero, row, col, 1)
                    
                if es_ganador(tablero, 1):
                        label = MY_FUENTE.render("Jugador 1 Gana!!!", 1, VERDE)
                        pantalla.blit(label, (40,10))
                        game_over = True    
            #solicitando la movida al jugador 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/TAMANIOCAJA))

                if lugar_valida(tablero, col):
                    row = obtener_siguiente_fila_disponible(tablero, col)
                    soltar_pieza(tablero, row, col, 2)

                    if es_ganador(tablero, 2):
                        label = MY_FUENTE.render("Jugador 2 Gana!!!", 1, VERDE)
                        pantalla.blit(label, (40,10))

                        if es_ganador(tablero, 2):
                            label = MY_FUENTE.render("Jugador 2 Gana!!!", 1, VERDE)
                            pantalla.blit(label, (40,10))
                            game_over = True  

            dibujar_tablero(tablero)
            pygame.display.update()
            
            turno += 1 
            turno = turno % 2

            if game_over:
                pygame.time.wait(3000)                          
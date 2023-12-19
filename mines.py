import tkinter as tk
import random

def generar_tablero(filas, columnas, minas):
    tablero = [[0] * columnas for _ in range(filas)]
    minas_generadas = 0

    while minas_generadas < minas:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)

        if tablero[fila][columna] != -1:
            tablero[fila][columna] = -1
            minas_generadas += 1

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= fila + i < filas and 0 <= columna + j < columnas and tablero[fila + i][columna + j] != -1:
                        tablero[fila + i][columna + j] += 1

    return tablero

class Buscaminas:
    def __init__(self, master, filas, columnas, minas):
        self.master = master
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.tablero = generar_tablero(filas, columnas, minas)
        self.botones = []

        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                boton = tk.Button(master, width=2, height=1)
                boton.grid(row=i, column=j)
                fila_botones.append(boton)

                # Manejar clic izquierdo
                boton.bind('<Button-1>', lambda event, x=i, y=j: self.hacer_click(event, x, y))

                # Manejar clic derecho
                boton.bind('<Button-3>', lambda event, x=i, y=j: self.marcar_mina(event, x, y))

            self.botones.append(fila_botones)

    def hacer_click(self, event, fila, columna):
        if self.tablero[fila][columna] == -1:
            print("¡Has perdido!")
            self.mostrar_tablero()
        else:
            valor = self.tablero[fila][columna]
            if valor > 0:
                self.botones[fila][columna].config(text=str(valor))
            else:
                self.descubrir_casillas_vacias(fila, columna)

    def marcar_mina(self, event, fila, columna):
        self.botones[fila][columna].config(text='M')
        self.botones[fila][columna].unbind('<Button-3>')  # Desactivar clic derecho después de marcar

    def descubrir_casillas_vacias(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas and self.botones[fila][columna]['state'] == 'normal':
            valor = self.tablero[fila][columna]
            self.botones[fila][columna].config(text=str(valor))

            if valor == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nueva_fila = fila + i
                        nueva_columna = columna + j
                        if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas and self.tablero[nueva_fila][nueva_columna] != -1:
                            self.descubrir_casillas_vacias(nueva_fila, nueva_columna)
                        elif 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas and self.tablero[nueva_fila][nueva_columna] == 0:
                            self.botones[nueva_fila][nueva_columna].config(text=str(self.tablero[nueva_fila][nueva_columna]))
                            self.descubrir_casillas_vacias(nueva_fila, nueva_columna)
                        elif 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas and self.tablero[nueva_fila][nueva_columna] > 0:
                            self.botones[nueva_fila][nueva_columna].config(text=str(self.tablero[nueva_fila][nueva_columna]))


    def mostrar_tablero(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                valor = self.tablero[i][j]
                if valor == -1:
                    self.botones[i][j].config(text='X')
                else:
                    self.botones[i][j].config(text=str(valor))

# Configuración del juego
filas = 8
columnas = 8
minas = 10

# Crear la ventana principal
root = tk.Tk()
root.title("Buscaminas")

# Iniciar el juego
buscaminas = Buscaminas(root, filas, columnas, minas)

# Mantener la ventana abierta
root.mainloop()

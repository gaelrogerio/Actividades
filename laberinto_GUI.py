import numpy as np
import time
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

vidas = 3
grid_size = 10 
cell_size = 50

class LaberintoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Laberinto")
        self.vidas = 5
        self.grid, self.casillas_especiales_coords = self.crear_matriz(grid_size, grid_size)
        self.camino = []
        self.create_widgets()

    def create_widgets(self):
        # Crear un lienzo para el laberinto
        self.canvas = tk.Canvas(self.root, width=grid_size * cell_size, height=grid_size * cell_size)
        self.canvas.pack()
        self.dibujar_laberinto()

        # Botón para comenzar el juego
        self.start_button = tk.Button(self.root, text="Comenzar", command=self.encontrar_camino)
        self.start_button.pack(pady=10)

        # Mostrar vidas restantes
        self.vidas_label = tk.Label(self.root, text=f"Vidas: {self.vidas}")
        self.vidas_label.pack()

    def crear_matriz(self, x, y):
        matriz = np.random.randint(0, 2, size=(x, y))
        matriz[0][0] = 0  # entrada
        matriz[-1][-1] = 2  # salida
        matriz, casillas_especiales = self.agregar_casillas_especiales(matriz, 10)  # agregar n casillas especiales
        return matriz, casillas_especiales

    def agregar_casillas_especiales(self, matriz, num_casillas):
        filas, columnas = matriz.shape
        casillas_especiales = []
        while len(casillas_especiales) < num_casillas:
            x = random.randint(0, filas - 1)
            y = random.randint(0, columnas - 1)
            if matriz[x][y] == 0 and (x, y) != (0, 0) and (x, y) != (filas - 1, columnas - 1):
                casillas_especiales.append((x, y))
                matriz[x][y] = -1  # Marcar como casilla especial
        return matriz, casillas_especiales

    def dibujar_laberinto(self):
        self.canvas.delete("all")
        for i in range(grid_size):
            for j in range(grid_size):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size

                if self.grid[i][j] == 0:
                    color = "white"  # Camino normal
                elif self.grid[i][j] == 1:
                    color = "black"  # Pared
                elif self.grid[i][j] == 2:
                    color = "green"  # Salida
                elif self.grid[i][j] == -1:
                    color = "yellow"  # Casilla especial
                else:
                    color = "red"  # Marcador de error por si acaso

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def encontrar_camino(self):
        filas = len(self.grid)
        columnas = len(self.grid[0])
        dp = [[float('inf')] * columnas for _ in range(filas)]
        dp[0][0] = 0

        for i in range(1, filas):
            dp[i][0] = dp[i - 1][0] + self.grid[i][0]
        for j in range(1, columnas):
            dp[0][j] = dp[0][j - 1] + self.grid[0][j]

        for i in range(1, filas):
            for j in range(1, columnas):
                if self.grid[i][j] != -1:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + self.grid[i][j]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1])

        camino = []
        i, j = filas - 1, columnas - 1
        while i > 0 or j > 0:
            camino.append((i, j))
            if i > 0 and j > 0:
                if dp[i - 1][j] < dp[i][j - 1]:
                    i -= 1
                else:
                    j -= 1
            elif i > 0:
                i -= 1
            else:
                j -= 1
        camino.append((0, 0))
        camino.reverse()

        self.camino = camino
        self.mover_jugador()

    def mover_jugador(self):
        for (x, y) in self.camino:
            self.canvas.create_oval(y * cell_size + 15, x * cell_size + 15, y * cell_size + 35, x * cell_size + 35, fill="blue")
            self.root.update()
            time.sleep(1)

            if self.grid[x][y] == 1:  # Pared
                self.pregunta_matematica()
                if self.vidas == 0:
                    messagebox.showinfo("¡Game Over!", "¡Has perdido todas tus vidas!")
                    return
            elif self.grid[x][y] == -1:  # Casilla especial
                self.casillas_especiales()
                if self.vidas == 0:
                    messagebox.showinfo("¡Game Over!", "¡Has perdido todas tus vidas!")
                    return
                self.grid[x][y] = 0  # Después del evento, volver a camino normal

        messagebox.showinfo("¡Felicidades!", "¡Has encontrado la salida! ¡GG!")

    def pregunta_matematica(self):
        global vidas
        num1 = random.randint(1, 1000)
        num2 = random.randint(1, 1000)
        operacion = random.choice(['+', '-', '*'])

        if operacion == '+':
            resultado = num1 + num2
        elif operacion == '-':
            resultado = num1 - num2
        else:
            num1 = random.randint(1, 30)
            num2 = random.randint(1, 30)
            resultado = num1 * num2
        while True:
            respuesta = simpledialog.askinteger("Desafío", f"Para derribar la pared, resuelve: {num1} {operacion} {num2}")
            if respuesta == resultado:
                messagebox.showinfo("¡Correcto!", "¡Derribaste la pared! puedes seguir avanzando")
                break
            else:
                self.vidas -= 1
                self.vidas_label.config(text=f"Vidas: {self.vidas}")
                messagebox.showinfo("Incorrecto", f"Perdiste una vida. Vidas restantes: {self.vidas}")
                if self.vidas == 0:
                    break

    def casillas_especiales(self):
        evento = random.choice(["vida_extra", "mina_explosiva", "monstruo"])
        if evento == "vida_extra":
            self.vidas += 1
            self.vidas_label.config(text=f"Vidas: {self.vidas}")
            messagebox.showinfo("¡Vida extra!", f"Hallaste un contenedor de corazón, ¡ganaste una vida!. Vidas restantes: {self.vidas}")
        elif evento == "mina_explosiva":
            self.vidas -= 1
            self.vidas_label.config(text=f"Vidas: {self.vidas}")
            messagebox.showinfo("¡Mina explosiva!", f"Pisaste una mina, ¡perdiste una vida!. Vidas restantes: {self.vidas}")
        elif evento == "monstruo":
            decision = messagebox.askquestion("¡Monstruo!", "Un monstruo te ataca, ¿quieres pelear (Sí) o huir (No)?")
            if decision == "yes":
                resultado = random.choice([True, False])
                if resultado:
                    messagebox.showinfo("Monstruo", "¡Derrotaste al monstruo! sigue avanzando")
                else:
                    self.vidas -= 1
                    self.vidas_label.config(text=f"Vidas: {self.vidas}")
                    messagebox.showinfo("Monstruo", f"El monstruo te derrotó, perdiste una vida. Vidas restantes: {self.vidas}")
            else:
                resultado = random.choice([True, False])
                if resultado:
                    messagebox.showinfo("Monstruo", "¡Lograste escapar del monstruo!")
                else:
                    self.vidas -= 1
                    self.vidas_label.config(text=f"Vidas: {self.vidas}")
                    messagebox.showinfo("Monstruo", f"No pudiste escapar del monstruo, perdiste una vida. Vidas restantes: {self.vidas}")

root = tk.Tk()
app = LaberintoApp(root)
root.mainloop()

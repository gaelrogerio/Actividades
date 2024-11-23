import heapq
import tkinter as tk
from tkinter import filedialog, messagebox
import json

class NodoHuffman:
    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def calcular_frecuencia(contenido):
    frecuencia = {}
    for simbolo in contenido:
        if simbolo in frecuencia:
            frecuencia[simbolo] += 1
        else:
            frecuencia[simbolo] = 1
    return frecuencia

def construir_arbol_huffman(frecuencia):
    cola_prioridad = []
    for simbolo, cuenta in frecuencia.items():
        heapq.heappush(cola_prioridad, NodoHuffman(simbolo, cuenta))
    
    while len(cola_prioridad) > 1:
        nodo_izq = heapq.heappop(cola_prioridad)
        nodo_der = heapq.heappop(cola_prioridad)
        nodo_comb = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nodo_comb.izquierda = nodo_izq
        nodo_comb.derecha = nodo_der
        heapq.heappush(cola_prioridad, nodo_comb)
    
    return cola_prioridad[0]

def generar_codigos_huffman(nodo, prefijo="", codigos={}):
    if nodo is not None:
        if nodo.simbolo is not None:
            codigos[nodo.simbolo] = prefijo
        generar_codigos_huffman(nodo.izquierda, prefijo + "0", codigos)
        generar_codigos_huffman(nodo.derecha, prefijo + "1", codigos)
    return codigos

def comprimir(contenido, codigos):
    return ''.join(codigos[s] for s in contenido)

def descomprimir(codigo_binario, codigos):
    codigos_invertidos = {v: k for k, v in codigos.items()}
    codigo = ""
    resultado = ""
    
    for bit in codigo_binario:
        codigo += bit
        if codigo in codigos_invertidos:
            resultado += codigos_invertidos[codigo]
            codigo = ""
    return resultado

def seleccionar_archivo(extension):
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos", extension)])
    return ruta_archivo

def comprimir_archivo():
    ruta_archivo = seleccionar_archivo("*.txt")
    if not ruta_archivo:
        return

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()

    # Calcular frecuencia y construir árbol de Huffman
    frecuencia = calcular_frecuencia(contenido)
    arbol_huffman = construir_arbol_huffman(frecuencia)
    codigos = generar_codigos_huffman(arbol_huffman)
    
    codigo_comprimido = comprimir(contenido, codigos)

    # Guardar el archivo comprimido con frecuencias y el código binario
    with open("comprimido.bin", "w") as archivo_bin:
        archivo_bin.write(json.dumps({"frecuencia": frecuencia, "codigo_comprimido": codigo_comprimido}))

    messagebox.showinfo("Compresión", "Archivo comprimido guardado como 'comprimido.bin'")

def descomprimir_archivo():
    ruta_archivo = seleccionar_archivo("*.bin")
    if not ruta_archivo:
        return

    # Leer el archivo comprimido y extraer frecuencias y el código binario
    with open(ruta_archivo, 'r') as archivo_bin:
        datos = json.loads(archivo_bin.read())
        frecuencia = datos["frecuencia"]
        codigo_comprimido = datos["codigo_comprimido"]

    arbol_huffman = construir_arbol_huffman(frecuencia)
    codigos = generar_codigos_huffman(arbol_huffman)

    contenido_descomprimido = descomprimir(codigo_comprimido, codigos)

    # Guardar el archivo descomprimido
    with open("descomprimido.txt", "w", encoding='utf-8') as archivo_descomprimido:
        archivo_descomprimido.write(contenido_descomprimido)

    messagebox.showinfo("Descompresión", "Archivo descomprimido guardado como 'descomprimido.txt'")

# Interfaz gráfica
root = tk.Tk()
root.title("Compresión y Descompresión Huffman")
root.geometry("300x200")

btn_comprimir = tk.Button(root, text="Comprimir archivo", command=comprimir_archivo)
btn_comprimir.pack(pady=10)

btn_descomprimir = tk.Button(root, text="Descomprimir archivo", command=descomprimir_archivo)
btn_descomprimir.pack(pady=10)

root.mainloop()

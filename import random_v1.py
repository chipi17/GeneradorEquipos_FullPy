import random
import tkinter as tk
import os
from tkinter import messagebox
from tkinter import ttk  # Importamos ttk para usar estilos
from PIL import Image, ImageTk

# Definimos las dimensiones de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Definimos las dimensiones del campo de fútbol
ANCHO_CAMPO = 600
ALTO_CAMPO = 400

# Definimos los colores de los equipos
COLOR_A = "#FF0000"  # Rojo
COLOR_B = "#0000FF"  # Azul
Color_C = "000000"

# Definimos los colores del campo de fútbol
COLOR_CESPED = "#32CD32"  # Verde oscuro
COLOR_AREA = "#90EE90"    # Verde claro
COLOR_AREA_LINEA = "#008000"  # Verde oscuro
COLOR_PORTERIA = "#FFFFFF"  # Blanco
COLOR_MEDIOCAMPO = "#FFFF99"  # Amarillo

# Creamos una lista global para almacenar referencias a las imágenes de las camisetas
image_references = []

# Creamos la ventana del formulario
formulario = tk.Tk()
formulario.geometry("400x400")
formulario.title("Generador de Equipos")

# Modificamos el estilo de la ventana
estilo = ttk.Style()
estilo.configure('TLabel', font=('Arial', 11))
estilo.configure('TButton', font=('Arial', 11))
estilo.configure('TEntry', font=('Arial', 11))

frame_principal = ttk.Frame(formulario)
frame_principal.pack(padx=10, pady=10, expand=True, fill='both')

etiqueta_jugadores = ttk.Label(frame_principal, text="Elige que tipo de futbol quieres:Sala(10),7(14) o 11(22) ")
etiqueta_jugadores.grid(row=0, column=0, sticky='w', pady=(0, 10))
entrada_jugadores = ttk.Entry(frame_principal)
entrada_jugadores.grid(row=0, column=1, sticky='w', pady=(0, 10))

frame_nombres = ttk.Frame(frame_principal)
frame_nombres.grid(row=1, column=0, columnspan=2, pady=(10, 0))

def mostrar_campos_nombres():
    try:
        num_jugadores = int(entrada_jugadores.get())
        if num_jugadores not in (10, 14, 22):
            raise ValueError("Debes poner los valores Elegir entre Futbol-Sala(10), Futbol 7(14) o Futbol 11(22)")
    except ValueError as e:
        messagebox.showwarning("Valor Incorrecto", str(e))
        return

    for widget in frame_nombres.winfo_children():
        widget.destroy()

    for i in range(num_jugadores):
        etiqueta_nombre = ttk.Label(frame_nombres, text=f"Jugador {i+1}:")
        etiqueta_nombre.grid(row=i, column=0, sticky='w')
        entrada_nombre = ttk.Entry(frame_nombres)
        entrada_nombre.grid(row=i, column=1, sticky='w')

boton_mostrar_campos = ttk.Button(frame_principal, text="Mostrar campos", command=mostrar_campos_nombres)
boton_mostrar_campos.grid(row=2, column=0, columnspan=2, pady=(10, 0))

# Función que se ejecuta cuando se presiona el botón "Generar equipos"
def generar_equipos():

    # Obtenemos la cantidad de jugadores y sus nombres desde los campos de entrada del formulario
    num_jugadores = int(entrada_jugadores.get())
    nombres = [entrada.get() for entrada in frame_nombres.winfo_children() if isinstance(entrada, ttk.Entry)]

    # Creamos dos listas vacías para almacenar los nombres de los equipos
    equipo_a = []
    equipo_b = []
    
    # Repartimos los nombres de forma aleatoria y equitativa en ambos equipos
    while nombres:
        jugador_a = random.choice(nombres)
        equipo_a.append(jugador_a)
        nombres.remove(jugador_a)
        
        if nombres:
            jugador_b = random.choice(nombres)
            equipo_b.append(jugador_b)
            nombres.remove(jugador_b)
    
    # Creamos la ventana y el lienzo donde se dibujarán los jugadores
    ventana = tk.Toplevel(formulario)
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    lienzo = tk.Canvas(ventana, width=ANCHO_CAMPO, height=ALTO_CAMPO)
    lienzo.pack()
    # Dibujamos el campo de fútbol
    lienzo.create_rectangle(0, 0, ANCHO_CAMPO, ALTO_CAMPO, fill=COLOR_CESPED)

    #lienzo.create_rectangle(0, ALTO_CAMPO/3, ANCHO_CAMPO/6, ALTO_CAMPO*2/3, fill=COLOR_AREA)
    #lienzo.create_rectangle(ANCHO_CAMPO*5/6, ALTO_CAMPO/3, ANCHO_CAMPO, ALTO_CAMPO*2/3, fill=COLOR_AREA)
# Dibujamos las áreas de cada equipo
    lienzo.create_rectangle(0, ALTO_CAMPO*1/4, ANCHO_CAMPO/6, ALTO_CAMPO*3/4, fill=COLOR_AREA, outline=COLOR_AREA_LINEA)
    lienzo.create_rectangle(ANCHO_CAMPO*5/6, ALTO_CAMPO*1/4, ANCHO_CAMPO, ALTO_CAMPO*3/4, fill=COLOR_AREA, outline=COLOR_AREA_LINEA)

    lienzo.create_line(ANCHO_CAMPO/2, 0, ANCHO_CAMPO/2, ALTO_CAMPO, width=5, fill=COLOR_MEDIOCAMPO)
    lienzo.create_oval(ANCHO_CAMPO/2-30, ALTO_CAMPO/2-30, ANCHO_CAMPO/2+30, ALTO_CAMPO/2+30, outline=COLOR_MEDIOCAMPO, width=5)

    lienzo.create_rectangle(0, ALTO_CAMPO/3, ANCHO_CAMPO/18, ALTO_CAMPO/2.5, fill=COLOR_PORTERIA)
    lienzo.create_rectangle(0, ALTO_CAMPO*1.5/2.5, ANCHO_CAMPO/18, ALTO_CAMPO*2/3, fill=COLOR_PORTERIA)

    lienzo.create_rectangle(ANCHO_CAMPO, ALTO_CAMPO/3, ANCHO_CAMPO-ANCHO_CAMPO/18, ALTO_CAMPO/2.5, fill=COLOR_PORTERIA)
    lienzo.create_rectangle(ANCHO_CAMPO, ALTO_CAMPO*1.5/2.5, ANCHO_CAMPO-ANCHO_CAMPO/18, ALTO_CAMPO*2/3, fill=COLOR_PORTERIA)
    lienzo.create_line(ANCHO_CAMPO/6, ALTO_CAMPO/3, ANCHO_CAMPO/6, ALTO_CAMPO*2/3, width=5, fill=COLOR_MEDIOCAMPO)
    lienzo.create_line(ANCHO_CAMPO*5/6, ALTO_CAMPO/3, ANCHO_CAMPO*5/6, ALTO_CAMPO*2/3, width=5, fill=COLOR_MEDIOCAMPO)
   
    image_references = []

    def posicionar_jugadores(equipo, color, es_equipo_a):
        global image_references
        camiseta_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"shirt{'a' if es_equipo_a else 'b'}.png")
        camiseta_img = Image.open(camiseta_img_path)
        camiseta_img = camiseta_img.resize((20, 20), Image.LANCZOS)
        camiseta_img_tk = ImageTk.PhotoImage(camiseta_img)
        image_references.append(camiseta_img_tk)

        if len(equipo) == 5:
            posiciones = [
                (ANCHO_CAMPO/12 if es_equipo_a else ANCHO_CAMPO*11/12, ALTO_CAMPO/2),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO/3),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO*2/3),
                (ANCHO_CAMPO/4 if es_equipo_a else ANCHO_CAMPO*3/4, ALTO_CAMPO/2),
                (ANCHO_CAMPO/2 - (40 if es_equipo_a else -40), ALTO_CAMPO/2)
        ]
    # Resto del
        elif len(equipo) == 7:
            posiciones = [
                (ANCHO_CAMPO/18 if es_equipo_a else ANCHO_CAMPO*17/18, ALTO_CAMPO/2),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO/4),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO/2),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO*3/4),
                (ANCHO_CAMPO/4 if es_equipo_a else ANCHO_CAMPO*3/4, ALTO_CAMPO/3),
                (ANCHO_CAMPO/4 if es_equipo_a else ANCHO_CAMPO*3/4, ALTO_CAMPO*2/3),
                (ANCHO_CAMPO/2 - (40 if es_equipo_a else -40), ALTO_CAMPO/2)
        ]
        elif len(equipo) == 11:
            posiciones = [
                (ANCHO_CAMPO/18 if es_equipo_a else ANCHO_CAMPO*17/18, ALTO_CAMPO/2),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO*1/6),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO/3),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO/2),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO*2/3),
                (ANCHO_CAMPO/6 if es_equipo_a else ANCHO_CAMPO*5/6, ALTO_CAMPO*5/6),
                (ANCHO_CAMPO/4 if es_equipo_a else ANCHO_CAMPO*3/4, ALTO_CAMPO/4),
                (ANCHO_CAMPO/4 if es_equipo_a else ANCHO_CAMPO*3/4, ALTO_CAMPO*3/4),
                (ANCHO_CAMPO/3 if es_equipo_a else ANCHO_CAMPO*2/3, ALTO_CAMPO/3),
                (ANCHO_CAMPO/3 if es_equipo_a else ANCHO_CAMPO*2/3, ALTO_CAMPO*2/3),
                (ANCHO_CAMPO/2 - (40 if es_equipo_a else -40), ALTO_CAMPO/2)
    ]
        if len(equipo) == 5:
            posiciones[-1] = (ANCHO_CAMPO/2 - (60 if es_equipo_a else -60), ALTO_CAMPO/2)
        elif len(equipo) == 7:
            posiciones[-1] = (ANCHO_CAMPO/2 - (60 if es_equipo_a else -60), ALTO_CAMPO/2)
        elif len(equipo) == 11:
            posiciones[-2] = (ANCHO_CAMPO/2 - (40 if es_equipo_a else -40), ALTO_CAMPO/3)
            posiciones[-1] = (ANCHO_CAMPO/2 - (40 if es_equipo_a else -40), ALTO_CAMPO*2/3)

        for i, jugador in enumerate(equipo):
            x, y = posiciones[i]
            lienzo.create_image(x, y, image=camiseta_img_tk, anchor='center', tags="jugador")
            lienzo.create_text(x, y-15, text=equipo[i], tags="nombre_jugador")

    posicionar_jugadores(equipo_a, COLOR_A, True)
    posicionar_jugadores(equipo_b, COLOR_B, False)
    leyenda_equipo_a = tk.Label(ventana, text="Equipo A (camisetas negras)", font=("Arial", 12), fg=COLOR_A)
    leyenda_equipo_a.pack(side=tk.LEFT, padx=(10, 0), pady=(10, 0))
    
    leyenda_equipo_b = tk.Label(ventana, text="Equipo B (camisetas blancas)", font=("Arial", 12), fg=COLOR_B)
    leyenda_equipo_b.pack(side=tk.RIGHT, padx=(0, 10), pady=(10, 0))

    leyenda_creador = tk.Label(ventana, text="Creado por Chipi17 ©", font=("Arial", 18, "bold"))
    leyenda_creador.pack(side=tk.LEFT, padx=(150, 0), pady=(10, 0))

# Creamos el botón para generar los equipos
boton_generar = ttk.Button(frame_principal, text="Generar equipos", command=generar_equipos)
boton_generar.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    # Iniciamos el bucle principal de la aplicación
formulario.mainloop()

import time
import tkinter as tk
from os import path
from tkinter import ttk
from tkinter import messagebox

#---------------------------------------------------------------------------------------------
# AGREGAR/QUITAR - FUNCION DRAG AND DROP -----------------------------------------------------
def make_draggable(widget): # Activa las propiedades de DND
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease-1>", on_drop_motion)

def unmake_draggable(widget): # Desactiva las propiedades de DND
    widget.unbind("<Button-1>")
    widget.unbind("<B1-Motion>")
    widget.unbind("<ButtonRelease-1>")

#---------------------------------------------------------------------------------------------
# POSICIONAMIENTO DE LABELS ------------------------------------------------------------------
posXYIni = [] # Variable de posición de origen
win = [False] #Variable de victoria - Evita que los discos sean DND

def on_drag_start(event): # Guarda las coordenadas iniciales al hacer click sobre el disco
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    posXYIni.clear()
    posXYIni.append(widget.winfo_x())
    posXYIni.append(widget.winfo_y())

# areas = [ #Rangos de áreas, orden A, B, C
#     [30,319,165,412], # Xi, Xf, Yi, Yf
#     [420, 724, 165, 412],[810, 1114, 165, 412]]

def on_drag_motion(event): # Función de movimiento (arrastre) del label (disco)
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

def obtainOrigin(origXY): # Obtiene el área de origen
    if posXYIni[0] >= 30 and posXYIni[0] <= 319:
        return "A"
    elif posXYIni[0] >= 420 and posXYIni[0] <= 724:
        return "B"
    elif posXYIni[0] >= 810 and posXYIni[0] <= 1114:
        return "C"

def on_drop_motion(event): # Función para mover el disco de palo
    widget = event.widget
    x = widget.winfo_x() 
    y = widget.winfo_y() 
    origin = obtainOrigin(posXYIni) #Obteniendo origen del disco a mover
    if origin == "A":
        if y >= 165 and y <= 412:
            if x >= 420 and x <= 724:
                quitaD_N_D()
                if validaMov(origin, "B"):
                    discosT_B.append(discosT_A.pop(len(discosT_A)-1))
                    actualizaMov()
                    muestraMensaje("")
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            elif x >= 810 and x <= 1114:
                quitaD_N_D()
                if validaMov(origin, "C"):
                    discosT_C.append(discosT_A.pop(len(discosT_A)-1))
                    actualizaMov()
                    muestraMensaje("")
                    validaWin()
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            else:
                widget.place(x=posXYIni[0], y=posXYIni[1])
        else:
            widget.place(x=posXYIni[0], y=posXYIni[1])
    if origin == "B":
        if y >= 165 and y <= 412:
            if x >= 30 and x <= 319:
                quitaD_N_D()
                if validaMov(origin, "A"):
                    discosT_A.append(discosT_B.pop(len(discosT_B)-1))
                    actualizaMov()
                    muestraMensaje("")
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            elif x >= 810 and x <= 1114:
                quitaD_N_D()
                if validaMov(origin, "C"):
                    discosT_C.append(discosT_B.pop(len(discosT_B)-1))
                    actualizaMov()
                    muestraMensaje("")
                    validaWin()
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            else:
                widget.place(x=posXYIni[0], y=posXYIni[1])
        else:
            widget.place(x=posXYIni[0], y=posXYIni[1])
    if origin == "C":
        if y >= 165 and y <= 412:
            if x >= 30 and x <= 319:
                quitaD_N_D()
                if validaMov(origin, "A"):
                    discosT_A.append(discosT_C.pop(len(discosT_C)-1))
                    actualizaMov()
                    muestraMensaje("")
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            elif x >= 420 and x <= 724:
                quitaD_N_D()
                if validaMov(origin, "B"):
                    discosT_B.append(discosT_C.pop(len(discosT_C)-1))
                    actualizaMov()
                    muestraMensaje("")
                else:
                    muestraMensaje("MOVIMIENTO INVÁLIDO")
                muestraDiscos()
            else:
                widget.place(x=posXYIni[0], y=posXYIni[1])
        else:
            widget.place(x=posXYIni[0], y=posXYIni[1])

def validaWin():
    global win
    if not discosT_A and not discosT_B:
        muestraMensaje("PARTIDA GANADA!!!")
        win[0] = True

#---------------------------------------------------------------------------------------------
# GUI ----------------------------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("TORRES DE HANOI - MC2N")
ventana.geometry("1160x640") #tamaño ventana

def getSource(): # Ruta local de ejecución
    ruta = path.dirname(path.abspath(__file__)) #Obtiene la ruta del script en ejecución
    return ruta

# >>> GENERADOR DE TORRES---------------------------------------------------------------------
img_bases = [] # Almacena las imagenes de los palos (PhotoImage)
bases = [] # Almacena las imagenes de los palos (labels)

for j in range(3): # Carga a memoria 3 objetos (imagenes) de las bases/palos/torres
    ruta = getSource()
    img=tk.PhotoImage(file=ruta+"\\src\\base.png")
    img = img.subsample(2,2)
    img_bases.append(img)

for j in range(3): # Crea labels para los palos
    bases.append(tk.Label(ventana, image=img_bases[j]))

iniB_x = 15 #Posición de inicio en x
for b in bases: # Coloca en pantalla los palos
    b.place(x=iniB_x, y=180)
    iniB_x += 390

# >>> DISCOS ---------------------------------------------------------------------------------
img_discos = [] # Almacena las imagenes de los discos (PhotoImage)
discosT_A = [] # Almacena las imagenes de los discos (labels) - Palo Inicial
discosT_B = [] # Almacena las imagenes de los discos (labels) - Palo Auxiliar
discosT_C = [] # Almacena las imagenes de los discos (labels) - Palo Destino/Final
count_Movs = [0] # Contador de movimientos

def generaDiscos(n_discos): # Genera las imagenes y labels de los discos
    global img_discos, discosT_A
    for i in range(n_discos):
        ruta = getSource()
        img = tk.PhotoImage(file=ruta+"\\src\\disco"+str(n_discos-i)+".png")
        img = img.subsample(2,2)
        img_discos.append([img, img.width()/2])
    for i in range(n_discos):
        discosT_A.append([tk.Label(ventana, image=img_discos[i][0]), img_discos[i][1]])

def usaD_N_D(): # Aplica la propiedad DND a todos los discos de cada palo
    if discosT_A:
        make_draggable(discosT_A[len(discosT_A)-1][0])
    if discosT_B:
        make_draggable(discosT_B[len(discosT_B)-1][0])
    if discosT_C:
        make_draggable(discosT_C[len(discosT_C)-1][0])

def quitaD_N_D(): # Remueve la propiedad DND a todos los discos de cada palo
    if discosT_A:
        unmake_draggable(discosT_A[len(discosT_A)-1][0])
    if discosT_B:
        unmake_draggable(discosT_B[len(discosT_B)-1][0])
    if discosT_C:
        unmake_draggable(discosT_C[len(discosT_C)-1][0])

def paintD(discos, ini_x): # Coloca los discos en la ventana
    global win
    ini_y = 412 #Posición Y inicio (Posicion mas baja)
    for d in discos:
        pos_x_ini = ini_x - d[1]
        d[0].place(x=pos_x_ini, y=ini_y)
        ini_y -= 31
    if not win[0]: #Aplica la propiedad DND si la partida no esta ganada
        print("Se hace DND")
        usaD_N_D()

def muestraDiscos(): # Envia a cada lista (Palo) a mostrar sus discos
    global discosT_A, discosT_B, discosT_C
    paintD(discosT_A, 180)
    paintD(discosT_B, 570)
    paintD(discosT_C, 960)

def destruyeDiscos(): # Elimina los discos de la ventana
    if discosT_A:
        for d in discosT_A:
            d[0].destroy()
    if discosT_B:
        for d in discosT_B:
            d[0].destroy()
    if discosT_C:
        for d in discosT_C:
            d[0].destroy()

def resetAll(): # Vacia memoria de discos, contadores y posiciones, entre otros
    destruyeDiscos()
    img_discos.clear()
    discosT_A.clear()
    discosT_B.clear()
    discosT_C.clear()
    posXYIni.clear()
    count_Movs.clear()
    count_Movs.append(0)
    win.clear()
    win.append(False)

def validaMov(salida, llegada): # Control de movimiento (Un disco mayor no puede estar sobre uno menor)
    if salida == "A" and llegada == "B":
        if discosT_B:
            if discosT_A[len(discosT_A)-1][1] < discosT_B[len(discosT_B)-1][1]:
                return True
            else:
                return False
        return True
    elif salida == "A" and llegada == "C":
        if discosT_C:
            if discosT_A[len(discosT_A)-1][1] < discosT_C[len(discosT_C)-1][1]:
                return True
            else:
                return False
        return True
    elif salida == "B" and llegada == "A":
        if discosT_A:
            if discosT_B[len(discosT_B)-1][1] < discosT_A[len(discosT_A)-1][1]:
                return True
            else:
                return False
        return True
    elif salida == "B" and llegada == "C":
        if discosT_C:
            if discosT_B[len(discosT_B)-1][1] < discosT_C[len(discosT_C)-1][1]:
                return True
            else:
                return False
        return True
    elif salida == "C" and llegada == "A":
        if discosT_A:
            if discosT_C[len(discosT_C)-1][1] < discosT_A[len(discosT_A)-1][1]:
                return True
            else:
                return False
        return True
    elif salida == "C" and llegada == "B":
        if discosT_B:
            if discosT_C[len(discosT_C)-1][1] < discosT_B[len(discosT_B)-1][1]:
                return True
            else:
                return False
        return True

def calculaMovMin(n_discos): # Ecuación de recurrencia TORRES DE HANOI
    min = 2**n_discos - 1
    count_Movs.append(min)


# >>>>>> OTROS COMPONENTES GUI ---------------------------------------------
my_label = tk.Label(ventana, text="Ingrese la cantidad de discos a utilizar: ", font=20)
my_label.place(x= 35, y=30)

lbl_Info = tk.Label(ventana, text="INICIAR JUEGO", font=20)
lbl_Info.place(x= 525, y=550)

opr_cmbx = ttk.Combobox(ventana, state="readonly", font=20, width=5)
opr_cmbx["values"]=[1, 2, 3, 4, 5, 6, 7]
opr_cmbx.place(x=315, y= 30)

lbl_Movs = tk.Label(ventana, text="MOVIMIENTOS REALIZADOS: 0", font=60)
lbl_Movs.place(x=880, y=30)

lbl_MovsMin = tk.Label(ventana, text="MOVIMIENTOS MINIMOS: 0", font=60)
lbl_MovsMin.place(x= 880, y=70)

partidaG = [False] # Indica si hay un juego en curso

def muestraMensaje(msg): # Modifica el label para mostrar información
    lbl_Info["text"]=msg

def actualizaMov(): # Modifica el label para mostrar el conteo de movimientos
    global count_Movs
    count_Movs[0] += 1
    lbl_Movs["text"]="MOVIMIENTOS REALIZADOS: " + str(count_Movs[0])


def startGame():
    sel = opr_cmbx.get()
    global partidaG
    if sel:
        sel = int(sel)
        if partidaG[0]:
            resetAll()
            partidaG[0] = False
        calculaMovMin(sel)
        lbl_Movs["text"]="MOVIMIENTOS REALIZADOS: " + str(count_Movs[0])
        lbl_MovsMin["text"]="MOVIMIENTOS MINIMOS: " + str(count_Movs[1])
        generaDiscos(sel)
        muestraDiscos()
        partidaG[0] = True
    else:
        muestraMensaje("SELECCIONE UNA CANTIDAD DE DISCOS A USAR")

btn = tk.Button(ventana, text = "Iniciar Juego", width=15, command=startGame)
btn.place(x=395, y= 30)

# >>>> Juego Automático ---------------------------------------------------------

ruta = [] # Almacena la ruta de movimientos para resolverlo automáticamente

def iniciaRecorrido(n_discos, salida, llegada, intermedio):
    if n_discos >= 1:
        iniciaRecorrido(n_discos-1, salida, intermedio, llegada)
        ruta.append([salida, llegada])
        iniciaRecorrido(n_discos-1, intermedio, llegada, salida)

def recorrerMov(cont):
    if cont == 0:
        muestraDiscos()
        muestraMensaje("JUEGO AUTOMÁTICO")
    elif cont-1 < len(ruta):
        moverDisco(ruta[cont-1][0], ruta[cont-1][1])
        actualizaMov()
    else:
        return
    cont+=1
    ventana.after(800, recorrerMov, cont)

def moverDisco(salida, llegada):
    if salida == "A" and llegada == "B":
        discosT_B.append(discosT_A.pop(len(discosT_A)-1))
        muestraDiscos()
    elif salida == "A" and llegada == "C":
        discosT_C.append(discosT_A.pop(len(discosT_A)-1))
        muestraDiscos()
    elif salida == "B" and llegada == "A":
        discosT_A.append(discosT_B.pop(len(discosT_B)-1))
        muestraDiscos()
    elif salida == "B" and llegada == "C":
        discosT_C.append(discosT_B.pop(len(discosT_B)-1))
        muestraDiscos()
    elif salida == "C" and llegada == "A":
        discosT_A.append(discosT_C.pop(len(discosT_C)-1))
        muestraDiscos()
    elif salida == "C" and llegada == "B":
        discosT_B.append(discosT_C.pop(len(discosT_C)-1))
        muestraDiscos()

def startAutoGame():
    sel = opr_cmbx.get()
    global partidaG, win
    if sel:
        sel = int(sel)
        if partidaG[0]:
            resetAll()
            partidaG[0] = False
            ruta.clear()
        calculaMovMin(sel)
        lbl_Movs["text"]="MOVIMIENTOS REALIZADOS: " + str(count_Movs[0])
        lbl_MovsMin["text"]="MOVIMIENTOS MINIMOS: " + str(count_Movs[1])
        generaDiscos(sel)
        partidaG[0] = True
        win[0]=True #Los discos no tendrán propiedad drag and drop
        iniciaRecorrido(sel, "A", "C", "B")
        recorrerMov(0)
    else:
        muestraMensaje("SELECCIONE UNA CANTIDAD DE DISCOS A USAR")

btn_Auto = tk.Button(ventana, text = "Mostrar Movimientos", width=18, command=startAutoGame)
btn_Auto.place(x=523, y= 30)

ventana.mainloop()
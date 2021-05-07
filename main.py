import tkinter as tk
from os import path
from tkinter import ttk
from tkinter import messagebox

def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease-1>", on_drop_motion)

def unmake_draggable(widget):
    widget.unbind("<Button-1>")
    widget.unbind("<B1-Motion>")
    widget.unbind("<ButtonRelease-1>")
# Variable de posición de origen
posXYIni = []
def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    posXYIni.clear()
    posXYIni.append(widget.winfo_x())
    posXYIni.append(widget.winfo_y())
    print("Start x:", posXYIni[0], "  y:", posXYIni[1])

areas = [
    [30,319,165,412], # Xi, Xf, Yi, Yf
    [420, 724, 165, 412],
    [810, 1114, 165, 412],
]
# Obtiene el área de origen
def obtainOrigin(origXY):
    if posXYIni[0] >= 30 and posXYIni[0] <= 319:
        return "A"
    elif posXYIni[0] >= 420 and posXYIni[0] <= 724:
        return "B"
    elif posXYIni[0] >= 810 and posXYIni[0] <= 1114:
        return "C"

# Función de movimiento de discos
def on_drop_motion(event):
    widget = event.widget
    x = widget.winfo_x() 
    y = widget.winfo_y() 
    origin = obtainOrigin(posXYIni)
    print("Origen", origin)
    if origin == "A":
        if y >= 165 and y <= 412:
            if x >= 420 and x <= 724:
                quitaD_N_D()
                if validaMov(origin, "B"):
                    discosT_B.append(discosT_A.pop(len(discosT_A)-1))
                    actualizaMov()
                muestraDiscos()
            elif x >= 810 and x <= 1114:
                quitaD_N_D()
                if validaMov(origin, "C"):
                    discosT_C.append(discosT_A.pop(len(discosT_A)-1))
                    actualizaMov()
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
                muestraDiscos()
            elif x >= 810 and x <= 1114:
                quitaD_N_D()
                if validaMov(origin, "C"):
                    discosT_C.append(discosT_B.pop(len(discosT_B)-1))
                    actualizaMov()
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
                muestraDiscos()
            elif x >= 420 and x <= 724:
                quitaD_N_D()
                if validaMov(origin, "B"):
                    discosT_B.append(discosT_C.pop(len(discosT_C)-1))
                    actualizaMov()
                muestraDiscos()
            else:
                widget.place(x=posXYIni[0], y=posXYIni[1])
        else:
            widget.place(x=posXYIni[0], y=posXYIni[1])

ventana = tk.Tk()
ventana.title("TORRES DE HANOI - MC2N")
ventana.geometry("1160x640") #tamaño ventana

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    # ventana.lift()
    print("Drop x:", x," ", widget.winfo_x(), "-", widget._drag_start_x, "+", event.x, " ||  y:", y, " ", widget.winfo_y(), "-", widget._drag_start_y, "+", event.y)

def getSource():
    ruta = path.dirname(path.abspath(__file__)) #Obtiene la ruta del script en ejecución
    return ruta

# GENERADOR DE TORRES
img_bases = []
bases = []
for j in range(3):
    ruta = getSource()
    img=tk.PhotoImage(file=ruta+"\\src\\base.png")
    img = img.subsample(2,2)
    img_bases.append(img)
    # print(img.height()) #307
    # print(img.width())  #334

for j in range(3):
    bases.append(tk.Label(ventana, image=img_bases[j]))
iniB_x = 15
for b in bases:
    b.place(x=iniB_x, y=180)
    iniB_x += 390

# DISCOS 183 x 57
# n_discos = 5
img_discos = []
discosT_A = []
discosT_B = []
discosT_C = []
count_Movs = [0]

def generaDiscos(n_discos):
    global img_discos, discosT_A
    for i in range(n_discos):
        # my_label_temp = tk.Label(ventana, image=img, bg="white")
        ruta = getSource()
        img = tk.PhotoImage(file=ruta+"\\src\\disco"+str(n_discos-i)+".png")
        img = img.subsample(2,2)
        # print(img.width())
        # print(img.height())  # constante 29
        img_discos.append([img, img.width()/2])
    for i in range(n_discos):
        discosT_A.append([tk.Label(ventana, image=img_discos[i][0]), img_discos[i][1]])

def usaD_N_D():
    if discosT_A:
        make_draggable(discosT_A[len(discosT_A)-1][0])
    if discosT_B:
        make_draggable(discosT_B[len(discosT_B)-1][0])
    if discosT_C:
        make_draggable(discosT_C[len(discosT_C)-1][0])

def quitaD_N_D():
    if discosT_A:
        unmake_draggable(discosT_A[len(discosT_A)-1][0])
    if discosT_B:
        unmake_draggable(discosT_B[len(discosT_B)-1][0])
    if discosT_C:
        unmake_draggable(discosT_C[len(discosT_C)-1][0])

def paintD(discos, ini_x):
    ini_y = 412
    for d in discos:
        pos_x_ini = ini_x - d[1]
        d[0].place(x=pos_x_ini, y=ini_y)
        ini_y -= 31
    usaD_N_D()

def muestraDiscos():
    global discosT_A, discosT_B, discosT_C
    paintD(discosT_A, 180)
    paintD(discosT_B, 570)
    paintD(discosT_C, 960)

def destruyeDiscos():
    if discosT_A:
        for d in discosT_A:
            d[0].destroy()
    if discosT_B:
        for d in discosT_B:
            d[0].destroy()
    if discosT_C:
        for d in discosT_C:
            d[0].destroy()

def resetAll():
    destruyeDiscos()
    img_discos.clear()
    discosT_A.clear()
    discosT_B.clear()
    discosT_C.clear()
    posXYIni.clear()
    count_Movs.clear()
    count_Movs.append(0)

def validaMov(salida, llegada):
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

def calculaMovMin(n_discos):
    min = 2**n_discos - 1
    count_Movs.append(min)

my_label = tk.Label(ventana, text="Ingrese la cantidad de discos a utilizar: ", font=20)
my_label.place(x= 35, y=30)
lbl_Info = tk.Label(ventana, text="INICIAR JUEGO", font=20)
lbl_Info.place(x= 525, y=550)

opr_cmbx = ttk.Combobox(ventana, state="readonly", font=20, width=5)
opr_cmbx["values"]=[1, 2, 3, 4, 5, 6, 7]
opr_cmbx.place(x=315, y= 30)

partidaG = [False]
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

btn = tk.Button(ventana, text = "Iniciar Juego", width=15, command=startGame)
btn.place(x=395, y= 30)

def actualizaMov():
    global count_Movs
    count_Movs[0] += 1
    lbl_Movs["text"]="MOVIMIENTOS REALIZADOS: " + str(count_Movs[0])

lbl_Movs = tk.Label(ventana, text="MOVIMIENTOS REALIZADOS: 0", font=60)
lbl_Movs.place(x=880, y=30)
lbl_MovsMin = tk.Label(ventana, text="MOVIMIENTOS MINIMOS: 0", font=60)
lbl_MovsMin.place(x= 880, y=70)

ventana.mainloop()
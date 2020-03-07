#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 03:14:21 2020

@author: arturo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 00:17:29 2019

@author: fpalm
"""

"""
Se declaran la librerias a usar en el codigo
"""
import sys #modulo que provee acceso a funciones y objetos mantenidos
# por del intérprete.

import random #modulo que contiene funciones para generar numeros aleatorios

"""libreria para importar la clase namedtuple, que sirve para acceder a los
campos de ella por nombre usando notacion punteada  """
from collections import namedtuple

from datetime import datetime #modulo para manejar fechas y horas

from sortedcontainers import SortedKeyList #modulo que contiene metodos de
#ordenamiento

#se crea Evento como una tupla de nombrem para acceder a los nombres
#tiempo, nodo y tipo
Evento = namedtuple("Evento", ["tiempo", "nodo", "tipo"])

#Esta clase crea los nodos que va a tener el sistema a simular
class Nodo:
    def __init__(
        # se crea los atributos de la clase, donde los parametrosson
        #tipo_n, el tipo de nodo
        #t_llegadas, tiempo de llegada de clientes
        #t_servicio, tiempo en ser atendido un cliente
        #capacidad, capacidad que tiene el nodo
        #suc, nodo sucesor
        #prob_suc
        self, tipo_n, t_llegadas, t_servicio, capacidad, suc, prob_suc
    ):
        #se crea el atributo tipo_n del objeto llamado tipo_n
        self.tipo_n = tipo_n
        
        #se crea el atributo t_llegadas del objeto llamado t_llegadas
        self.t_llegadas = float(t_llegadas)
        
        #se crea el atributo t_servicio del objeto llamado t_servicio
        self.t_servicio = float(t_servicio)
        
        #se crea el atributo capacidad del objeto llamado capacidad
        self.capacidad = int(capacidad)
        
        #se crea el atributo suc del objeto llamado i_suc
        self.i_suc = [int(s) for s in suc]
        
        #se crea el atributo prob_suc del objeto llamado prob_suc
        self.prob_suc = [float(ps) for ps in prob_suc]
        
        #se crea el atributo o del objeto llamado t_total_esp
        self.t_total_esp = 0
        
        #se crea el atributo 0 del objeto llamado tipo_even_prev
        self.t_even_prev = 0
        
        #se crea el atributo 0 del objeto llamado llegaron
        self.llegaron = 0
        
        #se crea el atributo 0 del objeto llamado cola
        self.cola = 0
        
        #se crea el atributo 0 del objeto llamado t_vacio
        self.t_vacio = 0
        
        #se crea el atributo 0 del objeto llamado cola_max
        self.cola_max = 0
        
        #se crea el atributo 0 del objeto llamado servidos
        self.servidos = 0
        
        #se crea el atributo 0 del objeto llamado util_pond
        self.util_pond = 0
        
        #se crea el atributo 0 del objeto llamado utilizacion
        self.utilizacion = 0
        
        #se crea el atributo 0 del objeto llamado cola_ini
        self.cola_ini = 0

#clase para crear las redes
class Red:
    
    def __init__(self, nodos): #se crea el metodo __init__ 
                               #y se asocia nodos al objeto. Y self que hace
                               #referencia al objeto alque van asociados
 
       self.nodos = nodos #se crea el atributo nodos del objeto llamado nodo
       
       for nodo in self.nodos:#recorre la instancia nodos
                              
            #rutina que recorre los nodos sucesores y lo alamacena en nodo.suc 
            nodo.suc = [nodos[i - 1] for i in nodo.i_suc]

    def imprime_red(self, a_salida=sys.stdout):#se crea el metodo imprime_red
                                               #con la asignacion sys.stdout
                                               #al objeto a_salida
                                               
        if type(a_salida) == str:#compara si es una cadena
            f = open(a_salida, "w+")#si lo esz abre el archivo para copiar en el 
        else:
            f = a_salida #sino no es cadena no hace nada
            
        for i, nodo in enumerate(self.nodos):#recorrido por los nodos
            
            #escribe en el archivo de salida los nodos encontrados
            f.write(f"Nodo: {i+1:2d}    Tipo: {nodo.tipo_n.title()}\n")
            
            if nodo.tipo_n == "llegada":#si el nodo es de tipo llegada
                #ecribe el el archivo el nodo de llega con dos decimales
                f.write(f"T_E_llegadas: {nodo.t_llegadas:.2f}    ")
            f.write(
                f"T_Servicio: {nodo.t_servicio:.2f}    Capacidad: {nodo.capacidad:2d}\n"
            )
            if nodo.suc:#si nodo es sucesor
                #crea la lista l_suc y con el for recorre los nodos sucesores
                #y crea una tupla con los valores encontrados dentro de la iteracion
                l_suc = [
                    f"{i_suc} ({prob_suc})"
                    for i_suc, prob_suc in zip(nodo.i_suc, nodo.prob_suc)
                ]
                #convierte la lista l_suc en una cadena de texto con el
                #delimitador " "
                suc = "    ".join(l_suc)
            else:
                #de lo contrario escribe en el archivo el sucesor vacio
                suc = ""
            f.write(f"Sucesores: {suc}\n\n")
            
        if type(a_salida) == str:#si el archivo de salida es de tipo cadena
            f.close()#cierra el archivo

    #se crea el metodo imprime_salida, con losobjetos YSIM, t_dif y a_salida
    def imprime_salida(self, TSIM, t_dif, a_salida=sys.stdout):
        if type(a_salida) == str:#si el archivo de salida es cadena
            f = open(a_salida, "a+")#abre el archivo d salida
        else:
            f = a_salida #si no es leible se deja igual
        t_dif += datetime(2020, 1, 1, 0, 0, 0)#icrementa el valor de tiempo de simulacion
        f.write(f"Tiempo de simulacion: {TSIM:8.0f}    ")#y lo escribe en el archivo
        secs = f"{t_dif.second + t_dif.microsecond / 1e6:.2f}"  # f'{dif:%-S.%f}'[:-4]
        
        #escribe el tiempo de corrida en el archivo
        f.write(f"Tiempo de corrida: {t_dif:%-H} h {t_dif:%-M} m {secs} s\n")
        
        #formato para mostrar las variables en el archivo de salida
        f.write(
            "Nod Llega  Servi  EnSer LCol  LColM ColI  TProEsp LProCol  T Vacio  OcupPro\n"
        )
        f.write(
            "=== ====== ====== ===== ===== ===== ===== ======= ======= ========= =======\n"
        )
        for i, nodo in enumerate(self.nodos):#recorre los nodos
            if nodo.utilizacion == 0:#compara si esta disponible 
                nodo.t_vacio += TSIM - nodo.t_even_prev#y calcula el valor y lo
                #guarda en el objeto t_vacio de nodo
            else:
                #de lo contrario se calcula los valores cuando esta utilizado
                nodo.util_pond += nodo.utilizacion * (TSIM - nodo.t_even_prev)
                nodo.t_total_esp += nodo.cola * (TSIM - nodo.t_even_prev)
                #y lo escribe en el archivo de salida
            f.write(
                f"{i + 1:3d} {nodo.llegaron:6d} {nodo.servidos:6d} {nodo.utilizacion:5d} "
            )
            f.write(f"{nodo.cola:5d} {nodo.cola_max:5d} {nodo.cola_ini:5d} ")
            f.write(
                f"{nodo.t_total_esp / nodo.llegaron:7.1f} {nodo.t_total_esp / TSIM:7.1f} "
            )
            f.write(f"{nodo.t_vacio:9.2f} {nodo.util_pond / TSIM:7.2f}\n")
        if type(a_salida) == str:
            f.close()#se cierra el archivo


def lee_red(a_entrada):#metodo lee_read que contiene la variable a_entrada

    with open(a_entrada) as arch_red:#abre el archivo de entrada
        
        #lee la linea y asigna el primer valor a TSIM, que es el tiempo de simulacion
        #y asigna el nmero de clientes a num_cli
        TSIM, num_cli = arch_red.readline().strip().split()[:2]
        nodos = []#crea la lista nodos
        otro_nodo = arch_red.readline().strip()[:1]#asigna el valor de la linea
        #del nodo de tipo otro
        while otro_nodo:#mientras nodo sea del tipo otro
            tipo = otro_nodo#variable auxiliar para manejar el valor de otro nodo
            if tipo == "1":#compara si es 1 para saber si es de llegada
                tipo_n = "llegada"
                
                #y asigna los valores d etiempo de llegada, tiempo de servicio
                #y la capacida a cada variable respectivamente 
                t_llegadas, t_servicio, capacidad = (
                    arch_red.readline().strip().split()[:3]
                )
            else:#si el nodo no es de llegada por lo tanto es de tpo otro
                tipo_n = "otro"
                t_llegadas = "0"
                #asigna los valores encontrados en la linea a cada varible
                #t_servicio y capacidad
                t_servicio, capacidad = arch_red.readline().strip().split()[:2]
                
                #lee en la linea el nodo sucesor
            num_suc = int(arch_red.readline().strip()[:1])
            if num_suc != 0:#si es diferente de cero
                #lo guarda en la variable suc
                suc = arch_red.readline().strip().split()[:num_suc]
                prob_suc = arch_red.readline().strip().split()[:num_suc]
            else:#de lo contrario se deja vacio
                suc = []
                prob_suc = []
                #se asigna a nodo la tupla Nodo con los valores
            nodo = Nodo(
                tipo_n, t_llegadas, t_servicio, capacidad, suc, prob_suc
            )
            nodos.append(nodo)#agrega los valores de nodo a la lista nodoss
            otro_nodo = arch_red.readline().strip()[:1]#lee otro nodo
        red = Red(nodos)#se crea una red con los nodos
        i = 0
        num_cli = int(num_cli)#el numero de clientes
        for j in range(num_cli):#recorre el valor de num_clientes
            red.nodos[i].cola += 1#y va creando la cola que hacen los clientes
            i += 1#incremeta ll
            if i >= len(red.nodos):#sil es mayor al valor medido de nodos
                i = 0#l seraigual a cero
    return red, float(TSIM)#retorna la red y el tiemp de simulacionn


def inicia_LEP(red):#metodo para leer la red de nodos
    
    LEP = SortedKeyList(key=lambda evento: evento.tiempo)#ordena la lisra de eventos
    for nodo in red.nodos:#recorre la red de nodos
        if nodo.tipo_n == "llegada":
            evento = Evento(
                random.expovariate(1 / nodo.t_llegadas), nodo, "llegada_e"
            )
            LEP.add(evento)
    return LEP


if __name__ == "__main__":
    random.seed(5)
    a_entrada = sys.argv[1]
    red, TSIM = lee_red(a_entrada)
    a_salida = sys.argv[2]
    red.imprime_red(a_salida)
    t_inicial = datetime.now()
    tiempo_sim = 0
    LEP = inicia_LEP(red)
    while tiempo_sim < TSIM:
        evento = LEP.pop(0)
        tiempo_sim = evento.tiempo
        nodo = evento.nodo
        nodo.t_total_esp += nodo.cola * (tiempo_sim - nodo.t_even_prev)
        nodo.util_pond += nodo.utilizacion * (tiempo_sim - nodo.t_even_prev)
        if evento.tipo != "salida":
            nodo.llegaron += 1
            if nodo.utilizacion == nodo.capacidad:
                nodo.cola += 1
                if nodo.cola > nodo.cola_max:
                    nodo.cola_max = nodo.cola
            else:
                if nodo.utilizacion == 0:
                    nodo.t_vacio += tiempo_sim - nodo.t_even_prev
                evento_n = Evento(
                    tiempo_sim + random.expovariate(1 / nodo.t_servicio),
                    nodo,
                    "salida",
                )
                LEP.add(evento_n)
                nodo.utilizacion += 1
            if evento.tipo == "llegada_e":
                evento_n = Evento(
                    tiempo_sim + random.expovariate(1 / nodo.t_llegadas),
                    nodo,
                    "llegada_e",
                )
                LEP.add(evento_n)
        else:
            if len(nodo.suc) > 0:
                nodo_i = random.choices(nodo.suc, cum_weights=nodo.prob_suc)[0]
                evento_n = Evento(tiempo_sim, nodo_i, "llegada_i")
                LEP.add(evento_n)
            nodo.servidos += 1
            if nodo.cola > 0:
                nodo.cola -= 1
                evento_n = Evento(
                    tiempo_sim + random.expovariate(1 / nodo.t_servicio),
                    nodo,
                    "salida",
                )
                LEP.add(evento_n)
            else:
                nodo.utilizacion -= 1
        nodo.t_even_prev = tiempo_sim

    t_final = datetime.now()
    t_dif = t_final - t_inicial
    red.imprime_salida(TSIM, t_dif, a_salida)

import random
import math
import simpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

SEMILLA=30
NUM_TRABAJADORES=5
T_LLEGADAS=1.6
TIEMPO_SIMULACION=9200
TOT_CLIENTES=50

te=0.0
dt=0.0
fin=0.0
a=3.91
def facturacion(personas):
    global dt
    global a
    R = random.random()#obtener numero aleatorio
    #tiempo=np.random.weibull(a , 7.76)
    tiempo=int(random.weibullvariate(3.91,7.76))
    yield env.timeout(tiempo)#deja correr el tiempo n minutos
    print("\o/ Facturacion lista a %s en %.2f minutos" % (personas,tiempo))
    dt = dt + tiempo#acumula los tiempos


def personas(env, name, personal):
    global te
    global fin
    llega=env.now#guarda el minuto de llegada del cliente
    print("---> %s llego al aeropuerto en minuto %.2f" % (name,llega))
    with personal.request() as request:#espera turno
        yield request#obtiene turno
        pasa=env.now#guarda los minutos cuando comienza a ser atendido
        espera=pasa - llega#calcula el tiempoque espero
        te=te+espera#acumula lostiemposde espera
        print("***%s pasa a facturacion en minuto %.2f y espero %.2f" % (name, pasa, espera))
        yield env.process(facturacion(name))#invoca el proceso facturacion
        deja=env.now#guarda el minuto en que termina de ser atendido
        print("<-- %s deja aeropuerto en minuto %.2f" % (name, deja))
        fin=deja#conserva globalmente el ultimo minuto de la simulacion



def principal(env,personal):
    llegada = 0
    i = 0
    while True:
    #for i in range(TOT_CLIENTES):#para n clientes
        R=random.random()
        llegada=-T_LLEGADAS*math.log(R)#distribucion exponencial
        yield env.timeout(llegada)#deja trancurrir un tiempo entre uno y otro
        i += 1
        env.process(personas(env, 'Personas %d' % i,personal))

print("----------Bienvenido Simulacion Aeropuerto-------------")
random.seed(SEMILLA) #cualquier valor
env=simpy.Environment()#crea el objeto entorno de simulacion
personal=simpy.Resource(env, NUM_TRABAJADORES)#crea los recursos(trabajadores)
env.process(principal(env,personal))#invoc el proceso principal
#env.run()#inicia la simulacion
env.run(until = TIEMPO_SIMULACION)
print ("\n---------------------------------------------------------------------")
print ("\nIndicadores obtenidos: ")

lpc = te / fin
print ("\nLongitud promedio de la cola: %.2f" % lpc)
tep = te / TOT_CLIENTES
print ("Tiempo de espera promedio = %.2f" % tep)
upi = (dt / fin) / NUM_TRABAJADORES
print ("Uso promedio de la instalacion = %.2f" % upi)
print ("\n---------------------------------------------------------------------")
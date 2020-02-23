#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 23:03:35 2020

@author: fpalm
"""


import random
import simpy
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

stats = {
    "ncar_a": 0,
    "ncar_b": 0,
    "env_a": 0,
    "env_b": 0,
    "des_a": 0,
    "des_b": 0,
    "prep_a": [],
    "prep_b": [],
    "en_pru": [],
    "retrab": [],
}
teca=0.0
teprep_a=0.0
teen_prua=0.0
teretraba=0.0
finca=0.0
finprep_a=0.0
finen_prua=0.0
finretraba=0.0
dt=0.0
finca=0.0
tea=0.0
dt=0.0
fina=0.0
def monitor(num, ress, res, stats):
    item = (num, ress[res]._env.now, ress[res].count, len(ress[res].queue))
    stats[res].append(item)


def service(num, ress, res, variate, params):
    monitor(num, ress, res, stats)
    with ress[res].request() as solicitud:
        monitor(num, ress, res, stats)
        yield solicitud
        monitor(num, ress, res, stats)
        yield env.timeout(variate(*params))
        monitor(num, ress, res, stats)


def carcasa_a(num, env, ress, stats):

    global teprep_a , finprep_a,teen_prua , finen_prua,teretraba , finretraba 
    llegoprep_a=env.now#guarda el tiempo de llegada
    llegoen_prua=env.now#guarda el tiempo de llegada para prueba
    
    yield from service(num, ress, "prep_a", random.triangular, (1, 4, 8))
    pasoprep_a=env.now#tiempo cuando comienza el servicio
    esperoprep_a=pasoprep_a-llegoprep_a#tiempo de espera
    teprep_a=teprep_a+esperoprep_a#acumulador
    yield from service(num, ress, "en_pru", random.triangular, (1, 3, 4))
    dejaprep_a=env.now#termino el proceso prep_a
    finprep_a=dejaprep_a#guarda el tiempo
    pasoen_prua=env.now#tiempo de comienzo de en_pru
    esperoen_prua=pasoen_prua-llegoen_prua#tiempo de espera en_pru
    teen_prua=teen_prua+esperoen_prua#acumulador
    
    if random.random() > 0.91:
        llegoretraba=env.now#cuando llega a ser retrab
        yield from service(num, ress, "retrab", random.expovariate, (1 / 45, ))
        pasoretraba=env.now#comienza retrab
        esperoretraba=pasoretraba-llegoretraba#espero en retrab
        teretraba=teretraba+esperoretraba#acumulador retrab
        if random.random() > 0.80:
            stats["des_a"] += 1
        else:
            stats["env_a"] += 1
    else:
        stats["env_a"] += 1
        dejaretraba=env.now#termina retrab
        finretraba=dejaretraba#guarda retrab
    dejaen_prua=env.now#termina en_pru
    finen_prua=dejaen_prua#guarda en_pru 


def carcasa_b(num, env, ress, stats):

    yield from service(num, ress, "prep_b", random.triangular, (3, 5, 10))
    yield from service(num, ress, "en_pru", random.weibullvariate, (2.5, 3.5))
    if random.random() > 0.91:
        yield from service(num, ress, "retrab", random.expovariate, (1 / 45, ))
        if random.random() > 0.80:
            stats["des_b"] += 1
        else:
            stats["env_b"] += 1
    else:
        stats["env_b"] += 1


def llegada_a(env, ress, stats):
    global tea
    global fina
    llegoa=env.now#tiemp que llega en llega_a
    while True:
        pasoa=env.now#comienza el proceso llega_a
        stats["ncar_a"] += 1
        env.process(carcasa_a(stats["ncar_a"], env, ress, stats))
        esperoa=pasoa-llegoa#espera en llega_a
        tea=tea+esperoa#acumula llega_a
        yield env.timeout(random.expovariate(1 / 5))
        dejaa=env.now#termina llega_a
        fina=dejaa#acumula llega_a


def llegada_b(env, ress, stats):
    while True:
        for i in range(4):
            stats["ncar_b"] += 1
            env.process(carcasa_b(stats["ncar_a"], env, ress, stats))
        yield env.timeout(random.expovariate(1 / 30))


env = simpy.Environment()
prep_a = simpy.Resource(env, capacity=1)
prep_b = simpy.Resource(env, capacity=1)
en_pru = simpy.Resource(env, capacity=1)
retrab = simpy.Resource(env, capacity=1)

ress = {"prep_a": prep_a, "prep_b": prep_b, "en_pru": en_pru, "retrab": retrab}

env.process(llegada_a(env, ress, stats))
env.process(llegada_b(env, ress, stats))
env.run(1920)

columns=['num', 't', 'uso', 'cola']

def plot_nodo(stats, nodo, columns):
    df = pd.DataFrame(stats[nodo], columns=columns)
    df.set_index('t', inplace=True)
    df.plot(y=['uso', 'cola'], title=f"nodo {nodo}", drawstyle="steps", subplots=True)

plot_nodo(stats, "prep_a", columns)
plot_nodo(stats, "prep_b", columns)
plot_nodo(stats, "en_pru", columns)
plot_nodo(stats, "retrab", columns)

mcllega_a = tea / fina
print ("\nTamano medio de la cola en el nodo de llegada_a para carcasa a: %.2f" % mcllega_a)
mcprep_a = teprep_a / finprep_a
print ("\nTamano medio de la cola en el nodo de prep_a para carcasa a: %.2f" % mcprep_a)
mcen_pruba = teen_prua / finen_prua
print ("\nTamano medio de la cola en el nodo de en_prua para carcasa a: %.2f" % mcen_pruba)
mcretraba = teretraba / finretraba
print ("\nTamano medio de la cola en el nodo de retraba para carcasa a: %.2f" % mcretraba)




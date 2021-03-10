from random import uniform
import numpy as np

def pesos_4(*num):
    pesos = np.array([uniform(-1, 1) for i in range(4)])
    return pesos


def pesos_2(*num):
    pesos_2 = np.array([uniform(-1, 1) for i in range(2)])
    return pesos_2

def peso_final(*num):
    peso_fim = np.array([uniform(-1, 1) for i in range(2)])
    return peso_fim
    
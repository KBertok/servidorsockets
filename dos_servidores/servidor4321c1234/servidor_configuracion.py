#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 18:42:01 2019

@author: klaus
"""

# Tabla estudiante,campos para el caso de archivo plano 

Nombre   = 0
Apellido = 1
Cedula   = 2
Login    = 3
Password = 4

IPSAUTORIZADAS=['127.0.0.1','192.168.0.10']

LONGITUD_PASSWORD=8
ALFABETO="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALFABETO_OPCIONAL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
PASSWORD_SOLO_CON_LETRAS=True

BASEDEDATOS='servidor_BD_examenes.db'

NUMERO_PREGUNTAS_TOTALES=30
NUMERO_PREGUNTAS_ESCOGER=5
ALEATORIO_DESORDENADO=True


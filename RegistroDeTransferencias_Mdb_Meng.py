#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################
#Autor: Jesus Marin                                                      #
#web: http://www.jam.net.ve                                              #
#Lenguaje: Python  2.6                                                   #
#RegistroDeTransferencias Beta                                           #
#Descripcion: Sencilla aplicacion de consola para llevar un registro de  #
# los datos de subida-bajada consumidos en internet.                     #
##########################################################################


from mongoengine import *
from datetime import *
from time import *



class Rsubida(Document):
    subida = FloatField()
    fecha_agregado = StringField()
    hora_agregado = StringField()

class Rbajada(Document):
    bajada = FloatField()
    fecha_agregado = StringField()
    hora_agregado = StringField()



#funcion que imprime una linea en blanco
def espacio():
    print

#funcion para convertir bytes a Megabytes
def bytestomb(b):
    mb = float(b) / (1024*1024)
    return mb

#definiendo la funcion "consultas" con algunas consultas
def consultas():
    espacio()
    print "Total datos Bajada: " + str(Rbajada.objects.sum("bajada")) + " MB"
    print "Total datos Subida: " + str(Rsubida.objects.sum("subida")) + " MB"
    tbajada = Rbajada.objects.sum("bajada")
    tsubida = Rsubida.objects.sum("subida")
    total = tbajada + tsubida
    print "Total Consumido: " + str(total) + " MB"
 
 
print "Conectando a la Base de datos en la instancia Local"

connect("bdregtransf")

#llamando a la funcion de consulta
consultas()

###### Codigo que extrae los datos de subida/bajada de la interfaz PPP0 #########
#Cambie ppp0 por su interfaz a monitorear
interface= 'ppp0'                                                               
for line in open('/proc/net/dev', 'r'):                                         
    if interface in line:                                                       
        data = line.split('%s:' % interface)[1].split()                         
        rx_bytes, tx_bytes = (data[0], data[8])                                 
#################################################################################

la_subida = bytestomb(tx_bytes)
la_bajada = bytestomb(rx_bytes)

fecha = date.today()
fechaagregado = fecha.strftime("%d-%m-%y")
horaagregado = strftime("%I:%M %p")

espacio()
print "Los datos ingresados son:"
espacio()
print "Subida: " + str(la_subida) + " MB"
print "Bajada: " + str(la_bajada) + " MB"
print "Fecha Agregado " + fechaagregado
print "Hora Agregado " + horaagregado

espacio()
respuesta = raw_input("Deseas anadir este registro? introdusca solo (s/n): ")
if respuesta == "s":

    regsubida = Rsubida(subida = la_subida, fecha_agregado = fechaagregado, hora_agregado = horaagregado)
    regbajada = Rbajada(bajada = la_bajada, fecha_agregado = fechaagregado, hora_agregado = horaagregado)

    regsubida.save()
    regbajada.save()
    print "Registros de Subida y Bajada ALMACENADOS con Exito!"
    consultas()
else:
    print "Cancelado!!!"

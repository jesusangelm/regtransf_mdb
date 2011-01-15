#! /usr/bin/env python

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
    
print "Conectando a la Base de datos en la instancia Local"
#Conectando a la instancia MongoDB local en la base de datos "bdregistrotransgerenciamdb"
connect("bdregistrotransgerenciamdb")

while True:
    try:
        la_subida = float(raw_input('Introdusca la cantidad de datos Enviados: '))
        la_bajada = float(raw_input('Introdusca la cantidad de datos Recibidos: '))
        break
    except ValueError:
        print "Solo se permiten numeros... Intente nuevamente."

fecha = date.today()
fechaagregado = fecha.strftime("%d-%m-%y")
horaagregado = strftime("%I:%M %p")

print "Los datos ingresados son:"
print "Subida: " + str(la_subida)
print "Bajada: " + str(la_bajada)
print "Fecha Agregado " + fechaagregado
print "Hora Agregado " + horaagregado

respuesta = raw_input("Estos datos son correctos? introdusca solo (s/n): ")

if respuesta == "s":
    regsubida = Rsubida(subida = la_subida, fecha_agregado = fechaagregado, hora_agregado = horaagregado)
    regbajada = Rbajada(bajada = la_bajada, fecha_agregado = fechaagregado, hora_agregado = horaagregado)

    regsubida.save()
    regbajada.save()
    print "Registros de Subida y Bajada ALMACENADOS con Exito!"


else:
    print "Cancelado!!!"


#Algunas consultas
respuesta = raw_input("Deseas ver algunas consultas? introdusca solo (s/n): ")

if respuesta == "s":
    #Mostrando todos los registros de bajada en la coleccion
    for rbajada in Rbajada.objects:
        print "Bajada: " + str(rbajada.bajada)

    #Sumatoria de todos los registros de bajada :)
    print "Total datos Bajada: " + str(Rbajada.objects.sum("bajada")) + " MB"
    print "Total datos Subida: " + str(Rsubida.objects.sum("subida")) + " MB"
    tbajada = Rbajada.objects.sum("bajada")
    tsubida = Rsubida.objects.sum("subida")
    total = tbajada + tsubida
    print "Total Consumido: " + str(total) + " MB"

else:
    print "Cancelado!"


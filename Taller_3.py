import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import math


import math

def rotate(Origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given Origin.

    The angle should be given in radians.
    """
    ox, oy = Origin # Se toman los puntos de origen
    px, py = point # Se toman los puntos de destino

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy) # Se calcula nuevo punto rotado
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy) # Se calcula nuevo punto rotado

    return qx, qy # Retornar valores




class imageShape: # Se define la clase

    def __init__(self, width, height):    # Se define el constructor
        self.width = width # Toma el valor de ancho
        self.height = height # Toma el valor del alto

    def generateShape(self):
        Num = np.random.randint(0,4) # Se genera u nuevo numero aleatorio
        self.image = np.zeros((self.height,self.width, 3), np.uint8) # Se genera una matriz en 0

        rd_width = round(self.width / 2) # Se toma la mitad del ancho
        rd_height = round(self.height / 2) # Se toma la mitad del alto

        L = int(min(self.height, self.width) / 2) # Se toma la mitad del valor minimo
        X = round(math.sqrt((L) ** 2 - (L / 2) ** 2)) # Se halla el cateto opuesto
        R = int(L / 2) # Se halla el radio
        L_H = rd_width
        L_V = rd_height

        if Num == 0:
            #cv2.line(self.image, (rd_width - L, rd_height), (rd_width + L, rd_height), (255, 255, 0), 1)

            triangle = np.array([[rd_width - (L / 2), rd_height + (X / 2)], [rd_width + (L / 2), rd_height + (X / 2)], [rd_width, -X + rd_height + (X / 2)]], np.int32) # Puntos del triangulo
            #cv2.polylines(self.image, [triangle], True, (255,255,0), thickness=1)
            cv2.fillPoly(self.image, [triangle], (255,255,0)) # Se dibujan los puntos en la matriz

            self.tipo_img = "triangulo"


        elif Num == 1:
            #cv2.rectangle(self.image, (rd_width - int(L / 2), rd_height + int(L / 2)), (rd_width + int(L / 2), rd_height - int(L / 2)), (255, 255, 0), -1)
            #cv2.line(self.image, (rd_width - int(L / 2), rd_height + int(L / 2)), (rd_width + int(L / 2), rd_height - int(L / 2)), (255, 255, 0), 1)

            #cv2.rectangle(self.image, (int(qx2),int(qy2)),(int(qx1),int(qy1)), (255, 255, 0), -1)

            P1 = [rd_width - int(L / 2), rd_height + int(L / 2)] # Se toman los puntos del cuadrado
            P2 = [rd_width + int(L / 2), rd_height + int(L / 2)] #
            P3 = [rd_width + int(L / 2), rd_height - int(L / 2)] #
            P4 = [rd_width - int(L / 2), rd_height - int(L / 2)] #

            qx1, qy1 = rotate([rd_width, rd_height],P1,math.radians(45)) # Se rotan los puntos
            qx2, qy2 = rotate([rd_width, rd_height], P2, math.radians(45)) #
            qx3, qy3 = rotate([rd_width, rd_height], P3, math.radians(45)) #
            qx4, qy4 = rotate([rd_width, rd_height], P4, math.radians(45)) #

            square = np.array([[(qx1,qy1)], [(qx2, qy2)], [(qx3, qy3)], [(qx4, qy4)]], np.int32) # Se define la matriz de los puntos del cadrado
            cv2.fillPoly(self.image, [square], (255,255,0)) # Se dibuja el cuadrado

            self.tipo_img = "Cuadrado"


        elif Num == 2:
            cv2.rectangle(self.image, (rd_width - int(L_H / 2), rd_height + int(L_V / 2)), (rd_width + int(L_H / 2), rd_height - int(L_V / 2)), (255, 255, 0), -1) # Puntos del rectangulo

            self.tipo_img = "Rectangulo"

        elif Num == 3:
            cv2.circle(self.image, (rd_width, rd_height), R, (255, 255, 0), -1) # Se dibuja el circulo

            self.tipo_img = "Circulo"

        self.Area_Tri = (L * X) / 2 # Se hallan las areas de las figuras geometricas
        self.Area_Sqr = L ** 2 #
        self.Area_Rect = L_H * L_V #
        self.Area_circ = math.pi * (R) ** 2 #


    def showShape(self):
        cv2.imshow('IMAGEN', self.image)  # Se muestra la imagen
        cv2.waitKey(5000)  # Espera 5 segundos
        cv2.destroyAllWindows()  # Cierra las ventanas


    def getShape(self):
        return self.image,self.tipo_img # Se retorna el tipo de imagen y la imagen


    def whatShape(self,Imagen):
        Image_gray = cv2.cvtColor(Imagen, cv2.COLOR_BGR2GRAY) # Se convierte la imagen a escala de grises
        _, Ibw_shapes = cv2.threshold(Image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # Se toma el umbral binario
        Contours, _= cv2.findContours(Ibw_shapes, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Saca el controno de la figura

        for idx, i in enumerate(Contours):
            M = cv2.moments(Contours[idx]) # Se sacan los momentos del contorno
            N = cv2.contourArea(Contours[idx]) # Se saca el area del contorno
            Area = M["m00"] # Se toma el primer momento

        if ((Area - int(Area * 0.01)) <= self.Area_Tri) and ((Area + int(Area * 0.01)) >= self.Area_Tri): # Se compara el area encontrada con la calculada con una variacion de +-1
            return ("Triangulo")
            print ("Triangulo")
        elif ((Area - int(Area * 0.01)) <= self.Area_Sqr) and ((Area + int(Area * 0.01)) >= self.Area_Sqr): # Se compara el area encontrada con la calculada con una variacion de +-1
            return ("Cuadrado")
            print ("Cuadrado")
        elif ((Area - int(Area * 0.01)) <= self.Area_Rect) and ((Area + int(Area * 0.01)) >= self.Area_Rect): # Se compara el area encontrada con la calculada con una variacion de +-1
            return ("Rectangulo")
            print("Rectangulo")
        elif ((Area - int(Area * 0.01)) <= self.Area_circ) and ((Area + int(Area * 0.01)) >= self.Area_circ): # Se compara el area encontrada con la calculada con una variacion de +-1
            return ("Circulo")
            print("Circulo")



if __name__ == '__main__':

    while (1):
        print("\n" + "A- Ingresar dimensiones")  # Se imprime en consola
        print("B- Generar figura")  # Se imprime en consola
        print("C- Visualizar imagen")  # Se imprime en consola
        print("D- Clasificar figura")  # Se imprime en consola
        print("?- Salir" + "\n")  # Se imprime en consola
        Entrada = input("Escoja una opcion: ")  # Se pide un valor

        if (Entrada == 'A'):
            width = input("Ingrese el ancho: ")
            height = input("Ingrese el alto: ")
        elif (Entrada == 'B'):
            F_geo = imageShape(int(width), int(height))
        elif (Entrada == 'C'):
            F_geo.generateShape()
            F_geo.showShape()
        elif (Entrada == 'D'):
            Imagen, Tipo_Imagen = F_geo.getShape()
            Tipo_Imagen_1 = F_geo.whatShape(Imagen)

            if Tipo_Imagen == Tipo_Imagen_1:
                print("La clasificacion es correcta, " + Tipo_Imagen_1)
            else:
                print("La clasificacion no es correcta")
        else:
            break  # Rompe while

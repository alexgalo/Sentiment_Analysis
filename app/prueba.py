class Clase_Funciones:
    # Agrega los 5 valores maximos
    def funcion1(self):
        print('Script prueba')
        numeros = list()
        numeros= [100, 2, 4, 6, 8, 10, 100, 20]
        elegidos = list()
        ordenados= list()
        ordenados= sorted(numeros)
        
        elegidos.append(ordenados[-1])
        elegidos.append(ordenados[-2])
        elegidos.append(ordenados[-3])
        elegidos.append(ordenados[-4])
        elegidos.append(ordenados[-5])
        
        print(elegidos)
        

if __name__ == '__main__':
    instancia = Clase_Funciones()
    instancia.funcion1()
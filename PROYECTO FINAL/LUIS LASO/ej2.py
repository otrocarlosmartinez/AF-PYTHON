from datetime import date, datetime

'''
    Metodo auxiliar para construir ventas
'''
def buildVenta(line):
    elements = line.split(",")
    return Venta(elements[0], int(elements[1]), float(elements[2]), datetime.strptime(elements[3], "%d/%m/%Y"))

'''
    Representa una venta
'''
class Venta():
    def __init__(self, nombre, cantidad, precio_unidad: float, fecha: date) -> None:
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio_unidad = precio_unidad
        self.__fecha = fecha
        
    def getNombre(self):
        return self.__nombre
    
    def getCantidad(self):
        return self.__cantidad
    
    def getPrecioUnidad(self):
        return self.__precio_unidad
    
    def getFecha(self):
        return self.__fecha
    
    def toLine(self):
        return "{},{},{},{}\n".format(self.__nombre, self.__cantidad, self.__precio_unidad, self.__fecha.strftime("%d/%m/%Y"))

'''
    Conjunto de ventas y operaciones que podemos hacer con ella
'''
class Ventas():
    def __init__(self, ventas) -> None:
        self.__ventas = ventas
        
    def getVentas(self):
        return self.__ventas
    
    def consultarVentas(self, fecha1: date, fecha2: date):
        if(fecha1 == fecha2):
            raise ValueError("Las fechas de consulta no pueden ser la misma")
        if(fecha1 > fecha2):
            temp = fecha1
            fecha1 = fecha2
            fecha2 = temp
        date1 = datetime.strptime(fecha1, "%d/%m/%Y")
        date2 = datetime.strptime(fecha2, "%d/%m/%Y")
        return list(filter(lambda x : date1 < x.getFecha() < date2, self.__ventas))

'''
    Leer y escribir a un archivo
'''
class ArchivoCSV():
    def __init__(self, path_to_file) -> None:
        self.__path_to_file = path_to_file
    
    def leerArchivo(self):
        
        ventas = []
        
        try:
            file = open(self.__path_to_file)
            
            lines = file.readlines()
            
            for line in lines:
                if line != "\n":
                    ventas.append(buildVenta(line.strip()))
                    
            file.close()
                
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print("Something went wrong while loading sells from file")
            print(e)
        else:
            print("Sells loaded successfully")
            return ventas
            
    def escribirArchivo(self, venta):
        
        try:
            file = open(self.__path_to_file, "a+")
            
            file.write(venta.toLine())
            
            file.close()
        except Exception as e:
            print("Something went wrong while writing sells")
            print(e)
        else:
            print("Sell written on file successfully")

'''
    Codigo principal con el flujo de trabajo
'''
archivo = ArchivoCSV("ventas.csv")

entrada = input("Elija si desea registrar una venta(REGISTRAR), consultar ventas(CONSULTAR) o salir(SALIR): ")

while(entrada != "SALIR"):
    
    match entrada:
        case "REGISTRAR":
            nombre = input("Introduzca el nombre del producto: ")
            cantidad = int(input("Introduzca la cantidad del producto: "))
            precio_unidad = float(input("Introduzca el precio por unidad del producto: "))
            
            archivo.escribirArchivo(Venta(nombre, cantidad, precio_unidad, date.today()))
            
        case "CONSULTAR":
            first_date = input("Introduzca una fecha en formato dia/mes/año: ")
            second_date = input("Introduzca otra fecha en formato dia/mes/año: ")
            
            try:
                lista_ventas = archivo.leerArchivo()
                
                ventas = Ventas(lista_ventas)
                
                ventas_en_rango = ventas.consultarVentas(first_date, second_date)
                
                print("----------------------------------------------\n")
                
                for venta in ventas_en_rango:
                    print(venta.toLine())
                    print("----------------------------------------------\n")
            except Exception as e:
                print(e)
                      
    entrada = input("Elija si desea registrar una venta(REGISTRAR), consultar ventas(CONSULTAR) o salir(SALIR): ")
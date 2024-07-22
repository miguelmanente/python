# Realice un ejercicio que convierta un número en romano y devuelva el número en entero

class Romano:
    def __init__(self, romano):
        self.romano = romano
    
    def chequeo(self, romano):                                                            # Constructor
        if (type(romano) != str):                                                         #Chequea que sea una cadena de letras
            print("El numero romano no es valido")
        elif (romano != romano.upper()):                                                    # Chequear si la cadena de letras está en minúsculas
            romano =romano.upper()
            print("El numero romano ",romano, "es = ", nRomano.convertirRaE(romano))       # Llamado al método conertir de Romano a Entero
        elif (romano == romano.upper()):                                                   # Chequear si la cadena de letras está en mayúsculas
            print("El numero romano ",romano, "es = ", nRomano.convertirRaE(romano))        
    
    def convertirRaE(self, romano):                                                          # método que convierte de romano a número entero
        romanos = {'I': 1, 'V': 5, 'X': 10,
               'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        prev = 0
        for letra in romano[::-1]:
            valor = romanos[letra]
            total += valor if valor >= prev else -valor
            prev = valor

        return total
  
romano = input("Ingrese un numero romano en mayusculas:  ")                                 # Ingreso del numero romano 

nRomano = Romano(romano)                                                                    # Instanciación del objeto nRomano
nRomano.chequeo(romano)                                                                     # Llamado al método Chequeo

 


""" print(format("hola","*<30"))   # Coloca la palabra Hola a la izquierda y luego coloca los 30 asteriscos

print(format('Menu',"*^30s"))  # Coloca la palabra Menu al centro  y repartido los 30 asteriscos

print(format("Hola","*>30s"))   # Coloca la palabra Hola a la derecha yal principio los 30 asteriscos

print(format(2554,"6"))     # Coloca el número a la derecha  precedido por 6 espacios en blanco

print(format(12343,"0=+8"))     # Coloca signo +, completa con ceros más los digitos de la cifra numérica

print(format(-12343,"+10"))   # Coloca signo -, completa con ceros adelante más los digitos de la cifra numérica 
 
print(format(12343,"*<10"))  #Coloca primero el número  y completa los diez caracteres con asterisco

print(format(11,"b"))   # Convierte el número en binario

print(format(0x1232,"d")) # convierte de hexadecimal en decimal
"""
print(format(1223,"o")) #Convierte de decimal a octal

print(format(1223,"x")) #Convierte de decimal a hexadecimal

print(format(139892,".2e")) #Convierte un numero en notacion con exponente e minúsculas

print(format(139892,".2E")) #Convierte un numero en notacion con exponente  E mayúscula
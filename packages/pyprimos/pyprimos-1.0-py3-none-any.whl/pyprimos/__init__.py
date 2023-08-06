# Importa el paquete que permite la integración de Python con R
import rpy2.robjects as ro

# Se crea la función en R y se le asigna a una variable de python
# Se utiliza el paquete matlab instalado en R que contiene la función isprime()
# Que calcula si el número es o no primo y devuelve true o false
codigoPrimos = """ 
library(matlab)
primos <- function(n){
    for (i in 1:n){
        if(as.logical(isprime(i))){
            print(paste("El siguiente numero es primo: ", i))
        }
    }
}
"""

# Se identifica el anterior código como código R y se ejecuta
ro.r(codigoPrimos)
primosPy = ro.globalenv['primos']
primosPy(input("Introduzca un número: "))
def calcularPrimo(n):
    n = int(input ("Vamos a calcular los números primos entre el 1 y el número que indique:\n"))
    contador = 0
    for i in range(2, n):
        for k in range(2, i):
            if i % k == 0:
                contador += 1
        if contador == 0:
            print(i, end=" ")
        contador = 0

def cuantos_primos(n):
    #Variables de la funcion 'cuantos_primos'
    # Lista que se devolvera al usuario con los numeros primos encontrados en el intervalo
    resultado = []

    # El comienzo del intervalo es 1 siempre
    inicial = 1
    # El final del intervalo es n, valor que facilita el usuario
    final = n

    # Bucle que recorre el intervalo desde 1 hasta el numero facilitado por el usuario + 1
    for i in range(inicial, final+1):
        # Variable que controla si el numero es primo
        es_primo = True
        # Bucle que recorrera todos los valores existentes desde el 1 hasta el numero que estamos recorriendo
        for k in range(2, i):
            if i % k == 0:
                es_primo = False
                break
        # Si el numero es primo y no es 1, ya que el numero 1 no es compuesto ni primo, se anade a la lista resultado
        if es_primo and i != 1:
            resultado.append(i)
    return resultado
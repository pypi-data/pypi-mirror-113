def esPrimo(n):
    for j in range(1, n):
        es_primo = True
        if(n%j == 0):
        	es_primo = False
        if(es_primo):
        	print(f"{j} es primo")
    
num = int(input('Ingrese un numero: '))
result = esPrimo(num)
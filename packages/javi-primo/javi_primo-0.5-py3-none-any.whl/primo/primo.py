from rpy2.robjects import r

def numero_primo(a):
    resultado = 1
    for i in range(1, a+1):
        if i%2 == 0:
            r("print(f'Es divisible por: 2')")
        elif i%3 == 0:
            r("print(f'Es divisible por: 3')")
        elif i%5 == 0:
            r("print(f'Es divisible por: 5')")
        elif i%7 == 0:
            r("print(f'Es divisible por: 7')")
        elif i%2 != 0: 
            r("print(f'Tu número es primo')")
        elif i%3 != 0:
            r("print(f'Tu número es primo')")
        elif i%5 != 0:
            r("print(f'Tu número es primo')")
        elif i%7 != 0:
            r("print(f'Tu número es primo')")

    
#print(numero_primo(23))

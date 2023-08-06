def es_primo(num):
    for n in range(2, num):
        if num % n == 0:
            print("No es primo", n, "es divisor de", num)
            return False
    print(num, "es primo")
    return True  
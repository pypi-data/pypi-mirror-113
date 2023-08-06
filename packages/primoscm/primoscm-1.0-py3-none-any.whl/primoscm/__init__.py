def primos(n):

    primos = [1]

    for i in range(2, n + 1):
        primo = True
        for j in range(2,i):
            if (i%j == 0):
                primo = False
        if (primo): primos.append(i)

    return(primos)
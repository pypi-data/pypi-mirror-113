def numprim(num):
    for i in range(2, num+1):
        primo = True
        for j in range(2, i):
            if i % j == 0 :
                primo = False 
        if primo:
            print(i,"es primo")
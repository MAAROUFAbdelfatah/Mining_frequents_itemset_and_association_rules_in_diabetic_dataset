
def support(transactions):
    
    support = {}
    
    for tranction in transactions:
        for item in tranction:
            if item in list(support.keys()):
                support[item] += 1
            else:
                support[item] = 1
    
    return support

def mis_values_ls(frequency, LS, beta):
    
    mis_values = {}

    for value in frequency.keys():
        #𝑀𝐼𝑆(𝑖𝑗) = 𝑚𝑎𝑥𝑖𝑛𝑢𝑚(𝛽𝑓(𝑖𝑗), 𝐿𝑆)
            mis_values[value] =round(max(beta * frequency[value], LS), 0)

    return mis_values

def mis_values_lms(frequency, SD, LMS, LMIS):
    
    mis_values = {}

    for value in frequency.keys():
        S = frequency[value]/614
        M = S - SD

        if M > LMS:
            mis_values[value] =round(M, 0)
        elif M < LMS and S > LMS:
            mis_values[value] = round(LMS, 0)
        else:
            mis_values[value] = round(LMIS, 0)
    return mis_values


"""tran = [['a', 'c', 'd', 'f'],
        ['a', 'c', 'e', 'f', 'g'],
        ['a', 'b', 'c', 'f', 'h'],
        ['b', 'f', 'g'],
        ['b', 'c']
]

f = support(tran)
mis = mis_values_ls(f, 2, 0.7)

imis = mis_values_lms(f, 0.1, 3, 2)

print("--------- SUPPORT-----------")
print(f)
print("############# CFP-Growth #################")
print(mis)
print('################# ICFP-Growth ################')
print(imis)"""
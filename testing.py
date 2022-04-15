import pandas as pd
data = pd.read_csv('diabetes-classification/InterventionSupport.csv')
#pr = list(data.Pregnancies)
#gl = list(data.Glucose)

#l =len(gl)
#dataset = []
#for i in range(l):
#  dataset.append([gl[i], pr[i]])

print(data)


def in_tuple(tuple1, tuple2):
    list1 = list(tuple1)
    list2 = list(tuple2)
    if list1 == list2:
        return True
    else:
        l1 = len(list1)
        l2 = len(list2)
        if l1 > l2:
            list1, list2 = list2, list1
            l1, l2 = l2, l1
        list1.sort()
        list2.sort()
        for i in range(l1, l2):
            if list1 == list2[0:i]:
                return True
    return False   
    

#print(in_tuple(('A2', 'B2', 'BMI1'), ('B2', 'A2')))
#('B2', 'A2', 'BMI1')



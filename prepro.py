import pandas as pd
import pyfpgrowth as fp
data = pd.read_csv('diabetes-classification/train.csv')
test_data = pd.read_csv('diabetes-classification/test.csv')
print(data)

features = list(data.columns)
ItemsData = []
for feature in features:
    if feature == "Pregnancies":
        featureData = list(data.Pregnancies)
        Pregnancies = []
        for item in featureData:
            if item <= 7:
                Pregnancies.append('P1')
            else:
                Pregnancies.append('P2')
    elif feature == "Glucose":
        
        featureData = list(data.Glucose)
        Glucose = []
        
        for item in featureData:
            
            if item <= 125:
                Glucose.append('G1')
            else:
                Glucose.append('G2')
        
    elif feature == "BloodPressure":
        print("1")
        featureData = list(data.BloodPressure)
        BloodPressure = []
        i=0
        for item in featureData:
            i += 1
            if item <= 40:
                BloodPressure.append('B1')
            elif item > 40 and item <= 90:
                BloodPressure.append('B2')
            else:
                BloodPressure.append('B3')
        print(i)
    elif feature == "SkinThickness":
        featureData = list(data.SkinThickness)
        SkinThickness = []
        for item in featureData:
            if item <= 8:
                SkinThickness.append('S1')
            elif item >8 and item <= 45:
                SkinThickness.append('S2')
            else:
                SkinThickness.append('S3')
        
    elif feature == "Insulin":
        featureData = list(data.Insulin)
        Insulin = []
        for item in featureData:
            if item <= 30:
                Insulin.append('I1')
            elif item >30 and item <= 150:
                Insulin.append('I2')
            else:
                Insulin.append('I3')
        
    elif feature == "BMI":
        featureData = list(data.BMI)
        BMI = []
        for item in featureData:
            if item <= 30:
                BMI.append('BMI1')
            else:
                BMI.append('BMI2')
        
    elif feature == "DiabetesPedigreeFunction":
        featureData = list(data.DiabetesPedigreeFunction)
        DiabetesPedigreeFunction = []
        for item in featureData:
            if item <= .8:
                DiabetesPedigreeFunction.append('D1')
            else:
                DiabetesPedigreeFunction.append('D2')
        
    elif feature == "Age":
        featureData = list(data.Age)
        Age = []
        for item in featureData:
            if item <= 30:
                Age.append('A1')
            else:
                Age.append('A2')
    else:
        featureData = list(data.Outcome)
        Outcome =[]
        for item in featureData:
            if item == 0:
                Outcome.append('0')
            else:
                Outcome.append('1')


for j in range(614):
    transaction = [Pregnancies[j], Glucose[j], BloodPressure[j], SkinThickness[j], Insulin[j], BMI[j], DiabetesPedigreeFunction[j], Age[j], Outcome[j]]
    ItemsData.append(transaction)



print(ItemsData)
print(len(ItemsData))
print(len(ItemsData[0]))

patterns = fp.find_frequent_patterns(ItemsData, 0)

asso_roles =  fp.generate_association_rules(patterns, 0)
roles_file = open("rolesFile.txt", "w")
new_asso_roles = {}
for key in asso_roles.keys():
    if asso_roles[key][0] in [('1', ), ('0', )]:
        roles_file.write(str(key)+"==>"+str(asso_roles[key]))
        roles_file.write("\n")
        new_asso_roles[key] = asso_roles[key]
roles_file.close()

print(new_asso_roles)

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

def classification(test ,new_asso_roles):
    result = {}
    for key in new_asso_roles.keys():
        if in_tuple(key, test):
            result[key] = new_asso_roles[key]
    return result 



features = list(test_data.columns)
ItemsData = []
for feature in features:
    if feature == "Pregnancies":
        featureData = list(test_data.Pregnancies)
        Pregnancies = []
        for item in featureData:
            if item <= 7:
                Pregnancies.append('P1')
            else:
                Pregnancies.append('P2')
    elif feature == "Glucose":
        
        featureData = list(test_data.Glucose)
        Glucose = []
        
        for item in featureData:
            
            if item <= 125:
                Glucose.append('G1')
            else:
                Glucose.append('G2')
        
    elif feature == "BloodPressure":
        featureData = list(test_data.BloodPressure)
        BloodPressure = []
        for item in featureData:
            if item <= 40:
                BloodPressure.append('B1')
            elif item > 40 and item <= 90:
                BloodPressure.append('B2')
            else:
                BloodPressure.append('B3')
    elif feature == "SkinThickness":
        featureData = list(test_data.SkinThickness)
        SkinThickness = []
        for item in featureData:
            if item <= 8:
                SkinThickness.append('S1')
            elif item >8 and item <= 45:
                SkinThickness.append('S2')
            else:
                SkinThickness.append('S3')
        
    elif feature == "Insulin":
        featureData = list(test_data.Insulin)
        Insulin = []
        for item in featureData:
            if item <= 30:
                Insulin.append('I1')
            elif item >30 and item <= 150:
                Insulin.append('I2')
            else:
                Insulin.append('I3')
        
    elif feature == "BMI":
        featureData = list(test_data.BMI)
        BMI = []
        for item in featureData:
            if item <= 30:
                BMI.append('BMI1')
            else:
                BMI.append('BMI2')
        
    elif feature == "DiabetesPedigreeFunction":
        featureData = list(test_data.DiabetesPedigreeFunction)
        DiabetesPedigreeFunction = []
        for item in featureData:
            if item <= .8:
                DiabetesPedigreeFunction.append('D1')
            else:
                DiabetesPedigreeFunction.append('D2')
        
    elif feature == "Age":
        featureData = list(test_data.Age)
        Age = []
        for item in featureData:
            if item <= 30:
                Age.append('A1')
            else:
                Age.append('A2')

for j in range(154):
    transaction = [Pregnancies[j], Glucose[j], BloodPressure[j], SkinThickness[j], Insulin[j], BMI[j], DiabetesPedigreeFunction[j], Age[j]]
    ItemsData.append(transaction)

    print(ItemsData[0])

roles_file_test = open("rolesFileTest.txt", "w")
for items in ItemsData:
    ones = 0
    zeros = 0
    r = classification(tuple(items), new_asso_roles)
    for key in r.keys():
        if r[key][0][0] == '1':
            ones += 1
        elif r[key][0][0] == '0':
            zeros += 1
    if zeros > ones:
        print(0)
        result = 0
    elif ones > zeros:
        result = 1
    else:
        print(1)
        result = None

    roles_file_test.write(str(result))
    roles_file_test.write("\n")
roles_file_test.close()

print(classification(('P1', 'G1', 'B2', 'S2', 'I2', 'BMI2', 'D1', 'A1'), new_asso_roles))
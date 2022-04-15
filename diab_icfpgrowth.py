import icfpgrowth as icfp
import pandas as pd
import misGenerater as mis
import time as t

data = pd.read_csv('diabetes-classification/train.csv')
test_data = pd.read_csv('diabetes-classification/test.csv')


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
        featureData = list(data.BloodPressure)
        BloodPressure = []
        for item in featureData:
            if item <= 40:
                BloodPressure.append('B1')
            elif item > 40 and item <= 90:
                BloodPressure.append('B2')
            else:
                BloodPressure.append('B3')
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

start = t.time()
patterns = icfp.generate_items_sets(ItemsData, mis.mis_values_lms(mis.support(ItemsData), 0.1, 50, 40))
#print(mis.mis_values_lms(mis.support(ItemsData),0.1, 50, 40))
asso_roles =  icfp.generate_association_rules(patterns, 0)
end = t.time()
roles_file = open("icfpgrowth_asso_rules.txt", "w")
new_asso_roles = {}
for key in asso_roles.keys():
    if asso_roles[key][0] in [('1', ), ('0', )]:
        roles_file.write(str(key)+"==>"+str(asso_roles[key]))
        roles_file.write("\n")
        new_asso_roles[key] = asso_roles[key]
roles_file.close()
print(end-start)
#print(new_asso_roles)
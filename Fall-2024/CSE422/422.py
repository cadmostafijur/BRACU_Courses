# data manipulation and visualization(6)
import numpy as np
import pandas as pd
import missingno as msno
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import seaborn as sns

# Machine learning models(5)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,VotingClassifier

# Libraries for evaluation and model selection
from sklearn.metrics import *
from sklearn.model_selection import *

# Library for handling imbalanced datasets
from imblearn.over_sampling import SMOTE


from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/CSE422_Project_Dataset/dataset.csv')

print(df.shape)

df.head(5)

df.info()

df.count()

# null values in the dataset
print("Null values per column:")
print(df.isnull().sum())

# color=#611f70
# color=#611f70
#f0bbfc
#27092e
#6982b3
color_majority= '#dbb5ff'

color = [color_majority, color_majority, color_majority, color_majority, color_majority, color_majority, color_majority, color_majority, color_majority, color_majority,'#b164fa','#850afa']
fig, axis  = plt.subplots(figsize=(10, 2), dpi=80)
fig.patch.set_facecolor('#ffffff')#fig bg
axis.set_facecolor('#ffffff')# axis bg
#check bar plot missing valu in dataframe(here use missingno as msno)
msno.bar(df, sort='descending',
         color=color,
         ax=axis, fontsize=8,
         labels='off',
         filter='top')
#label-x axis
axis.set_xticklabels(axis.get_xticklabels(),
                     rotation=90, ha='center',
                     size=10, weight='normal',
                     alpha=1)# get_xticklabels current lable
                     #alpa opcaity labe
axis.set_yticklabels('')# y label not necss
axis.spines['bottom'].set_visible(True)
plt.show()

category_cols = df.select_dtypes(include=['object'])

for col in category_cols:
    unique_categories = len(df[col].unique())
    color_palette = sns.color_palette("rocket", unique_categories)
    plt.figure(figsize=(5, 4))
    sns.countplot(
        data=df,
        x=col,
        order=df[col].value_counts().index,
        palette=color_palette
    )

    plt.xlabel(col)
    plt.ylabel('Count')
    plt.show()

df["work_type"].value_counts()
df["gender"].value_counts()
df["gender"]=df["gender"].map({"Male":1,"Female":0})
df.count()
df["gender"].mean()

df["gender"]=df["gender"].fillna(df["gender"].mean())

df.count()
df["ever_married"]=df["ever_married"].map({"Yes":1,"No":0})

df.count()

df["bmi"]=df["bmi"].fillna(df["bmi"].mean())

df = pd.get_dummies(df,columns=["work_type"])

df["Residence_type"]=df["Residence_type"].map({"Urban":1,"Rural":0})
df = pd.get_dummies(df,columns=["smoking_status"])
df.count()
df=df.drop(["id"],axis=1)
correlation=df.corr()
fig, ax = plt.subplots(figsize=(8,8))
sns.heatmap(correlation,cmap='viridis')
plt.show()

y=df["stroke"]
X=df.drop(["stroke"],axis=1)


model1=LogisticRegression(solver="liblinear")
cross_val_score(model1,X,y,cv=10).mean()

model2=DecisionTreeClassifier()
cross_val_score(model2,X,y,cv=10).mean()
model3=RandomForestClassifier()
cross_val_score(model3,X,y,cv=10).mean()

model4=GradientBoostingClassifier()
cross_val_score(model4,X,y,cv=10).mean()
model5=KNeighborsClassifier()
cross_val_score(model5,X,y,cv=10).mean()
model6 = VotingClassifier(estimators = [("lr",model1),("dtf",model2),("rf",model3),("gb",model4),("knn",model5),],voting="soft")
cross_val_score(model6,X,y,cv=10).mean()
y=df["stroke"]
X=df.drop(["stroke"],axis=1)
# split data
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=1)

#SMOTE
smote=SMOTE()
X_train,y_train=smote.fit_resample(X_train,y_train)
num_stroke_before = y.sum()
num_stroke_after = y_train.sum()

plt.bar(['Before', 'After'], [num_stroke_before, num_stroke_after])
plt.title('Number of Stroke Cases Before and After Oversampling')
plt.xlabel('Oversampling')
plt.ylabel('Number of Stroke Cases')
plt.show()
model_1=LogisticRegression(solver='liblinear')
model_1.fit(X_train,y_train)
y_hat=model_1.predict(X_test)
acc_val = accuracy_score(y_test,y_hat)

print('Logistic Regression :',acc_val*100,"%")
print(classification_report(y_test,y_hat))
RocCurveDisplay.from_estimator(model_1,X_test,y_test)
# DecisionTree
model_5= DecisionTreeClassifier()
model_5.fit(X_train,y_train)
y_hat=model_5.predict(X_test)
# print(X_test)
acc_val = accuracy_score(y_test,y_hat)

print('DecisionTree :',acc_val*100,"%")
print(classification_report(y_test,y_hat))
RocCurveDisplay.from_estimator(model_5,X_test,y_test)

model_3= KNeighborsClassifier(n_neighbors = 5)
model_3.fit(X_train,y_train)
y_hat=model_3.predict(X_test)
acc_val = accuracy_score(y_test,y_hat)

print('KNN :',acc_val*100,"%")
print(classification_report(y_test,y_hat))
RocCurveDisplay.from_estimator(model_3,X_test,y_test)
# RandomForestClassifier
model_4= RandomForestClassifier()
model_4.fit(X_train,y_train)
y_hat=model_4.predict(X_test)
acc_val = accuracy_score(y_test,y_hat)

print('RandomForestClassifier:',acc_val*100,"%")
print(classification_report(y_test,y_hat))
RocCurveDisplay.from_estimator(model_4,X_test,y_test)

model_2= GradientBoostingClassifier()
model_2.fit(X_train,y_train)
y_hat=model_2.predict(X_test)
acc_val = accuracy_score(y_test,y_hat)

print('GradientBoosting :',acc_val*100,"%")
print(classification_report(y_test,y_hat))
RocCurveDisplay.from_estimator(model_2,X_test,y_test)
models = {
    "Logistic Regression": 89.68509984639017,
    "K-Nearest Neighbors": 86.52073732718894,
    "Decision Tree": 95.67588325652842,
    "Random Forest": 97.74193548387096,

}

name = list(models.keys())
accu = list(models.values())

error = []
for i in list(models.values()):
  error.append(100-i)


err = [100 - i for i in accu]

for model, accuracy, err in zip(name, accu, error):
    print(f"Model: {model}, Accuracy: {accuracy:.2f}%, Error: {err:.2f}%")

plt.bar(name, accu, label='Accuracy', color='#9b89f5', width = 0.4)
plt.xlabel('Model')
plt.ylabel('Percentage')
plt.title('Model Accuracy')
plt.xticks(rotation=90)
plt.legend()
plt.show()

plt.bar(name, error , label='Error', color='#cf0c0c')
plt.xlabel('Model')
plt.ylabel('Percentage')
plt.title('Error')
plt.xticks(rotation=90)
plt.legend()
plt.show()
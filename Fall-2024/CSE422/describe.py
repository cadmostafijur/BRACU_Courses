# Import essential libraries for data manipulation, visualization, and machine learning
import numpy as np  # For numerical operations
import pandas as pd  # Data manipulation
import missingno as msno  # Visualization of missing data
import matplotlib  # Basic plotting library
import matplotlib.pyplot as plt  # Detailed plotting functions
import seaborn as sns  # Advanced statistical plotting

# Import machine learning algorithms and tools
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import *  # All performance metrics
from sklearn.model_selection import *  # Model selection and validation tools
from imblearn.over_sampling import SMOTE  # Handles imbalanced datasets by oversampling

# Integration with Google Colab for accessing files on Google Drive
from google.colab import drive
drive.mount('/content/drive')  # Mount Google Drive

# Loading the dataset from a specified path
df = pd.read_csv('/content/drive/MyDrive/CSE422_Project_Dataset/dataset.csv')

# Display the shape of the DataFrame
print(df.shape)

# Display the first five rows of the DataFrame
df.head(5)

# Print detailed information about the DataFrame
df.info()

# Count non-null entries for each column
df.count()

# Print the number of null values per column
print("Null values per column:")
print(df.isnull().sum())
# Custom color setup for missing data visualization
color_majority= '#dbb5ff'
color = [color_majority] * 10 + ['#b164fa','#850afa']

# Setup plot for visualizing missing data
fig, axis = plt.subplots(figsize=(10, 2), dpi=80)
fig.patch.set_facecolor('#ffffff')  # Background color for the figure
axis.set_facecolor('#ffffff')  # Background color for the axis

# Generate a bar plot for missing values using the missingno library
msno.bar(df, sort='descending', color=color, ax=axis, fontsize=8, labels='off')

# Adjusting the labels and ticks for better readability
axis.set_xticklabels(axis.get_xticklabels(), rotation=90, ha='center', size=10, weight='normal', alpha=1)
axis.set_yticklabels('')
axis.spines['bottom'].set_visible(True)  # Ensure the bottom spine is visible
plt.show()
# Identify categorical columns and visualize counts for each category
category_cols = df.select_dtypes(include=['object'])  # Select columns that are of type 'object', typical for categorical data

# Loop through each categorical column and create a count plot
for col in category_cols:
    unique_categories = len(df[col].unique())  # Count unique values in the column
    color_palette = sns.color_palette("rocket", unique_categories)  # Generate a color palette
    plt.figure(figsize=(5, 4))  # Set the figure size
    sns.countplot(data=df, x=col, order=df[col].value_counts().index, palette=color_palette)
    plt.xlabel(col)  # Set the x-axis label to the column name
    plt.ylabel('Count')  # Set the y-axis label
    plt.show()

# Convert categorical data to numerical data
df["gender"] = df["gender"].map({"Male": 1, "Female": 0})  # Map 'Male' to 1 and 'Female' to 0

# Fill missing values with the mean of the column
df["gender"] = df["gender"].fillna(df["gender"].mean())

# Map categorical 'ever_married' to numerical
df["ever_married"] = df["ever_married"].map({"Yes": 1, "No": 0})

# Fill 'bmi' missing values with the column's mean
df["bmi"] = df["bmi"].fillna(df["bmi"].mean())

# One-hot encode 'work_type'
df = pd.get_dummies(df, columns=["work_type"])

# Map 'Residence_type' and create dummies for 'smoking_status'
df["Residence_type"] = df["Residence_type"].map({"Urban": 1, "Rural": 0})
df = pd.get_dummies(df, columns=["smoking_status"])

# Drop the 'id' column as it is not useful for modeling
df = df.drop(["id"], axis=1)

# Visualize the correlation matrix
correlation = df.corr()  # Compute correlation matrix
fig, ax = plt.subplots(figsize=(8,8))  # Set size of the figure
sns.heatmap(correlation, cmap='viridis')  # Create a heatmap of the correlations
plt.show()
# Prepare data for modeling
y = df["stroke"]  # Define the target variable
X = df.drop(["stroke"], axis=1)  # Drop the target variable from the dataset to create the feature set

# Initialize various classifiers
model1 = LogisticRegression(solver="liblinear")
model2 = DecisionTreeClassifier()
model3 = RandomForestClassifier()
model4 = GradientBoostingClassifier()
model5 = KNeighborsClassifier()
model6 = VotingClassifier(estimators=[("lr", model1), ("dt", model2), ("rf", model3), ("gb", model4), ("knn", model5)], voting="soft")

# Evaluate models using cross-validation
cross_val_score(model1, X, y, cv=10).mean()
cross_val_score(model2, X, y, cv=10).mean()
cross_val_score(model3, X, y, cv=10).mean()
cross_val_score(model4, X, y, cv=10).mean()
cross_val_score(model5, X, y, cv=10).mean()
cross_val_score(model6, X, y, cv=10).mean()

# Data splitting for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Apply SMOTE for handling class imbalance
smote = SMOTE()
X_train, y_train = smote.fit_resample(X_train, y_train)

# Visualize the number of stroke cases before and after SMOTE
num_stroke_before = y.sum()
num_stroke_after = y_train.sum()
plt.bar(['Before', 'After'], [num_stroke_before, num_stroke_after])
plt.title('Number of Stroke Cases Before and After Oversampling')
plt.xlabel('Oversampling')
plt.ylabel('Number of Stroke Cases')
plt.show()

# Train and evaluate Logistic Regression
model_1.fit(X_train, y_train)
y_hat = model_1.predict(X_test)
acc_val = accuracy_score(y_test, y_hat)
print('Logistic Regression :', acc_val * 100, "%")
print(classification_report(y_test, y_hat))
RocCurveDisplay.from_estimator(model_1, X_test, y_test)

# Train and evaluate Decision Tree
model_5.fit(X_train, y_train)
y_hat = model_5.predict(X_test)
acc_val = accuracy_score(y_test, y_hat)
print('DecisionTree :', acc_val * 100, "%")
print(classification_report(y_test, y_hat))
RocCurveDisplay.from_estimator(model_5, X_test, y_test)

# Train and evaluate KNN
model_3.fit(X_train, y_train)
y_hat = model_3.predict(X_test)
acc_val = accuracy_score(y_test, y_hat)
print('KNN :', acc_val * 100, "%")
print(classification_report(y_test, y_hat))
RocCurveDisplay.from_estimator(model_3, X_test, y_test)

# Train and evaluate Random Forest
model_4.fit(X_train, y_train)
y_hat = model_4.predict(X_test)
acc_val = accuracy_score(y_test, y_hat)
print('RandomForestClassifier:', acc_val * 100, "%")
print(classification_report(y_test, y_hat))
RocCurveDisplay.from_estimator(model_4, X_test, y_test)

# Train and evaluate Gradient Boosting
model_2.fit(X_train, y_train)
y_hat = model_2.predict(X_test)
acc_val = accuracy_score(y_test, y_hat)
print('GradientBoosting :', acc_val * 100, "%")
print(classification_report(y_test, y_hat))
RocCurveDisplay.from_estimator(model_2, X_test, y_test)

# Comparing models
models = {
    "Logistic Regression": 89.68509984639017,
    "K-Nearest Neighbors": 86.52073732718894,
    "Decision Tree": 95.67588325652842,
    "Random Forest": 97.74193548387096,
}
name = list(models.keys())
accu = list(models.values())
error = [100 - i for i in accu]

# Visualizing model performance
for model, accuracy, err in zip(name, accu, error):
    print(f"Model: {model}, Accuracy: {accuracy:.2f}%, Error: {err:.2f}%")
plt.bar(name, accu, label='Accuracy', color='#9b89f5', width=0.4)
plt.xlabel('Model')
plt.ylabel('Percentage')
plt.title('Model Accuracy')
plt.xticks(rotation=90)


# Binary encoding is compact but still imposes 
# an ordinal relationship between categories.
# Target Encoding (Mean Encoding):
# Replaces categories with the mean of the target variable for each category.
# Why not here? It introduces information from the target variable,
#  which can lead to data leakage if not handled carefully.

# One-hot encoding is the best choice when:

# The number of categories is not too large
#  (avoiding high-dimensionality issues).
# There is no natural order among the categories.
# You want to ensure no relationships between the 
# categories are unintentionally introduced.

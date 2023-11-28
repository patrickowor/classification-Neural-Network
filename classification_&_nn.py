# -*- coding: utf-8 -*-
"""Classification & NN.ipynb

Automatically generated by Colaboratory.

"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# %matplotlib inline

# reading the dataset into memory
df = pd.read_csv('https://canvas.wlv.ac.uk/courses/41905/files/6902583/download?download_frd=1&verifier=UcopI6blzAfWBl4Fz9MMdR88ZBd8zqdTQge3CR19')
df.head()

# getting sum of empty rows in dataset

print(df.isna().sum())

# filling NaN with the mean of the column
df['3 Point Percent'] = df['3 Point Percent'].fillna(df['3 Point Percent'].mean())

# confirming change made
df.isna().sum()

# checking for duplicate rows
# df[df.duplicated()]

# getting the info of the dataset

df.info()

# getting a description on the dataset
df.describe()

# plotting heat map to se relationship betweeen each column and our target label
import seaborn as sns
plt.figure(figsize=(12, 6))
sns.heatmap(df.corr(),
            cmap = 'BrBG',
            fmt = '.2f',
            linewidths = 2,
            annot = True)

# dropping features with the least relationship to the dataset
df2 = df.drop([  '3 Point Percent', '3 Point Made', '3 Point Attempt', 'Name'], axis=1)

X = df2.drop(['TARGET_5Yrs'], axis=1)
y = df2['TARGET_5Yrs']

X.head()

y.head()

#splitting data to training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import GaussianNB

# trying logistic model with multiple parameters to get the best and varied results
model_list = [
    ('LogisticRegression',LogisticRegression() ),
    ('LogisticRegression max_iter=1000',LogisticRegression(max_iter=1000) ),
    ('LogisticRegression solver=LIBLINEAR',LogisticRegression( solver='LIBLINEAR'.lower() ) ),
    ('LogisticRegression solver=LIBLINEAR max_iter=1000',LogisticRegression( solver='LIBLINEAR'.lower(), max_iter=1000) ),
    ('LogisticRegression solver=SAGA',LogisticRegression( solver='SAGA'.lower() )),
    ('LogisticRegression solver=SAGA max_iter=1000',LogisticRegression( solver='SAGA'.lower(), max_iter=1000) ),
]
models = []
accuracies = []

for model_name, model in model_list:
  # creating a Logistic Regression model
  logistic_model = model

  # fitting the model on the training data
  logistic_model.fit(X_train, y_train)

  # trying predictions on the testing data
  logistic_predictions = logistic_model.predict(X_test)

  # evaluating the models performance
  print(f"{model_name}-> Logistic Regression Performance:")
  print(classification_report(y_test, logistic_predictions))
  print("Accuracy:", accuracy_score(y_test, logistic_predictions))
  models.append(model_name)
  accuracies.append(accuracy_score(y_test, logistic_predictions))
  print("\n\n")

# creating a Gaussian Naive Bayes model
naive_bayes_model = GaussianNB()

# fitting the model on the training data
naive_bayes_model.fit(X_train, y_train)

# making predictions on the testing data
naive_bayes_predictions = naive_bayes_model.predict(X_test)

# evaluating the model's performance
print("Gaussian Naive Bayes Performance:")
print(classification_report(y_test, naive_bayes_predictions))
print("Accuracy:", accuracy_score(y_test, naive_bayes_predictions))
models.append("Gaussian Naive Bayes")
accuracies.append(accuracy_score(y_test, naive_bayes_predictions))

# the Neural Network model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

epochs=12
batch_size=32

# creating a neural network model
nn_model = Sequential()
nn_model.add(Dense(units=64, activation='relu', input_dim=X_train.shape[1]))
nn_model.add(Dense(units=1, activation='sigmoid'))

# compiling the model the model
nn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# fitting the model
nn_model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test))

# Evaluate the model's performance
nn_loss, nn_accuracy = nn_model.evaluate(X_test, y_test)
print(f"Neural Network Performance: Accuracy = {nn_accuracy}")
models.append("Neural Network Performance")
accuracies.append(nn_accuracy)

import matplotlib.pyplot as plt
import numpy as np


plt.figure(figsize=(10, 6))
plt.bar(models, accuracies, color=['blue', 'green', 'orange'])
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison of Different Models')
plt.ylim([0, 1])  # Set the y-axis limit to match accuracy range (0 to 1)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')
plt.show()
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

data = pd.read_csv('Final.csv')
y = data['y']
X = data.drop(['Ticker', 'y', 'Filing Date'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

kernels = ['linear', 'poly', 'rbf', 'sigmoid']

for kernel in kernels:
    svm_classifier = SVC(kernel=kernel, decision_function_shape='ovr')

    svm_classifier.fit(X_train, y_train)

    y_pred = svm_classifier.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy with {kernel} kernel: {accuracy * 100:.2f}%')

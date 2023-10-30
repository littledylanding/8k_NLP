from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

df = pd.read_csv("filtered_data.csv")
y_col = [x for x in df.columns if 'LSM' not in x]
y_col.remove('Ticker')
y_col.remove('Filing Date')
x_col = [x for x in df.columns if 'LSM' in x]
y = df[y_col]
X = df[x_col]
y = y.loc[:, (y.sum() != 0)]
X = X.loc[:, (X.sum() != 0)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=19)

rf = RandomForestClassifier(n_estimators=1000)

multi_target_rf = MultiOutputClassifier(rf, n_jobs=-1)

multi_target_rf.fit(X_train, y_train)

y_pred = multi_target_rf.predict(X_test)
for i, col in enumerate(y.columns):
    print(f"Classification Report for {col}:\n")
    print(classification_report(y_test.iloc[:, i], y_pred[:, i]))
    print("\n")

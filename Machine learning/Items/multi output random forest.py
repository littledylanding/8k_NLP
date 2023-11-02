from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd


def drop_first_last(group):
    return group.iloc[1:-1]


df = pd.read_csv("Data.csv")
df = df.sort_values(by=['Ticker'])
result = df.groupby(['Ticker']).apply(drop_first_last)
df = result.reset_index(drop=True)
x_col = list(df.columns)
err = ['Ticker', 'Market', 'y', 'Ret', 'Items']
for i in err:
    x_col.remove(i)
y = df['y']
X = df[x_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=19)

rf = RandomForestClassifier(n_estimators=1000, random_state=19)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

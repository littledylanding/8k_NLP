from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

df = pd.read_excel("C:\\Users\\jiaqi\\Desktop\\8k_NLP\\FilingData.xlsx")
all_items = sorted(df['Section'].str.split(', ', expand=True).stack().unique())
for item in all_items:
    df[item] = df['Section'].str.contains(item, na=False).astype(int)
df.sort_values(by=['Ticker', 'Filing Date'], inplace=True)
feature_cols = df.columns.difference(['Ticker', 'Filing Date', 'Section'])

X = pd.DataFrame()
y = pd.DataFrame()

for ticker in df['Ticker'].unique():
    company_data = df.loc[df['Ticker'] == ticker, feature_cols]

    if len(company_data) > 2:
        lag1 = company_data.iloc[:-2].reset_index(drop=True)
        lag2 = company_data.iloc[1:-1].reset_index(drop=True)

        combined_lags = pd.concat([lag1, lag2], axis=1, ignore_index=True)

        X = pd.concat([X, combined_lags], ignore_index=True)

        y = pd.concat([y, company_data.iloc[2:]], ignore_index=True)

new_col_names = [f"{col}_lag1" for col in feature_cols] + [f"{col}_lag2" for col in feature_cols]
X.columns = new_col_names
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

rf = RandomForestClassifier(n_estimators=1000)

multi_target_rf = MultiOutputClassifier(rf, n_jobs=-1)

multi_target_rf.fit(X_train, y_train)

y_pred = multi_target_rf.predict(X_test)
for i, col in enumerate(y.columns):
    print(f"Classification Report for {col}:\n")
    print(classification_report(y_test.iloc[:, i], y_pred[:, i]))
    print("\n")

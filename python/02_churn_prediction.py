import pyodbc
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# 1. CONNECT & FETCH DATA
server = r'LOCAL_SQL_SERVER'
database = 'Wine_Analytics_UK'
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("STEP 1: Fetching Semantic Layer Data...")
df = pd.read_sql("SELECT * FROM dbo.vw_RetentionActionBase", conn)
print(f"STEP 1 COMPLETE: {len(df)} rows fetched")

# 2. FEATURE ENGINEERING
print("STEP 2: Feature engineering...")
df['IsChurned'] = df['Customer_Status'].apply(lambda x: 1 if x == 'Churned' else 0)

df['Avg_CSAT_Score']      = df['Avg_CSAT_Score'].fillna(5.0)
df['Avg_Basket_Size']     = df['Avg_Basket_Size'].fillna(1.0)
df['Total_Tickets_Count'] = df['Total_Tickets_Count'].fillna(0)
df['Frequency_Count']     = df['Frequency_Count'].fillna(0)
df['Total_Net_Profit']    = df['Total_Net_Profit'].fillna(0)
df['Total_Revenue']       = df['Total_Revenue'].fillna(0)

df['CSAT_Risk']          = 5 - df['Avg_CSAT_Score']
df['Has_Complaint']      = (df['Total_Tickets_Count'] > 0).astype(int)
df['Log_Tickets']        = np.log1p(df['Total_Tickets_Count'])
df['Low_Basket_Flag']    = (df['Avg_Basket_Size'] <= 1.5).astype(int)
df['Low_Frequency_Flag'] = (df['Frequency_Count'] <= 2).astype(int)
print("STEP 2 COMPLETE")

# 3. FEATURE LIST
features = [
    'Frequency_Count'
    ,'Low_Frequency_Flag'
    ,'Total_Net_Profit'
    ,'Total_Revenue'
    ,'Avg_Basket_Size'
    ,'Low_Basket_Flag'
    ,'CSAT_Risk'
    ,'Has_Complaint'
    ,'Log_Tickets'
]

X = df[features].fillna(0)
y = df['IsChurned']

# 4. TRAIN THE MODEL
print("STEP 3: Training Churn Propensity Model...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
model.fit(X_scaled, y)
print("STEP 3 COMPLETE")

# 5. PREDICT PROBABILITY
print("STEP 4: Predicting probabilities...")
df['Churn_Probability'] = model.predict_proba(X_scaled)[:, 1]
print("STEP 4 COMPLETE")

# 6. WRITE BACK TO SQL
print("STEP 5: Writing predictions back to SQL Server...")

# Create table once if missing
cursor.execute("""
IF OBJECT_ID('dbo.Fact_Churn_Predictions', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Fact_Churn_Predictions (
        PredictionID      INT PRIMARY KEY IDENTITY(1,1),
        CustomerKey       INT NOT NULL,
        ChurnProbability  DECIMAL(10,4),
        PredictionDate    DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Churn_Customer FOREIGN KEY (CustomerKey) REFERENCES dbo.Dim_Customers(CustomerKey)
    )
END
""")
conn.commit()
print("STEP 5A COMPLETE: Table checked/created")

# Clear old rows instead of DROP/CREATE
cursor.execute("DELETE FROM dbo.Fact_Churn_Predictions")
conn.commit()
print("STEP 5B COMPLETE: Existing predictions cleared")

insert_query = """
INSERT INTO dbo.Fact_Churn_Predictions (CustomerKey, ChurnProbability)
VALUES (?, ?)
"""
data_to_insert = list(df[['CustomerKey', 'Churn_Probability']].itertuples(index=False, name=None))

cursor.fast_executemany = True
cursor.executemany(insert_query, data_to_insert)
conn.commit()
print(f"STEP 5C COMPLETE: {len(data_to_insert)} rows inserted")

print("AI Prediction Complete.")

cursor.close()
conn.close()

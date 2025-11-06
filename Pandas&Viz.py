import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#citim csv.urile
df_event = pd.read_csv('events.csv')
df_marketing = pd.read_csv('marketing_spend.csv')
df_items = pd.read_csv('order_items.csv')
df_order = pd.read_csv('orders.csv')
df_subscrib = pd.read_csv('subscriptions.csv')
df_user = pd.read_csv('users.csv')

#Verificat valori null
#print(df_event.isnull().sum())
#print(df_marketing.isnull().sum())
# print(df_items.isnull().sum())
# print(df_order.isnull().sum())
#print(df_subscrib.isnull().sum())
#print(df_user.isnull().sum())

#Modificam pentru o mai buna manipulare:
df_event['event_time'] = pd.to_datetime(df_event['event_time'])
#print(df_event.dtypes)
df_user['signup_date'] = pd.to_datetime(df_user['signup_date'])
#print(df_user.dtypes)
df_order['order_date'] = pd.to_datetime(df_order['order_date'])
#print(df_order.dtypes)
df_marketing['day'] = pd.to_datetime(df_marketing['day'])
#print(df_marketing.dtypes)

#Curatam duplicate:
df_subscrib['canceled_at'] = df_subscrib['canceled_at'].fillna('Inca nu')
#coloana respectiva reprezinta data 'de dezabonare', valorile null reprezinta ca inca sunt abonati, nu putem sterge randurile cu  non-valori dar le-am facut mai dragute :D
print(df_items.duplicated().sum()) #verificam cate dublicate avem
df_items = df_items.drop_duplicates() #Stergem  duplicate


#Statistici:
q1 = df_order['amount'].quantile(0.25)
q3 = df_order['amount'].quantile(0.75)
IQR = q3 -q1

Statistici = {
    'Count': df_order['amount'].count(),
    'Mean': df_order['amount'].mean(),
    'Median': df_order['amount'].median(),
    'P95': np.percentile(df_order['amount'] , 95),
    'IQR': IQR
}


#Histograma + boxplot pentru 'amount'.


status = df_order.status.value_counts()
print(status)
df_order_real = df_order[~df_order['status'].isin(['cancelled', 'refunded'])]
#print(df_order_real['status'].value_counts())

plt.figure(figsize=(12,5))
#histograma
plt.subplot(1,2,1)
sns.histplot(df_order_real['amount'], bins=30, kde=True)
plt.title('Distributia valorilor amount')
plt.xlabel('Amount')
plt.ylabel('Frecventa')
#boxplot
plt.subplot(1,2,2)
sns.boxplot(x = df_order_real['amount'])
plt.title('Boxplot pentru amount')
plt.tight_layout()
plt.show()
"""
Explicati---
 """
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import seaborn as sns
import math
import os
#Folder unde se afla datele noastre:
DATA = Path("data")

#citim csv.urile
df_event = pd.read_csv(DATA / "events.csv", parse_dates=["event_time"])
df_marketing = pd.read_csv(DATA / "marketing_spend.csv", parse_dates=["day"])
df_items = pd.read_csv(DATA / "order_items.csv")
df_order = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
df_subscrib = pd.read_csv(DATA / "subscriptions.csv", parse_dates=["started_at","canceled_at"])
df_user = pd.read_csv(DATA / "users.csv", parse_dates=["signup_date"])

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
df_order_real = df_order[~df_order['status'].isin(['cancelled', 'refunded'])]
Statistici = {
    'Count': df_order_real['amount'].count(),
    'Mean': df_order_real['amount'].mean(),
    'Median': df_order_real['amount'].median(),
    'P95': np.percentile(df_order_real['amount'] , 95),
    'IQR': IQR
}


#Histograma + boxplot pentru 'amount'.


status = df_order.status.value_counts()
#print(status)

#print(df_order_real['status'].value_counts())
#print('Q3:',q3)
#print('Q1:' ,q1)
#print('Mediana:', df_order_real.amount.median())
plt.figure(figsize=(8, 4))
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
plt.savefig("images/amount_hist_boxplot.png")
plt.show()

#Funnel 14zile:

#Filtram doar ultimele 14 zile
cutoff = df_event['event_time'].max() - pd.Timedelta(days=13)

#Pastram doar evenimentele din ultimele 14 zile
ev = df_event[df_event['event_time'] >= cutoff].copy()

#Definim etapele Funnel-ului
steps = ['view_product', 'add_to_cart', 'checkout', 'purchase']

#Numaram cati utilizatori unici au fost in fiecare pas
steps_counts = {}
for pas in steps: #Filtram doar randurile cu acel eveniment (nunique = numar unic)
    steps_counts[pas] = ev[ev['event_name'] == pas]['user_id'].nunique()

#Calculam conversiile dintre pasi succesivi
conv = {} #salvam ratele de conversie
for i in range(len(steps)-1):
    pas_curent = steps[i]
    pas_urmator = steps[i + 1]

    #Numaram cati useri au ajuns in pasul urmator
    utilizatori_urmator = ev[ev['event_name']== pas_urmator]['user_id'].nunique()

    #Numaram cati useri erau in pasul curent
    utilizatori_curent = ev[ev['event_name']== pas_curent]['user_id'].nunique()

    #Calculam rata = urmator / curent (cu protectie sa nu impartim la 0)
    rata = utilizatori_urmator / utilizatori_curent if utilizatori_curent > 0 else 0

    #Salvam rezultatul:
    conv[f"{pas_curent}_to_{pas_urmator}"] = rata

    #Conversia totala:
    utilizatori_start= ev[ev['event_name']== steps[0]]["user_id"].nunique()
    utilizatori_final= ev[ev['event_name']== steps[-1]]["user_id"].nunique()

    overall = utilizatori_final / utilizatori_start if utilizatori_start > 0 else 0

    #Afisam rezultatele:
    print("Utilizatori unici pe fiecare pas:")
    for k , v in steps_counts.items():
        print(f"{k}: {v}")

    print("\nRate de conversie intre pasi:")
    for k, v in conv.items():
        print(f"{k}: {v:.2%} ")
    print(f"\nConversia totala({steps[0]} -> {steps[-1]}): {overall:.2%}")

steps_order = list(steps_counts.keys())
counts = list(steps_counts.values())

plt.figure(figsize=(8,5))
plt.bar(steps_order, counts, color='skyblue')
plt.title('Funnel 14 zile - utilizatori unici per pas')
plt.ylabel('Număr utilizatori')
plt.xlabel('Etape Funnel')
plt.tight_layout()
plt.savefig("images/funnel.png")
plt.show()
"""
Explicatii---
Avem o distributie asimetrica(skewed)
Boxplot.ul ne areata:
-valoarea minima este 0;
-q1 = 254.6625;
-mediana= circa 500 (498.29);
-q3 = 869.74;
-valoarea maxima este
avem si valori 'outlieri' valori care se abat de la boxplot.ul nostru(comenzi mai mari, fata de tendinta)    
Histograma cu frecventa descendenta deoarece avem o distributie asimetrica spre dreapta
Majoritatea valorilor sunt mici (in jur de 0-1000) si scade treptat pe masura ce 'amount' creste.


Pe scurt:
Aceasta distributie indica faptul ca cele mai multe comenzi au o valoare redusa,
in timp ce un numar mic de comenzi cu valori mari influenteaza media si genereaza prezenta outlierilor.  
"""


#Experiment & Time series:

#Datele experimentului
n_cont = 12400
c_cont = 1116
n_vari = 12100
c_vari = 1210

#Rata de conversie:
p_c = c_cont / n_cont
p_v = c_vari / n_vari

#Lift procentual:
lift = (p_v - p_c)/ p_c * 100

#Rata combinata (pooled) pentru testul z
p_pool = (c_cont + c_vari) / (n_cont + n_vari)

#Standard error:
se = np.sqrt(p_pool * (1 - p_pool) * (1/n_cont + 1/n_vari))

#Scor z
z = (p_v - p_c) / se

#Calcul p-value bilateral:
p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z)/np.sqrt(2))))

print(f"Rata control: {p_c:.4f}")
print(f"Rata varianta: {p_v:4f}")
print(f"Lift: {lift:.2f}%")
print(f"Z-score: {z:.3f}")
print(f"P-value: {p_value:.5f}")

if p_value < 0.05:
    print("Diferenta este semnificativa statistic")
else:
    print("Nu este o diferenta semnificativa")


#Revenue zilnic - Time Series + MA(7) + anomalii

#Filtram comenzile platite:
df_paid = df_order[df_order['status']=='paid'].copy()

#Revenue zilnic:

daily_revenue = df_paid.groupby(df_paid['order_date'].dt.date)['amount'].sum()
daily_revenue = daily_revenue.sort_index() #ordonam dupa zi
print(daily_revenue.head())

ma7 = daily_revenue.rolling(window=7, min_periods=1).mean()

#Z-score
z_score = (daily_revenue - daily_revenue.mean()) / daily_revenue.std()

#Zile cu anomalii |z| > 3
anomalii = daily_revenue[np.abs(z_score) >3]
print("Anomalii:")
print(anomalii)

#Top5 anomalii:
print("Top 5 zile anormale:")
print(anomalii.sort_values(ascending=False).head(5))
top_5_anomalii = anomalii.sort_values(ascending=False).head(5)
#Grafic: revenue zilnic +MA(7) + anomalii
plt.figure(figsize=(12,5))
plt.plot(daily_revenue.index, daily_revenue.values, label='Revenue zilnic')
plt.plot(ma7.index, ma7.values, label='MA(7)', color='Red', linewidth=2)
plt.scatter(anomalii.index, anomalii.values, color='green', label='Anomalie z >3')
plt.title('Revenue zilnic + Media mobilă 7 zile + Anomalii')
plt.xlabel('Zi')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("images/revenue_ma7_anomalies.png")
plt.close()
plt.show()

top_5_anomalii.to_csv("top5_anomalies.csv", header=["revenue"])

#Salvare grafice:
if not os.path.exists("images"):
    os.makedirs("images")

print(df_order_real.shape)
print(df_order_real.head())
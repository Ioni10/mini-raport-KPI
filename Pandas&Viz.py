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
#print(status)
df_order_real = df_order[~df_order['status'].isin(['cancelled', 'refunded'])]
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




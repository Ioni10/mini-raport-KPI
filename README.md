# mini-raport-KPI
Scop : Dintr-un set de CSV-uri e-commerce, construiți cap-coadă un mini-raport cu KPI, analize și vizualizări.

Livrabile

1) SQL
	- Daily Sales (30 zile): `day, orders, revenue` (doar `status='paid'`).
	- Top 5 categorii (90 zile) după venit (join `orders` + `order_items`).
	- Refund rate lunar = `refunded_orders / paid_orders`.
	- ROAS zilnic = join `marketing_spend` + revenue (`paid`).



2) Pandas & Viz :
	- Curățare (dtypes, NaN, duplicate) + scurtă justificare.
	- Statistici `amount`: count/mean/median/p95/IQR + 2–3 rânduri interpretare.
	- Histogramă + boxplot pentru `amount`.
	- Funnel 14 zile (view → add_to_cart → checkout → purchase): rate per pas + overall.

3) Experiment & Time series:
	- A/B test proporții (Control: n=12400, conv=1116; Variantă: n=12100, conv=1210) – rate, lift, z-test, p-value, concluzie.
	- Revenue zilnic: MA(7) + anomalii (|z|>3). Export top 5 + grafic.

4) Raport scurt (max 1 pagină): 4 concluzii cheie .

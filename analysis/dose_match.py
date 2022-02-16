import pandas as pd
import matplotlib.pyplot as plt

af_dose=pd.read_csv("output/measure_doacs_dose_match_rate.csv", usecols=["date", "af_&_crcl", "on_doac", "dose_match", "value"])
af_dose['value'] = 100 - (100 * af_dose['value'])
dose_subset=af_dose.loc[(af_dose["on_doac"] != 0) & (af_dose["date"] >= '2021-01-01'), :]
pivot_dose = dose_subset.pivot(index='date', columns='on_doac', values='value')
pivot_dose.plot(kind='bar', color=('#003087'), edgecolor='white', figsize=(10,7), width=1, legend='')
plt.ylabel('Proportion (%) of patients with Atrial Fibrillation and with Cr/Cl')
plt.xlabel('Period')
#plt.ylim(ymin=0)
plt.gca()
plt.savefig(f'output/dose_match.png')
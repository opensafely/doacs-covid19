import pandas as pd
import matplotlib.pyplot as plt



# overall
df=pd.read_csv("../output/measure_doacs_by_region.csv", usecols=["date", "on_doac", "population"])
summary_df=df.groupby(["date"], as_index=False)["on_doac"].sum()
summary_df
summary_df.plot.bar(x="date", y="on_doac", xlabel='Date', ylabel='Count', title='Number of people prescribed a DOAC', edgecolor='grey')
plt.legend(loc='upper left')

# region
df=pd.read_csv("../output/measure_doacs_by_region.csv", usecols=["date", "region", "on_doac", "population"])
pivot_df = df.pivot(index='date', columns='region', values='on_doac')
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by region', stacked='True', edgecolor='white') 
plt.legend(loc='upper left')
axes = plt.gca()
pivot_df = df.pivot(index='date', columns='region', values='on_doac')
pivot_df.plot(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by region') 
plt.legend(loc='upper left')
axes = plt.gca()
axes.yaxis.grid()

# sex
df=pd.read_csv("../output/measure_doacs_by_sex.csv", usecols=["date", "sex", "on_doac", "population"])
pivot_df = df.pivot(index='date', columns='sex', values='on_doac')
pivot_df.plot(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by sex') 
plt.legend(loc='upper left')
axes = plt.gca()
axes.yaxis.grid()
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by sex', stacked=True, edgecolor='white') 
plt.legend(loc='upper left')
axes = plt.gca()
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by sex', stacked=False, edgecolor='white') 
plt.legend(loc='upper left')
axes = plt.gca()

# ethnicity
df=pd.read_csv("../output/measure_doacs_by_ethnicity.csv", usecols=["date", "ethnicity", "on_doac", "population"])
pivot_df = df.pivot(index='date', columns='ethnicity', values='on_doac')
pivot_df.plot(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by ethnicity') 
plt.legend(loc='upper left')
axes = plt.gca()
axes.yaxis.grid()
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by ethnicity', stacked=True, edgecolor='white') 
plt.legend(loc='upper left')
axes = plt.gca()

# age bands
df=pd.read_csv("../output/measure_doacs_by_age_band.csv", usecols=["date", "age_band", "on_doac", "population"])
pivot_df = df.pivot(index='date', columns='age_band', values='on_doac')
pivot_df.plot(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by age band') 
plt.legend(loc='upper left')
axes = plt.gca()
axes.yaxis.grid()
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC by age band', stacked=True, edgecolor='white') 
plt.legend(loc='upper left')
axes = plt.gca()

# carer
df=pd.read_csv("../output/measure_doacs_by_carer.csv", usecols=["date", "carer", "on_doac", "population"])
pivot_df = df.pivot(index='date', columns='carer', values='on_doac')
pivot_df.plot(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC coded as being a caregiver') 
plt.legend(["Not Caregiver", "Caregiver"], loc='upper left')
axes = plt.gca()
axes.yaxis.grid()
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Number of people prescribed a DOAC coded as being a caregiver', stacked=True, edgecolor='white') 
plt.legend(["Not Caregiver", "Caregiver"], loc='upper left')
axes = plt.gca()

# weight recorded in last 12 months
df=pd.read_csv("../output/measure_doacs_with_weight_recorded.csv", usecols=["date", "weight_recorded", "on_doac"])
pivot_df = df.pivot(index='date', columns='weight_recorded', values='on_doac')
pivot_df.plot.bar(xlabel='Period', ylabel='Count', title='Proportion of patients prescribed a DOAC with a weight recorded in the last 12 months', stacked='True', edgecolor='white') 
plt.legend(["On doac, weight not recorded", "On doac, weight recorded"], loc='upper left')
axes = plt.gca()





#coded with non-valvular atrial fibrillation 
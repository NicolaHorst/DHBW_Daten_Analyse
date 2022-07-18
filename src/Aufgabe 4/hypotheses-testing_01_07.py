#!/usr/bin/env python
# coding: utf-8

# # Statistische Tests
# 

# In[1]:


### Importieren aller relevanten Bibliotheken ###

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from scipy.stats import shapiro, levene
import scipy.stats as stats
import statistics


# In[2]:


### Einlesen der Daten ###
data = pd.read_csv('insurance.csv')
data_stud = pd.read_csv("StudentsPerformance.csv")
print(data.shape)
data.head()
data_stud.head()


# In[3]:


### Infos über die Daten ###
data.info()
data_stud.info()


# In[4]:


### BMI in geeignete Kodierungen umwandeln ###
def bmi_encoder(x):
  if x < 18.5:
    return 'underweight'
  elif x < 25:
    return 'normal'
  elif x < 30:
    return 'overweight'
  else:
    return 'obese'


# In[8]:


data['bmi'] = data['bmi'].apply(lambda x: bmi_encoder(x))
data.head()


# In[5]:


### Verteilung der verschiedenen Variablen mit Versicherungskosten ###

fig = px.bar(data, x='age',y='charges', title="Alter",
            labels={
                     "charges": "Versicherungskosten",
                     "age": "Alter"
                 }
            )
fig.show()

fig = px.bar(data, x='sex',y='charges', title="Geschlecht",
            labels={
                     "charges": "Versicherungskosten",
                     "sex": "Geschlecht"
                 }
            )
fig.show()

fig = px.bar(data, x='bmi',y='charges', title="BMI",
            labels={
                     "charges": "Versicherungskosten",
                     "bmi": "BMI"
                 }
            )
fig.show()

fig = px.bar(data, x='children',y='charges', title="Kinder",
            labels={
                     "charges": "Versicherungskosten",
                     "children": "Kinder"
                 }
            )
fig.show()

fig = px.bar(data, x='smoker',y='charges', title="Raucher VS Nicht Raucher",
            labels={
                     "charges": "Versicherungskosten",
                     "smoker": "Raucher"
                 }
            )
fig.show()

fig = px.bar(data, x='region',y='charges', title="Region",
            labels={
                     "charges": "Versicherungskosten",
                     "region": "Region"
                 }
            )
fig.show()

fig = px.bar(data_stud, x='gender',y='math score', title="Geschlecht",
            labels={
                     "math score": "Mathe-Note",
                     "gender": "Geschlecht"
                 }
            )
fig.show()

fig = px.bar(data_stud, x='test preparation course',y='math score', title="Prüfungsvorbereitungskurs",
            labels={
                     "math score": "Mathe-Note",
                     "test preparation course": "Prüfungsvorbereitungskurs"
                 }
            )
fig.show()

fig = px.bar(data_stud, x='race/ethnicity',y='math score', title="Nationalität",
            labels={
                     "math score": "Mathe-Note",
                     "race/ethnicity": "Nationalität"
                 }
            )
fig.show()


fig = px.bar(data_stud, x='parental level of education',y='math score', title="Bildungsniveau der Eltern",
            labels={
                     "math score": "Mathe-Note",
                     "parental level of education": "Bildungsniveau der Eltern"
                 }
            )
fig.show()


# # Hypothesen, die wir nach der Beobachtung der Daten testen konnten:
# 
# 
# **Two Sample Tests:**
# 
# Für 'data'
# - Raucher haben hohe Versicherungskosten
# - Versicherungskosten bleiben bei allen Geschlechtern ähnlich
# - Kinder zu haben hat keinen Einfluss auf die Versicherungskosten
# 
# Für 'data_stud'
# - Mathe-Note bleiben bei allen Geschlechtern ähnlich
# - Studenten die in einem Prüfungsvorbereitungskurs teilgenommen haben, haben bessere Mathe-Note
# 
# **Multiple Populations:**
# 
# Für 'data'
# - Alle 4 Regionen haben ähnliche Versicherungskosten
# - Unterschiedliche Versicherungskosten in den einzelnen BMI-Gruppen
# - Anzahl der Kinder hat keinen Einfluss auf die Versicherungskosten
# 
# Für 'data_stud'
# - Alle Nationalitäten haben ähnliche Mathe-Note
# - Bildungsniveau der Eltern hat keinen Einfluss auf die Mathe-Note
# 
# **Non-Numeric Tests:**
# 
# - Männer und Frauen haben unterschiedliche BMI-Verteilungen
# - Die Verteilung zwischen Männern und Frauen ist in allen Staaten gleich
# - Viele weitere Informationen im Abschnitt
# 

# ## Two Sample Tests

# ### Raucher vs. Nichtraucher Versicherungskosten

# In[7]:


smoker_insurance_charges = data[data['smoker'] == 'yes']['charges']
non_smoker_insurance_charges = data[data['smoker'] == 'no']['charges']

data['smoker_insurance_charges'] = smoker_insurance_charges

data['non_smoker_insurance_charges'] = non_smoker_insurance_charges

data.head()


# In[8]:


### Schritt 1 - Prüfen, ob die Daten normalverteilt sind ###
### Der Shapiro-Wilk-Test testet die Nullhypothese, dass die ###
### Daten aus einer Normalverteilung gezogen wurden ###
### Wenn pValue < 0,05 ist, ist die Verteilung nicht normal ###

smoker_dist = shapiro(smoker_insurance_charges)
non_smoker_dist = shapiro(non_smoker_insurance_charges)

print('pvalue for smoker Distribution: ', smoker_dist[1])
print('pvalue for non smoker Distribution: ', non_smoker_dist[1])


# In[9]:




fig = px.histogram(data, x="smoker_insurance_charges", title="Verteilung der Raucherversicherungskosten")
fig.show()

fig = px.histogram(data, x="non_smoker_insurance_charges", title="Verteilung der Nichtraucherversicherungskosten")
fig.show()



print('Hier sehen wir deutlich, dass beide Variablen nicht einer Normalverteilung folgen')


# In[10]:


### Schritt 2: Testen, ob beide Verteilungen die gleiche Varianz haben oder nicht ###
###Der Levene-Test testet die Nullhypothese, dass alle eingegebenen Stichproben###
### aus Populationen mit gleichen Varianzen stammen.  ###

lavene_test = levene(smoker_insurance_charges, non_smoker_insurance_charges)

print('pvalue for equal variance: ', lavene_test[1])


# In[12]:


### Schritt 3: Da die Verteilungen nicht normal sind ###
### und nicht die gleiche Varianz haben, verwenden wir den MannWhitney Test ###

different = stats.mannwhitneyu(smoker_insurance_charges, non_smoker_insurance_charges, alternative='two-sided')
sm_charge_lt_nsm = stats.mannwhitneyu(smoker_insurance_charges, non_smoker_insurance_charges, alternative='less')
sm_charge_gt_nsm = stats.mannwhitneyu(smoker_insurance_charges, non_smoker_insurance_charges, alternative='greater')
print('pvalue: ', different[1])
if different[1] < 0.05:
  print('Die Versicherungskosten zwischen Raucher und Nichtraucher sind unterschiedlich')

if sm_charge_lt_nsm[1] < 0.05:
  print('Raucher haben weniger Versicherungskosten als Nichtraucher')

if sm_charge_gt_nsm[1] < 0.05:
  print('Raucher haben mehr Versicherungskosten als Nichtraucher')


# ### Bildungsniveau Eltern: Bachelor VS College  Mathe-Note

# In[13]:


bachelor_math_score = data_stud[data_stud['parental level of education'] == "bachelor's degree"]['math score']
college_math_score = data_stud[data_stud['parental level of education'] == 'some college']['math score']

data_stud['bachelor_math_score'] = bachelor_math_score

data_stud['college_math_score'] = college_math_score

data_stud.head()


# In[14]:


male_dist = shapiro(bachelor_math_score)
female_dist = shapiro(college_math_score)

print('pvalue for Bachelor Distribution: ', male_dist[1])
print('pvalue for Colege Distribution: ', female_dist[1])


# In[15]:


fig = px.histogram(data_stud, x="bachelor_math_score", title="Verteilung der Bildungsniveau der Eltern: Bachelor")
fig.show()

fig = px.histogram(data_stud, x="college_math_score", title="Verteilung der Bildungsniveau der Eltern: College")
fig.show()



print('Hier sehen wir deutlich, dass beide Variablen nicht einer Normalverteilung folgen')


# In[16]:


lavene_test_mf = levene(bachelor_math_score, college_math_score, center='median')

print('pvalue for equal variance: ', lavene_test_mf[1])


# In[17]:


### Schritt 3: Da die Verteilungen normal sind ###
### und die gleiche Varianz haben, verwenden wir den T Test ###

different_mf = stats.ttest_ind(bachelor_math_score, college_math_score, equal_var = True)

print('pvalue:  ', different_mf[1])

if different_mf[1] < 0.05:
  print('Die Mathe-Note zwischen Bildungnieveau der Eltern ist unterschiedlich')
else:
   print('Die Mathe-Note zwischen Bildungnieveau der Eltern ist nicht unterschiedlich') 


# ### Kinder haben oder nicht haben

# In[18]:


c_insurance_charges = data[data['children'] > 0]['charges']
nc_insurance_charges = data[data['children'] == 0]['charges']

data['c_insurance_charges'] = c_insurance_charges
data['nc_insurance_charges'] = nc_insurance_charges

data.head()


# In[19]:


c_dist = shapiro(c_insurance_charges)
nc_dist = shapiro(nc_insurance_charges)

print('pvalue for chlidren Distribution: ', c_dist[1])
print('pvalue for no children Distribution: ', nc_dist[1])


# In[20]:


fig = px.histogram(data, x="c_insurance_charges", title="Verteilung Versicherungskosten wenn man Kinder hat")
fig.show()

fig = px.histogram(data, x="nc_insurance_charges", title="Verteilung Versicherungskosten wenn man keine Kinder hat")
fig.show()

print('Die Verteilung der Versicherungskosten ist nicht normal')


# In[21]:


lavene_test_c = levene(c_insurance_charges, nc_insurance_charges, center='median')

print('pvalue for equal variance: ', lavene_test_c[1])


# In[23]:


### Hier ist 1 der 2 Hauptannahmen des T/Z-Tests ungültig ###
### Das ist die Annahme der Normalverteilung ###
### Wenn die Verteilung normal wäre, hätten wir ### verwenden können
### T-Test mit ungleichen Varianzen ###

different_c = stats.mannwhitneyu(c_insurance_charges, nc_insurance_charges, alternative='two-sided')
c_charge_lt_nc = stats.mannwhitneyu(c_insurance_charges, nc_insurance_charges, alternative='less')
c_charge_gt_nc = stats.mannwhitneyu(c_insurance_charges, nc_insurance_charges, alternative='greater')
print('pvalue: ', different_c[1])
if different_c[1] < 0.05:
  print('Die 2 Verteilungen sind unterschiedlich')

if c_charge_lt_nc[1] < 0.05:
  print('Mit Kindern haben weniger Gebühren als ohne Kinder')

if c_charge_gt_nc[1] < 0.05:
  print('Mit Kindern haben mehr Gebühren als ohne Kinder')


# ## Multiple Populations

# ### Regionen vs. Versicherungen
# 
# Da Hier unsere Variable mehr als 2 underschiedliche Ausprägungen hat müssen wir ANOVA verwenden

# In[24]:


se = data[data['region'] == 'southeast']['charges']
nw = data[data['region'] == 'northwest']['charges']
sw = data[data['region'] == 'southwest']['charges']
ne = data[data['region'] == 'northeast']['charges']

data['se']= se
data['nw']= nw
data['sw']= sw
data['ne']= ne


# In[25]:


se_dist = shapiro(se)
nw_dist = shapiro(nw)
sw_dist = shapiro(sw)
ne_dist = shapiro(ne)

print('pvalue for se Distribution: ', se_dist[1])
print('pvalue for nw Distribution: ', nw_dist[1])
print('pvalue for sw Distribution: ', sw_dist[1])
print('pvalue for ne Distribution: ', ne_dist[1])


# In[26]:


fig = px.histogram(data, x="se", title="Verteilung Versicherungskosten wenn Region: se")
fig.show()

fig = px.histogram(data, x="nw", title="Verteilung Versicherungskosten wenn Region: nw")
fig.show()

fig = px.histogram(data, x="sw", title="Verteilung Versicherungskosten wenn Region: sw")
fig.show()

fig = px.histogram(data, x="ne", title="Verteilung Versicherungskosten wenn Region: ne")
fig.show()

print('Die Verteilung der Versicherungskosten ist nicht normal')


# In[27]:


lavene_test_region = levene(se, nw, sw, ne, center='median')

print('pvalue for equal variance: ', lavene_test_region[1])


# In[28]:


### Kruskal Willis Test ist die nicht parametrische Form der Anova ###
### Anova erfordert Normalität und Homogenität ###
### Hier ist unsere Verteilung nicht normal, sondern homogen ###
### Wir verwenden den Kruskal-Willis-Test zur Überprüfung der ###
### Nullhypothese, dass der Median aller Gruppen gleich ist ###

region_test = stats.kruskal(se, nw, sw, ne)
print('pvalue for the Kruskal Test = ', region_test[1])
if region_test[1] < 0.05:
  print('Regionale Verteilung der Versicherungskosten ist unterschiedlich')
else:
  print('Regionale Verteilung der Versicherungsprämien ist ähnlich')


# ### BMI vs Charges

# In[29]:


import seaborn as sns

middle_school = np.array([51.36372405, 44.96944041, 49.43648441, 45.84584407, 45.76670682,
       56.04033356, 60.85163656, 39.16790361, 36.90132329, 43.58084076])
high_school = np.array([56.65674765, 55.92724431, 42.32435143, 50.19137162, 48.91784081,
       48.11598035, 50.91298812, 47.46134988, 42.76947742, 36.86738678])
university = np.array([60.03609029, 56.94733648, 57.77026852, 47.29851926, 54.21559389,
       57.74008243, 50.92416154, 53.47770749, 55.62968872, 59.42984391])

print("Middle school Mean: ",np.mean(middle_school))
print("High school Mean: ",np.mean(high_school))
print("University Mean: ",np.mean(university))
total_mean = (np.mean(middle_school) + np.mean(high_school) + np.mean(university))/3
print("Total Mean: ",np.mean(total_mean))


middle_school_dist = shapiro(middle_school)
high_school_dist = shapiro(high_school)
university_dist = shapiro(university)

print('pvalue for middle_school Distribution: ', middle_school_dist[1])
print('pvalue for high_school Distribution: ', high_school_dist[1])
print('pvalue for university Distribution: ', university_dist[1])

sns.kdeplot(middle_school)
sns.kdeplot(high_school)
sns.kdeplot(university)
plt.show()


# In[30]:


stats.f_oneway(middle_school, high_school, university)


# In[ ]:





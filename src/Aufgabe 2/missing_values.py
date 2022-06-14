#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
#pip install -U scikit-learn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression

import missingno as msno


# ## Daten auslesen



train=pd.read_csv('train.csv')
test=pd.read_csv('test.csv')

print('Training data shape: ', train.shape)
print('Testing data shape: ', test.shape)

# Die ersten paar Zeilen des Trainingsdatensatzes
train.head()


# ## Untersuchung der Target Variable
# 
# >Für jeden Passagier im Testdatensatz müssen wir ein Modell erstellen, das vorhersagt, ob die Passagiere den Untergang der Titanic überlebt haben oder nicht. Überlebt ist also die abhängige Variable im Datensatz. Untersuchen wir nun die Verteilung der abhängige Variable





train['Survived'].value_counts()





s = sns.countplot(x = 'Survived',data = train)
sizes=[]
for p in s.patches:
    height = p.get_height()
    sizes.append(height)
    s.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}%'.format(height/len(train)*100),
            ha="center", fontsize=14) 


# Hier:
# * 0: nicht überlebt 
# * 1: überlebt 
# 
# 

# # Erkennung fehlender Werte
# 
# >Der erste Schritt ist die Ermittlung der Anzahl/des Prozentsatzes der fehlenden Werte in jeder Spalte des Datensatzes. Dies vermittelt einen Eindruck von der Verteilung der fehlenden Werte.



def missing_values_table(df):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Dein Datensatz hat " + str(df.shape[1]) + " columns.\n"      
            "Es gibt " + str(mis_val_table_ren_columns.shape[0]) +
              " Spalten mit missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns


# In[ ]:


train_missing= missing_values_table(train)
train_missing


# In[ ]:


test_missing= missing_values_table(test)
test_missing


# ## Visuelle Erkennung fehlender Daten mit der Missingno-Bibliothek
# 

# In[ ]:


msno.bar(train)


# >Das obige Balkendiagramm gibt einen schnellen grafischen Überblick über die Vollständigkeit des Datensatzes. Wir sehen, dass die Spalten Alter, Kabine und Einschiffung fehlende Werte aufweisen. 

# ## Suche nach dem Grund für fehlende Daten mithilfe einer Matrixdarstellung 

# In[ ]:


msno.matrix(train)


# >* Die Spalte "Embarked" weist nur sehr wenige fehlende Werte auf und scheint mit keiner anderen Spalte korreliert zu sein. Daher kann die Fehlmenge in der Spalte "Embarked" als "Missing Completely at Random" eingestuft werden.
# * Sowohl in der Spalte "Alter" als auch in der Spalte "Cabin" gibt es viele fehlende Werte, was ein Fall von MAR sein könnte, da wir den Grund für die fehlenden Daten in diesen Spalten nicht direkt beobachten können.
# 
# Mit dem missingno-Paket können wir das Diagramm auch nach einer bestimmten Spalte sortieren. Sortieren wir die Werte nach den Spalten "Age" und "Cabin", um zu sehen, ob es ein Muster bei den fehlenden Werten gibt

# In[ ]:


#sorted by Age
sorted = train.sort_values('Age')
msno.matrix(sorted)


# ## Löschen von fehlenden Daten

# In[ ]:


train.isnull().sum()


# In[ ]:


train_1 = train.copy()
train_1['Age'].mean() #pandas skips the missing values and calculates mean of the remaining values.


# 
# ### Listenweises Löschen/ Dropping rows
# 
# >Bei der listenweisen Löschung werden vollständige Zeilen (die die fehlenden Werte enthalten) gelöscht. Daher wird sie auch als vollständige Falllöschung bezeichnet.
# 

# In[ ]:


#Drop rows which contains any NaN or missing value for Age column
train_1.dropna(subset=['Age'],how='any',inplace=True)
train_1['Age'].isnull().sum()


# >Ein großer Nachteil des listenweisen Löschens ist, dass ein großer Teil der Daten und damit eine Menge Informationen verloren gehen. Daher ist es ratsam, diese Methode nur zu verwenden, wenn die Anzahl der fehlenden Werte sehr gering ist.

# 
# ### Weglassen ganzer Spalten 
# 
# Wenn eine Spalte viele fehlende Werte enthält, z. B. mehr als 80 %, und das Merkmal nicht signifikant ist, sollten Sie dieses Merkmal vielleicht löschen. Aber auch hier gilt, dass es keine gute Methode ist, Daten zu löschen.
# 

# ## Imputation
# 

# In[ ]:


# imputing with a constant

from sklearn.impute import SimpleImputer
train_constant = train.copy()
#setting strategy to 'constant' 
mean_imputer = SimpleImputer(strategy='constant') # imputing using constant value
train_constant.iloc[:,:] = mean_imputer.fit_transform(train_constant)
train_constant.isnull().sum()
# Die ersten paar Zeilen des Trainingsdatensatzes
train_constant.head()


# In[ ]:


from sklearn.impute import SimpleImputer
train_most_frequent = train.copy()
#setting strategy to 'mean' to impute by the mean
mean_imputer = SimpleImputer(strategy='most_frequent')# strategy can also be mean or median 
train_most_frequent.iloc[:,:] = mean_imputer.fit_transform(train_most_frequent)


# In[ ]:


train_most_frequent.isnull().sum()

# Die ersten paar Zeilen des Trainingsdatensatzes
train_most_frequent.head()


# ## Fortgeschrittene Imputationstechniken 
# 
# Bei fortgeschrittenen Imputationsverfahren werden Algorithmen des maschinellen Lernens verwendet, um die fehlenden Werte in einem Datensatz zu imputieren, im Gegensatz zu den vorherigen Verfahren, bei denen wir andere Spaltenwerte zur Vorhersage der fehlenden Werte verwendet haben. In dieser Vorlesung werden wir uns  folgende Technike ansehen:
# 
# * [Nearest neighbors imputation](https://scikit-learn.org/stable/modules/impute.html#nearest-neighbors-imputation)
# 
# ### K-Nearest Neighbor Imputation
# 
# Bei [KNNImputer class](https://scikit-learn.org/stable/modules/impute.html#multivariate-feature-imputation) wird jedes fehlende Merkmal mit Hilfe der Werte von n_Nächsten Nachbarn, die einen Wert für das Merkmal haben, unterstellt. Die Merkmale der Nachbarn werden gleichmäßig gemittelt oder nach der Entfernung zu jedem Nachbarn gewichtet. 

# In[ ]:


train_knn = train.copy(deep=True)


# In[ ]:


from sklearn.impute import KNNImputer
train_knn = train.copy(deep=True)

knn_imputer = KNNImputer(n_neighbors=2, weights="uniform")
train_knn['Age'] = knn_imputer.fit_transform(train_knn[['Age']])


# In[ ]:


train_knn['Age'].isnull().sum()

# Die ersten paar Zeilen des Trainingsdatensatzes
train_knn.head()


# In[ ]:





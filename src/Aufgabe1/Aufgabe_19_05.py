import pandas as pd

#load data
df = pd.read_csv("../../Data/laptops.csv", encoding='latin-1')

# show the head of the Dataframe
print(df.head())

# get Information about the Dataframe
df.info()


#das GB von ram weglassen und in einen numerischen Wert ändern
df['Ram'] = df['Ram'].replace('[GB]', '', regex=True)
df['Ram'] = pd.to_numeric(df['Ram'])


#jetzt für Weight
#das 'KG' entfernen und in eine numerische Zahl ändern
df['Weight'] =


print(df.head())

df.info()

#erstelle eine neue Variable mit der Name Angebot, die 100 Euro weniger als die aktuelle Preis ist
df['Angebot'] = df['Price_euros'] -100

print(df.head())

df.info()

#erstelle eine neue Variable mit der Name ersteAngebot, die 2% Euro weniger als die aktuelle Preis ist
df['ersteAngebot'] =

print(df.head())


#unbennene die Variable Angebot zum maxAngebot
df.rename(columns = {'Angebot':'maxAngebot'}, inplace = True)

print(df.head())

#unbennene die Variable Ram zum Ram_GB
df.rename(columns =

print(df.head())


#unbennene die Variable Weight zum Weight_KG
df.rename(columns =

print(df.head())

#erstelle eine neue Dataframe mit der Name apple, welche alle Daten von df enthält, die als Company Apple haben
is_apple =  df['Company']=="Apple"

apple = df[is_apple]

print(apple.head())

#erstelle eine neue Dataframe mit der Name Ultrabook, welche alle Daten von df enthält, die als TypeName Ultrabook haben
is_ultrabook=

print(Ultrabook.head())

#erstelle eine neue Dataframe mit der Name laptop_unt_1000, welche alle Daten von df enthält, die weniger als 1000 Euro kosten

unt_1000 =  df['Price_euros']<= 1000

laptop_unt_1000 = df[unt_1000]

print(laptop_unt_1000.head())

#erstelle eine neue Dataframe mit der Name Ultrabook_900, welche alle Daten von df enthält, die ein maxAngebot groeßer als 900 Euro haben

is_ultrabook_900=


print(Ultrabook_900.head())
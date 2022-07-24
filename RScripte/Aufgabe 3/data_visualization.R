#lade notwendige Paketen
library(dplyr)
library(stringr)
library(plotly)

#lade die Daten

df <- read.csv2("../Data/StudentsPerformance.csv", header = TRUE, sep= ",", dec=".")



# >Der Datensatz enthält 8 Spalten mit 1000 Einträgen.  
# 3 Spalten mit Continuirliche Werten und 5 Spalten mit Diskrete Werten.
# 
# 
# >Es gibt keine fehlenden Werte im Datensatz.  
# 



#Berechnung der Gesamtnote

x = df$math.score
y = df$reading.score
z = df$writing.score
total_marks = x+y+z

df$total.marks= total_marks/3


#sehe die Struktur der Daten
str(df)

#sehe Informationen für die Daten
summary(df)


# AUFGABE 1
# Bitte vergleichen Sie grafisch der Anzahl der Studenten, die in einem Vorbereitungskurs ("test preparation course") teilgenommen haben mit denen die nicht.

df_prep_course <- 
  df %>% 
  count(test.preparation.course) 

fig <- plot_ly(
  x = df_prep_course$test.preparation.course,
  y=df_prep_course$n,
  type = "bar"
)

fig <- fig %>% layout(title = "Vergleich anzahl Students die an Vorbereitungskurs teilgenommen haben", xaxis = list(title = 'Teilnahme'), yaxis = list(title = 'Anzahl'))
fig


# AUFGABE 2
# Bitte stellen Sie grafisch dar, ein geschlechtsspezifischer Vergleich der Nationalität ("race/ethnicity") der Studenten.


fig= plot_ly(
  data = df,
  x = ~race.ethnicity,
  y = ~total.marks,
  color = ~gender,
  type = "bar"
) %>% 
  layout(barmode = "stack", title = "Geschlechtsspezifischer Vergleich der Nationalität ", xaxis = list(title = 'Nationalität'), yaxis = list(title = 'Anzahl'))


fig


# AUFGABE 3
# Bitte überprüfen Sie grafisch die Verteilung der Variablen "math score", "reading score", "writing score".

# Verteilung Lese Note
fig <- plot_ly(x = df$reading.score, type = "histogram",)%>% 
  layout(title = "Verteilung Lesenote", xaxis = list(title = 'Lese Note'), yaxis = list(title = 'Anzahl'))

fig



# Verteilung Schreibe Note
fig <- plot_ly(x = df$writing.score, type = "histogram",)%>% 
  layout(title = "Verteilung Schreib Note", xaxis = list(title = 'Schreibe Note'), yaxis = list(title = 'Anzahl'))

fig



# Verteilung Mathe Note
fig <- plot_ly(x = df$math.score, type = "histogram",)%>% 
  layout(title = "Verteilung Mathe", xaxis = list(title = 'Mathe Note'), yaxis = list(title = 'Anzahl'))

fig


# AUFGABE 4
# Bitte überprüfen Sie grafisch, ob es eine Beziehung bei der Mathe-Note ("math score") und die Schreib-Note ("writing score ") gibt.

fig <- plot_ly(data = df, x = ~writing.score, y = ~math.score, type = "scatter")

fig




# AUFGABE 5
# Bitte überprüfen Sie grafisch, ob es eine Beziehung bei der Mathe-Note ("math score") und das Geschlecht ("gender") gibt.

fig <- plot_ly(data = df, x = ~math.score, color = ~gender, type = "scatter")
fig


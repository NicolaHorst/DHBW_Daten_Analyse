# Importieren aller relevanten Bibliotheken

library(dplyr)
library(stringr)
library(plotly)
library(onewaytests)
library(car)

#lade die Daten

data_insurance <- read.csv2("../Data/insurance.csv", header = TRUE, sep= ",", dec=".")
data_stud <- read.csv2("../Data/StudentsPerformance.csv", header = TRUE, sep= ",", dec=".")
data_iris <- read.csv2("../Data/Iris.csv", header = TRUE, sep= ",", dec=".")



### Infos über die Daten ###
str(data)
str(data_stud)


# AUFGABE 1
# Bitte überprüfen Sie in Python und R, ob die Versicherungskosten bei allen Geschlechtern ähnlich bleiben und begründen Sie Ihre Entscheidung (insurance.csv).

## Schritt 1 prüfen auf normalverteilung
onewaytests::nor.test(charges~sex, data = data_insurance)


fig <- plot_ly(x = data_insurance$charges, color = data_insurance$sex, type = "histogram")
fig

# Die Daten sind nicht normalverteilt



## Schritt 2 Prüfen ob die verteilungen die gleiche Varianz haben
levent_test <- leveneTest(data_insurance$charges, data_insurance$sex)
levent_test$`Pr(>F)`

# Die Verteilungen haben nicht die selbe Varianz


##Schritt 3: Da die Verteilungen nicht normalverteilt sind und nicht die gleiche Varianz haben, verwenden wir den MannWhitney Test
data_male= filter(data_insurance, sex == "male")
data_female= filter(data_insurance, sex == "female")

results <- wilcox.test(data_female$charges, data_male$charges, exact = TRUE, correct = TRUE, conf.int = TRUE)
results$p.value

# Da der P-Value größer als 0.05 ist, gibt es keinen Unterschied zwischen den Versicherungskosten von Frauen und Männer



# AUFGABE 2
# Bitte überprüfen Sie in Python und R, ob Studenten, die in einem Prüfungsvorbereitungskurs teilgenommen haben, bessere Mathe-Note haben und begründen Sie Ihre Entscheidung (StudentsPerformance.csv).


## Schritt 1 prüfen auf normalverteilung
onewaytests::nor.test(math.score ~ test.preparation.course, data = data_stud)


fig <- plot_ly(x = data_stud$math.score, color = data_stud$test.preparation.course, type = "histogram")
fig

# Die Daten sind nicht normalverteilt



## Schritt 2 Prüfen ob die verteilungen die gleiche Varianz haben
levent_test <- leveneTest(data_stud$math.score, data_stud$test.preparation.course)
levent_test$`Pr(>F)`

# Die Verteilungen haben nicht die selbe Varianz


## Schritt 3: Da die Verteilungen nicht normalverteilt sind und nicht die gleiche Varianz haben, verwenden wir den MannWhitney Test
data_participated= filter(data_stud, test.preparation.course == "completed")
data_not_participated= filter(data_stud, test.preparation.course == "none")

results <- wilcox.test(data_not_participated$math.score, data_participated$math.score, exact = TRUE, correct = TRUE, conf.int = TRUE)
results$p.value
# Da der P-Value kleiner als 0.05 ist, gibt es einen Unterschied zwischen den den Mathenoten bei personen die am preparation Kurs teilgenommen haben

results_lt <- wilcox.test(data_not_participated$math.score, data_participated$math.score, exact = TRUE, correct = TRUE, conf.int = TRUE, alternative = "less")
results_lt$p.value
# Da der P-Value für die alternative less kleiner als 0.05 ist, haben studenten die nicht am test teilgenommen haveb eine schlechtere Noten als Teilnehmer


# AUFGABE 3
# Bitte überprüfen Sie in Python und R, ob Studenten, die ihre Eltern ein „Bachelor“ Abschluss hatten, bessere Reading-Score haben als Studenten, 
# die ihre Eltern ein „College“ Abschluss hatten, und begründen Sie Ihre Entscheidung (StudentsPerformance.csv).
## Schritt 1 prüfen auf normalverteilung

normal_distributed <- onewaytests::nor.test(reading.score ~ parental.level.of.education, data = data_stud)
normal_distributed$Level
normal_distributed$p.value

fig <- plot_ly(x = df_parents_bachelor$reading.score, type = "histogram")
fig

fig <- plot_ly(x = df_parents_no_bachelor$reading.score, type = "histogram")
fig

# Bachelors Degree ist normal verteilt aber some college nicht



## Schritt 2 Prüfen ob die verteilungen die gleiche Varianz haben
levent_test <- leveneTest(data_stud$reading.score, data_stud$parental.level.of.education)
levent_test$`Pr(>F)`

# Die Verteilungen haben die selbe Varianz


## Schritt 3: Da die Verteilungen nicht alle normalverteilt sind und nicht die gleiche Varianz haben, verwenden wir den MannWhitney Test
df_parents_bachelor <- filter(data_stud, parental.level.of.education == "bachelor's degree")
df_parents_no_bachelor <- filter(data_stud, parental.level.of.education == "some college")

results <- wilcox.test(df_parents_no_bachelor$reading.score, df_parents_bachelor$reading.score, exact = TRUE, correct = TRUE, conf.int = TRUE)
results$p.value
# Die Lesenote zwischen Kindern mit Eltern die einen Bachelor haben und Kindern mit Eltern die keinen Bachelor haben sind nicht unterschiedlich



# AUFGABE 4
# Bitte überprüfen Sie in Python und R, ob unterschiedliche Versicherungskosten in den einzelnen BMI-Gruppen fallen und begründen Sie Ihre Entscheidung (insurance.csv).
# Schritt 1 prüfen auf normalverteilung

### BMI in geeignete Kodierungen umwandeln ###
data_insurance$bmi <- ifelse(data_insurance$bmi < 18.5, "underweight", ifelse(data_insurance$bmi < 25, "normal", ifelse(data_insurance$bmi < 30, "overweight",  "obese")))

normal_distributed <- onewaytests::nor.test(
  charges ~ bmi,
  data = data_insurance
)
normal_distributed$Level
normal_distributed$p.value

fig <- plot_ly(
  x = data_insurance$charges,
  color = data_insurance$bmi,
  type = "histogram"
)
fig

# Dadurch das die Verteilungen nicht normal sind können wir das prüfen der Varianz weglassen und direkt einen Kruskal test machen.
results_kruskal <- kruskal.test(data_insurance$charges ~ data_insurance$bmi)
results_kruskal$p.value



# AUFGABE 5
# Bitte überprüfen Sie in Python und R, ob es Unterschiede bei petal.length für die verschiedene Iris-Arten gibt. Bitte begründen Sie Ihre Entscheidung (Iris.csv).  

summary(aov(data_iris$PetalLengthCm ~ data_iris$Species))

TukeyHSD(aov(data_iris$PetalLengthCm ~ data_iris$Species))

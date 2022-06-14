#lade notwendige Paketen
library(dplyr)
library(stringr)

#lade die Daten

#train <- read.csv2("train.csv", header = TRUE, sep= ",", dec=".")

train <- read.csv2("train.csv", header = TRUE, sep= ",", dec= "../../../../../Desktop/Alle Dateien", na.strings=c("", "NA"))

#sehe die Struktur der Daten
str(train)

#sehe Informationen für die Daten
summary(train)

# Wie hoch ist der Anteil der fehlenden Daten für jede Variable?
pctmiss <- colSums(is.na(train))/nrow(train)*100



#visualisieren von fehlende Werte

install.packages("igraph", type="binary")

if (!require(devtools)) install.packages("devtools")
devtools::install_github("boxuancui/DataExplorer")

library(DataExplorer)

plot_missing(train)


#Listwise deletion

newdata <- train
newdata <- na.omit(newdata)


#Verwendung der Hmisc-Packet und Imputation mit dem Medianwert

library(Hmisc)
newdata_med <- train
newdata_med$Age=impute(newdata_med$Age, median)

#Imputieren mit einem bestimmten konstanten Wert

library(Hmisc)
newdata_const <- train

newdata_const$Cabin=impute(newdata_const$Cabin, "keine wert") 


# Imputieren fehlender Werte unter Verwendung der 5 nächstgelegenen Nachbarn
library(VIM)
imputedata <- kNN(train, k=5)
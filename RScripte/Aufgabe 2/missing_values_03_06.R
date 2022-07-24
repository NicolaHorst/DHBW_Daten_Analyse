#lade notwendige Paketen
library(dplyr)
library(stringr)
# install.packages("igraph", type="binary")


#lade die Daten

test_data <- read.csv2("../Data/test.csv", header = TRUE, sep= ",", dec=".", na.strings=c("", "NA"))


#sehe die Struktur der Daten
str(test_data)

#sehe Informationen für die Daten
summary(test_data)

# Wie hoch ist der Anteil der fehlenden Daten für jede Variable?
pctmiss <- colSums(is.na(test_data))/nrow(test_data)*100



#visualisieren von fehlende Werte


if (!require(devtools)) install.packages("devtools")
devtools::install_github("boxuancui/DataExplorer")

library(DataExplorer)

plot_missing(test_data)


#Listwise deletion

newdata <- test_data
newdata <- na.omit(newdata)


#Verwendung der Hmisc-Packet und Imputation mit dem Medianwert

library(Hmisc)
newdata_med <- test_data
newdata_med$Age=impute(newdata_med$Age, median)

#Imputieren mit einem bestimmten konstanten Wert

library(Hmisc)
newdata_const <- test_data

newdata_const$Cabin=impute(newdata_const$Cabin, "keine wert") 


# Imputieren fehlender Werte unter Verwendung der 5 nächstgelegenen Nachbarn
library(VIM)
imputedata <- kNN(test_data, k=5)


# Lineare Regression
# Importieren aller benötigten Libaries
library(glmnet)
library(here)

# Set seed
set.seed(1337)


# load data
students_data <- read.csv2(
  "C:\\Users\\nic-e\\OneDrive\\Dokumente\\GitHub\\DHBW_Daten_Analyse\\Data\\StudentsPerformance.csv",
  header = TRUE, sep = ",", dec = ".", stringsAsFactors = T
)

# split data into training and test sets
training_indices <- sample(nrow(students_data), nrow(students_data) * 0.8)
training_data <- students_data[training_indices, ]
test_data <- students_data[-training_indices, ]

# Show number of samples per set
cat(paste0(
  "Size of training data: ", nrow(training_data), "\n",
  "Size of test data: ", nrow(test_data), "\n"
))

# Perform a single-pass linear regression
model <- glm(math.score ~ ., data = students_data)

# Show the evaluation of the model
print(summary(model))


# Calculate mean squared errors for the model
model_mse <- mean(
  (
    predict(model, test_data) - test_data$math.score
  ) ^ 2
)
cat(paste0("Model's MSE: ", model_mse, "\n"))

# Visualizing the model's performance on the test data
plot(
  x = predict(model), y = students_data$math.score,
  xlab = "Values (Predicted)",
  ylab = "Values (Actual)",
  main = "Predicted vs. Actual Values"
)
abline(a = 0, b = 1)


#Auteur Daniel Nissille
#Petite ébauche de test statistique pour mesurer l'efficacité du pipeline EduRisk

getwd()
setwd("C:/Users/Daniel/Desktop/OpenScience/Report_material/Code_test")

#charger les données test
data <- read.csv("resultats_qcm.csv",
  header = TRUE,
  sep = ",",
  stringsAsFactors = FALSE,
  colClasses = c(
    "character",  # participant_id
    "character",  # edurisk
    rep("integer", 5),  # Q1 à Q5
    "numeric"     # temps_total_sec
  )
)

str(data)
unique(data$edurisk)
#vecteur des bonnes réponses
bonnes_reponses <- c(1,2,2,2,1)
data$score <- rowSums(data[, c("Q1", "Q2", "Q3","Q4","Q5")] == bonnes_reponses)

#vérification que tout s'est bien construit
unique(data$edurisk)
colnames(data)
summary(data$score)
table(data$edurisk)
aggregate(score ~ edurisk, data = data, summary)

#boxplot simple des cas
boxplot(score ~ edurisk,
        data = data,
        names = c("Contrôle", "Edurisk"),
        ylab = "Score",
        main = "Score selon la condition Edurisk")

#mesure de la normalité pour svoir si on doit utiliser un test paramètrique ou non.
shapiro.test(data$score[data$edurisk == "False"])#test de normalité
shapiro.test(data$score[data$edurisk == "True"])

#mesure des variances pour savoir si on doit faire un test de student ou de Welch
var.test(score ~ edurisk, data = data)

#test de student (variance égales)
t.test(score ~ edurisk,data=data,var.equal = TRUE)
#test welch (variance inégales )
t.test(score ~ edurisk,data=data,var.equal = FALSE)

#analyse du temps
t.test(temps_total_sec ~ edurisk, data = data)

#indice d de cohen pour mesurer l'effet réel de la méthode
library(effsize)
cohen.d(score ~ edurisk, data = data)
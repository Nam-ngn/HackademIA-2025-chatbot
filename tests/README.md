# Pipeline de test pour EduRisk
Auteur Daniel Nissille (groupe 3)<br>
Decembre 2025<br>
Dans le cadre du cours Open Science<br>  

**Note importante**: Cette version est une ébauche et pourra être
améliorée par un retour concret sur un vrai jeu de données.


## Guide d'installation et d'utilisation
-------------------------

### 1.Installer Python

- 1.1 Rendez-vous sur le site officiel : https://www.python.org/downloads  
- 1.2 Téléchargez la version stable (recommandée : Python 3.x).  
- 1.3 Pendant l'installation, cochez l'option "Add Python to PATH".  
- 1.4 Vérifiez l'installation :

	python --version  
	ou  
	python3 --version

-------------------------

### 2.Installer R et RStudio

- 2.1 Rendez-vous sur le site CRAN : https://cran.r-project.org/  
- 2.2 Téléchargez la version adaptée à votre système d'exploitation (Windows, MacOS, Linux).  
- 2.3 Installez R avec les options par défaut.  
- 2.4 Rendez-vous sur : https://posit.co/download/rstudio-desktop/  
- 2.5 Téléchargez et installez la version gratuite (RStudio Desktop).

-------------------------

### 3.Installer une librairie R non native.
- 3.1 Ouvrez RStudio  
- 3.2 dans la consol, tapez:

	install.packages("effsize")

- 3.3 chargez la librairie avec:

	library(effsize)

-------------------------

### 4. Lancer le QCM en Python

- 4.1 Ouvrez un terminal (ou PowerShell sur Windows).  
- 4.2 Placez-vous dans le dossier contenant ControlTest.py :

	cd /chemin/vers/le/dossier

- 4.3 Lancez le script :

	python ControlTest.py

- 4.4 L'utilisateur est prêt pour effectuer le test.

-------------------------

### 5 Lancer le script RStudio 

- 5.1 Ouvrez RStudio.  
- 5.2 Dans le menu, cliquez sur File -> Open File... et sélectionnez votre script R ExempleTestR.  
- 5.3 Dans la console R, exécutez le script. (petite flèche exécution)  
- 5.4 Assurez-vous que la librairie  (effsize) est bien isntallée. 

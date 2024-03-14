class Client:
    def __init__(self, nom, prenom, age, adresse, mot_de_passe):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.adresse = adresse
        self.mot_de_passe = mot_de_passe

    def afficher_infos(self):
        print(f"Nom: {self.nom}, Prénom: {self.prenom}, Âge: {self.age}, Adresse: {self.adresse}")


class CompteBancaire:
    def __init__(self, proprietaire, solde=0):
        self.proprietaire = proprietaire
        self.solde = solde
        self.operations = []

    def deposer(self, montant):
        self.solde += montant
        self.operations.append(f"Dépôt: +{montant} MAD")
        print(f"{montant} MAD ont été déposés dans le compte de {self.proprietaire.nom}. Nouveau solde : {self.solde} MAD")

    def retirer(self, montant):
        if self.solde >= montant:
            self.solde -= montant
            self.operations.append(f"Retrait: -{montant} MAD")
            print(f"{montant} MAD ont été retirés du compte de {self.proprietaire.nom}. Nouveau solde : {self.solde} MAD")
        else:
            print("Solde insuffisant.")

    def consulter_solde(self):
        print(f"Solde du compte de {self.proprietaire.nom}: {self.solde} MAD")

    def afficher_operations(self):
        print(f"Opérations du compte de {self.proprietaire.nom}:")
        for operation in self.operations:
            print(operation)


class CompteEpargne(CompteBancaire):
    def __init__(self, proprietaire, solde=0, taux_interet=0.01):
        super().__init__(proprietaire, solde)
        self.taux_interet = taux_interet

    def calculer_interets(self):
        interets = self.solde * self.taux_interet
        self.solde += interets
        self.operations.append(f"Intérêts: +{interets} MAD")
        print(f"Intérêts calculés pour le compte de {self.proprietaire.nom}: {interets} MAD. Nouveau solde : {self.solde} MAD")


class CompteCheques(CompteBancaire):
    def __init__(self, proprietaire, solde=0, decouvert_autorise=0):
        super().__init__(proprietaire, solde)
        self.decouvert_autorise = decouvert_autorise

    def retirer(self, montant):
        if self.solde + self.decouvert_autorise >= montant:
            self.solde -= montant
            self.operations.append(f"Retrait: -{montant} MAD")
            print(f"{montant} MAD ont été retirés du compte de {self.proprietaire.nom}. Nouveau solde : {self.solde} MAD")
        else:
            print("Opération impossible: dépassement du découvert autorisé.")


class Banque:
    def __init__(self, nom):
        self.nom = nom
        self.clients = []
        self.comptes = {}

    def ajouter_client(self, client):
        self.clients.append(client)
        print(f"Le client {client.nom} {client.prenom} a été ajouté à la banque {self.nom}.")

    def creer_compte(self, client, type_compte, **kwargs):
        if client in self.clients:
            if type_compte == "epargne":
                compte = CompteEpargne(client, **kwargs)
            elif type_compte == "cheques":
                compte = CompteCheques(client, **kwargs)
            else:
                print("Type de compte non pris en charge.")
                return
            self.comptes[client.nom] = compte
            print(f"Un compte {type_compte} a été créé pour {client.nom}.")
        else:
            print("Le client n'est pas enregistré dans la banque.")

    def effectuer_virement(self, origine, destination, montant):
        if origine in self.comptes and destination in self.comptes:
            if self.comptes[origine].solde >= montant:
                self.comptes[origine].retirer(montant)
                self.comptes[destination].deposer(montant)
                print(f"Virement de {montant} MAD effectué de {origine} vers {destination}.")
            else:
                print("Solde insuffisant pour effectuer le virement.")
        else:
            print("Compte(s) non trouvé(s). Veuillez vérifier les informations fournies.")

    def afficher_tous_comptes(self):
        print("Liste de tous les comptes :")
        for nom, compte in self.comptes.items():
            print(f"Propriétaire: {nom}, Solde: {compte.solde} MAD")


class Admin:
    def __init__(self, nom_utilisateur, mot_de_passe):
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe

    def afficher_infos(self):
        print(f"Nom d'utilisateur: {self.nom_utilisateur}")

    def modifier_nom_utilisateur(self, banque, client, nouveau_nom):
        if client in banque.clients:
            client.nom = nouveau_nom
            print("Le nom de l'utilisateur a été modifié avec succès.")
        else:
            print("Le client n'est pas enregistré dans la banque.")


def affichage_menu():
    print("\n" + "-" * 50)
    print("Bienvenue à la Banque IARV")
    print("Veuillez vous connecter:")
    print("-" * 50)


def login():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    return username, password


def executer_programme(banque):
    affichage_menu()
    while True:
        username, password = login()
        if username == "admin" and password == "password":
            print("Connexion réussie.\n")
            break
        else:
            print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.\n")
            affichage_menu()

    while True:
        print("\n" + "-" * 50)
        print("Que souhaitez-vous faire ?")
        print("1. Gestion des clients")
        print("2. Gestion des comptes")
        print("3. Effectuer un virement")
        print("4. Afficher tous les comptes")
        print("5. Se connecter en tant que client")
        print("6. Quitter")
        print("-" * 50)

        choix = input("Choix : ")

        if choix == "1":
            gerer_clients(banque)
        elif choix == "2":
            gerer_comptes(banque)
        elif choix == "3":
            effectuer_virement(banque)
        elif choix == "4":
            banque.afficher_tous_comptes()
        elif choix == "5":
            login_client(banque)
        elif choix == "6":
            print("Merci d'avoir utilisé nos services. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez saisir un nombre entre 1 et 6.")

def login_client(banque):
    print("\n" + "-" * 50)
    print("Se connecter en tant que client")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    for client in banque.clients:
        if client.nom == username and client.mot_de_passe == password:
            print("Connexion réussie en tant que client.\n")
            menu_client(client, banque)
            return

    print("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.\n")

def menu_client(client, banque):
    while True:
        print("\n" + "-" * 50)
        print("Que souhaitez-vous faire ?")
        print("1. Consulter le solde de votre compte")
        print("2. Effectuer un dépôt")
        print("3. Effectuer un retrait")
        print("4. Afficher les opérations de votre compte")
        print("5. Retourner à la page de connexion")
        print("6. Quitter")
        print("-" * 50)

        choix = input("Choix : ")

        if choix == "1":
            banque.comptes[client.nom].consulter_solde()
        elif choix == "2":
            montant = float(input("Entrez le montant à déposer : "))
            banque.comptes[client.nom].deposer(montant)
        elif choix == "3":
            montant = float(input("Entrez le montant à retirer : "))
            banque.comptes[client.nom].retirer(montant)
        elif choix == "4":
            banque.comptes[client.nom].afficher_operations()
        elif choix == "5":
            print("Retour à la page de connexion.\n")
            return
        elif choix == "6":
            print("Merci d'avoir utilisé nos services. À bientôt !")
            exit()
        else:
            print("Choix invalide. Veuillez saisir un nombre entre 1 et 6.")

def gerer_clients(banque):
    print("\n" + "-" * 50)
    print("Gestion des clients")
    print("1. Ajouter un client")
    print("2. Modifier le nom d'un client")
    print("3. Retour au menu principal")
    choix = input("Choix : ")

    if choix == "1":
        ajouter_client(banque)
    elif choix == "2":
        modifier_nom_client(banque)
    elif choix == "3":
        pass
    else:
        print("Choix invalide. Veuillez saisir un nombre entre 1 et 3.")

def ajouter_client(banque):
    print("\n" + "-" * 50)
    print("Ajouter un client")

    nom_client = input("Entrez le nom du client : ")
    prenom_client = input("Entrez le prénom du client : ")
    age_client = int(input("Entrez l'âge du client : "))
    adresse_client = input("Entrez l'adresse du client : ")
    mot_de_passe_client = input("Entrez le mot de passe du client : ")

    client = Client(nom_client, prenom_client, age_client, adresse_client, mot_de_passe_client)
    banque.ajouter_client(client)


def modifier_nom_client(banque):
    print("\n" + "-" * 50)
    print("Modifier le nom d'un client")

    nom_client = input("Entrez le nom du client à modifier : ")
    for client in banque.clients:
        if client.nom == nom_client:
            nouveau_nom = input("Entrez le nouveau nom : ")
            client.nom = nouveau_nom
            print("Nom modifié avec succès.")
            return
    print("Client non trouvé.")


def gerer_comptes(banque):
    print("\n" + "-" * 50)
    print("Gestion des comptes")
    print("1. Créer un compte")
    print("2. Retour au menu principal")
    choix = input("Choix : ")

    if choix == "1":
        creer_compte(banque)
    elif choix == "2":
        pass
    else:
        print("Choix invalide. Veuillez saisir un nombre entre 1 et 2.")

def creer_compte(banque):
    print("\n" + "-" * 50)
    print("Création d'un nouveau compte")

    nom_client = input("Entrez le nom du client : ")
    prenom_client = input("Entrez le prénom du client : ")
    for client in banque.clients:
        if client.nom == nom_client and client.prenom == prenom_client:
            type_compte = input("Entrez le type de compte (epargne/cheques) : ")

            if type_compte == "epargne":
                solde_initial = float(input("Entrez le solde initial du compte épargne : "))
                taux_interet = float(input("Entrez le taux d'intérêt du compte épargne (en décimal) : "))
                banque.creer_compte(client, "epargne", solde=solde_initial, taux_interet=taux_interet)
            elif type_compte == "cheques":
                solde_initial = float(input("Entrez le solde initial du compte chèques : "))
                decouvert_autorise = float(input("Entrez le découvert autorisé du compte chèques : "))
                banque.creer_compte(client, "cheques", solde=solde_initial, decouvert_autorise=decouvert_autorise)
            else:
                print("Type de compte non pris en charge.")
            return
    print("Client non trouvé.")

def effectuer_virement(banque):
    print("\n" + "-" * 50)
    print("Effectuer un virement")
    origine = input("Entrez le nom du client émetteur : ")
    destination = input("Entrez le nom du client bénéficiaire : ")
    montant = float(input("Entrez le montant du virement : "))
    banque.effectuer_virement(origine, destination, montant)

# Exemple d'utilisation
banque1 = Banque("Banque IARV")
admin = Admin("admin", "password")

executer_programme(banque1)

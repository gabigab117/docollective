# DOCOLLECTIVE

Une plateforme d'échange de vêtements. Réalisée dans le cadre du projet du mois d'octobre Docstring.
L'idée est qu'un utilisateur peut choisir 1 ou plusieurs vêtements. Il valide la commande (sans payer). En contrepartie
il doit créer des annonces et envoyer des vêtements à la plateforme pour recevoir ceux qu'il voulait. L'idée est de
créer une plateforme purement basée sur l'échange.

## App Utilisateurs (accounts)

Un package views :

- users.py pour tout ce qui est signup, login, logout et profil.
- password.py pour ce qui concerne le changement de mot de passe et la demande d'un nouveau.

### Profil

L'utilisateur a accès à ses informations personnelles. Il peut créer des adresses et en sélectionner une par défaut.
Ajout de la MAJ du profil (maj 11 nov 2023)

### Password

Utilisation des classes de Django ==> 100% héritage

## App Marketplace (shop)

L'idée n'est pas de gagner de l'argent ici (règle du projet Docstring). Je n'ai donc pas intégré Stripe sur ce projet.
Traditionnelles vues d'index, de détail, de liste des instances, mais...

Un utilisateur qui va sur sa propre annonce ne peut pas l'ajouter au panier, il ne peut que supprimer l'annonce.

Les vues sont dans un package. (Maj 11 nov 2023)

### Les recommandations

Création d'une vue pour les recommandations. Pour la première fois, j'ai utilisé les requêtes Q.
Une vue spécifique avec des annonces en fonction des préférences de l'utilisateur.
Afin de ne pas avoir d'erreur "NonType" j'ai mis en place des "property" qui retournent les préférences de l'utilisateur
ou (or) "NC".

### Ajout au panier

Vérification : L'annonce est-elle déjà dans un panier ? Ou bien même dans mon panier ?
Si on est sur notre propre annonce, Ajouter au panier ne s'affiche pas, mais Supprimer l'annonce à la place.

### La panier

modelformset_factory pour pouvoir sélectionner et supprimer plusieurs éléments

### Choix de l'adresse

Au moment de la commande. J'utilise une vue de l'app accounts. Pour être redirigé au bon endroit j'utilise un paramètre
d'url.

### Validation du panier

Après avoir déterminé une adresse, lors de la validation du panier un email est envoyé à l'utilisateur.

### Suppression d'une annonce

Surcharge de form_valid afin de rendre la suppression d'une annonce si elle est dans un panier.

### Tableau de bord utilisateur

my_shop_view. Les annonces publiées, en attente de modération, mes demandes d'échanges, les échanges validés.

### Pour les administrateurs

- Vue pour valider les demandes d'échanges
- Vue pour valider la publication des annonces

## App SAV (sav)

Gérer les demandes des utilisateurs.
Un modèle Ticket et un modèle Message. Un ticket comportera des messages.

L'utilisateur peut Ouvrir un ticket, consulter les tickets en cours et l'historique des tickets clôturés.

### Ouverture d'un ticket

Lorsqu'un utilisateur écrit un premier message, j'utilise un ModelForm avec un champ supplémentaire qui me permet de
créer un ticket et d'associer le message au ticket.

### Les tickets en cours

La vue d'un ticket est limitée aux superusers et au "propriétaire" du ticket. Un formulaire permet de poster des
messages.

### Clôture

Vue pour clôturer un ticket.

### Administration

Une vue pour les superusers, ils peuvent consulter tous les tickets en cours.

## Fixtures

Vous devez utiliser toutes les fixtures pour la BDD ==> python manage.py loaddata accounts.json shop.json sav.json

Super utilisateur ==> login superuser@super.fr password Robert_PatrickT1000

Utilisateur ==> login user@user.fr password Arnold_SchwT800

## .env

SECRET_KEY=

DEBUG=True

ALLOWED_HOSTS="127.0.0.1"

ENV="DEV"


Recaptcha :

RECAPTCHA_PUBLIC_KEY=

RECAPTCHA_PRIVATE_KEY=


Serveur Mail :

EMAIL_ID=

EMAIL_PW=

# A faire

Continuer les tests
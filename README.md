# docollective

Une plateforme d'échange de vêtements.

# Tâches

- limiter à 5 adresses
- vue all avec filtres
- vue favoris
- l'échange en lui mm
- et passer en commandé avec espace client
- Des tests !
- En option, un abo Stripe

# Problèmes à résoudre

- L'échange, créer un modèle intermédiaire que les deux parties doivent cocher à True

# Reprendre

- Empêcher un delete quand un article est dans un panier

# Notes

- Url lisible : pk + slug

# Thibault

- Soit tu fais juste un 1-1 et quand un vêtement t'intéresse, ça notifie la personne, ensuite elle a le choix de trouver
dans ce que tu as quelque chose qui l'intéresse également, et il peut y avoir un "match"

- Soit tu fais un truc plus général, et tu peux juste faire un modèle comme les bibliothèques gratuites dans les rues, du
style prend un livre, donne un livre. Donc là ça serait, tu peux récupérer un vêtement / item seulement si tu en donnes
un en échange

### 1er cas
1 - 1, faire un match avec une personne
### 2eme cas
Envoyer son vêtement, une fois reçu on m'expédie celui commandé
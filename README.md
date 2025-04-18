# Wordle Game

Un jeu Wordle en Python, inspiré du jeu original, où le but est de deviner un mot de 5 lettres en un maximum de 6 tentatives.

## 🎮 Fonctionnalités

- Devinez un mot de 5 lettres en 6 tentatives maximum
- Feedback visuel avec code couleur :
  - 🟩 Vert : Lettre correcte et bien placée
  - 🟨 Jaune : Lettre présente mais mal placée
  - ⬜ Gris : Lettre absente du mot
- Validation des entrées :
  - Vérification de la longueur du mot (5 lettres)
  - Vérification que le mot ne contient que des lettres
- Interface en ligne de commande simple et intuitive

## 📋 Prérequis

- Python 3.x
- Aucune dépendance externe nécessaire

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
cd wordle_project
```

2. Le projet est prêt à être utilisé !

## 💻 Utilisation

Pour lancer le jeu :
```bash
python main.py
```

Pour lancer les tests :
```bash
coverage run -m unittest tests/test_game.py && coverage report -m 
```

## 🧪 Tests

Le projet inclut une suite de tests complète couvrant :
- Validation des entrées
- Feedback des couleurs
- Gestion des lettres répétées
- Scénarios de victoire et défaite

Pour voir les tests en détail, consultez `tests/test_game.py`.

## 🏗 Structure du Projet

```
wordle_project/
├── src/
│   ├── game.py          # Logique principale du jeu
│   ├── word_list.py     # Liste des mots disponibles
├── tests/
│   ├── test_game.py     # Tests unitaires
│   └── __init__.py
├── main.py              # Point d'entrée
└── README.md            # Documentation
```

## 🎯 Règles du Jeu

1. Le jeu choisit aléatoirement un mot de 5 lettres
2. Vous avez 6 tentatives pour deviner le mot
3. Après chaque tentative :
   - Les lettres en vert sont correctes et bien placées
   - Les lettres en jaune sont présentes mais mal placées
   - Les lettres en gris sont absentes du mot
4. Les lettres répétées sont gérées intelligemment :
   - Si une lettre apparaît une seule fois dans le mot cible, seule sa première occurrence sera marquée en jaune
   - Les lettres correctement placées (vertes) sont prioritaires

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- Inspiré par le jeu Wordle original
- Merci à tous les contributeurs

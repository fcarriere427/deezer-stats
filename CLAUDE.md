# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexte

Application web personnelle pour exploiter les données Deezer, hébergée sur Raspberry Pi. Projet d'apprentissage Python avec objectif de qualité professionnelle.

**Utilisateur** : Développeur junior apprenant Python, venant de JavaScript (voir projet Strava pour référence de niveau).

## Stack technique

- **Python 3.13** avec typage strict (mypy)
- **FastAPI** pour l'API REST
- **PostgreSQL** avec SQLAlchemy (ORM)
- **uv** pour les dépendances (moderne, rapide)
- **pytest** pour les tests (objectif coverage > 80%)
- **ruff** pour linting/formatting
- **Docker** pour le déploiement

## Commandes courantes

```bash
# Installation
uv sync --all-extras

# Lancer l'application
uv run deezer serve --reload
# ou directement :
uv run uvicorn deezer_stats.main:app --reload

# Tests
uv run pytest
uv run pytest --cov=src/deezer_stats --cov-report=html

# Linting
uv run ruff check .
uv run ruff format .

# Typage
uv run mypy src/

# Un seul test
uv run pytest tests/test_file.py::test_function -v
```

## Architecture

```
src/deezer_stats/
├── api/            # Routes FastAPI (endpoints)
├── core/           # Config, sécurité, settings
├── db/             # Modèles SQLAlchemy, migrations
├── services/       # Logique métier (Deezer API, etc.)
├── cli.py          # Commandes CLI (Typer)
└── main.py         # Point d'entrée FastAPI
```

## Conventions

- **Langue** : Code et commits en anglais, commentaires explicatifs en français si besoin
- **Typage** : Toutes les fonctions doivent être typées
- **Tests** : Chaque nouvelle feature doit avoir des tests
- **Docstrings** : Format Google pour les fonctions publiques
- **Git** : Branches feature/*, PRs vers develop, commits atomiques

## Workflow Git

1. Créer branche depuis `develop` : `git checkout -b feature/nom-feature`
2. Commits atomiques avec messages clairs
3. PR vers `develop` (même en solo, pour review)
4. Merge après CI verte

## Notes pédagogiques

Ce projet est un outil d'apprentissage. Quand tu proposes du code :
- Explique les concepts Python nouveaux
- Justifie les choix d'architecture
- Propose des alternatives quand pertinent
- Signale les bonnes pratiques Python (vs JavaScript)

Journal d'apprentissage : `C:\Users\florian.carriere\OneDrive - Wavestone\_Florian\01 - Notes\09 - Perso\25-12 - App Deezer\`

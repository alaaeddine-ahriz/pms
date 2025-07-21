#!/bin/bash
"""
Script d'activation de l'environnement Python
Usage: source activate_env.sh
"""

echo "🔧 Activation de l'environnement Python venv-3.12..."

# Vérifier si pyenv est installé
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv n'est pas installé"
    echo "📝 Installez pyenv: https://github.com/pyenv/pyenv#installation"
    return 1
fi

# Vérifier si Python 3.12 est installé
if ! pyenv versions | grep -q "3.12"; then
    echo "❌ Python 3.12 n'est pas installé avec pyenv"
    echo "📝 Installez avec: pyenv install 3.12"
    return 1
fi

# Vérifier si l'environnement virtuel existe
if ! pyenv versions | grep -q "venv-3.12"; then
    echo "⚠️  L'environnement virtuel venv-3.12 n'existe pas"
    echo "📝 Création de l'environnement virtuel..."
    pyenv virtualenv 3.12 venv-3.12
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de la création de l'environnement virtuel"
        return 1
    fi
    echo "✅ Environnement virtuel venv-3.12 créé"
fi

# Activer l'environnement virtuel
echo "🚀 Activation de venv-3.12..."
pyenv activate venv-3.12

if [ $? -eq 0 ]; then
    echo "✅ Environnement venv-3.12 activé"
    echo "🐍 Python version: $(python --version)"
    echo "📦 pip version: $(pip --version)"
    
    # Installer les dépendances si nécessaire
    if [ -f "requirements.txt" ]; then
        echo "📦 Installation des dépendances..."
        pip install -r requirements.txt
    fi
    
    echo ""
    echo "🎉 Prêt pour le développement !"
    echo "🚀 Lancez: python3 start_dev.py"
else
    echo "❌ Erreur lors de l'activation de l'environnement"
    return 1
fi 
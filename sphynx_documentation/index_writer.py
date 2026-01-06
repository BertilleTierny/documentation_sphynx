#!/usr/bin/env python3
"""
Ce script génère un fichier index.rst pour la documentation avec Sphinx.

Ce script parcourt les sous-dossiers .\source\doc_actuarielle et .\source\doc_technique
et génère automatiquement un fichier .\source\index.rst contenant un toctree
référençant tous les fichiers .rst à documenter avec Sphinx.
"""

import os
from pathlib import Path


def get_rst_files(directory: Path) -> list[str]:
    """
    Récupère la liste des fichiers reStructuredText d'un dossier.

    Parcourt le dossier spécifié et retourne les noms (sans extension)
    de tous les fichiers .rst trouvés, triés alphabétiquement.
    Le fichier index.rst est automatiquement exclu s'il existe.

    Args:
        directory: Chemin vers le dossier à analyser. Peut être un chemin
            absolu ou relatif sous forme d'objet Path.

    Returns:
        Liste des noms de fichiers .rst sans leur extension, triés
        alphabétiquement. Retourne une liste vide si le dossier
        n'existe pas ou ne contient aucun fichier .rst.
    """
    if not directory.exists():
        print(f"Le dossier {directory} n'existe pas.")
        return []
    
    rst_files = []
    for file in sorted(directory.glob("*.rst")):
        # On exclut index.rst s'il existe dans le sous-dossier
        if file.stem != "index":
            rst_files.append(file.stem)
    
    return rst_files


def generate_index_content(source_dir: Path) -> str:
    """
    Génère le contenu complet du fichier index.rst.

    Construit un fichier index.rst valide pour Sphinx contenant:
    - Un titre principal "Documentation Complète"
    - Un toctree pour la documentation actuarielle
    - Un toctree pour la documentation technique

    Args:
        source_dir: Chemin vers le dossier 'source' du projet Sphinx.
            Ce dossier doit contenir les sous-dossiers 'doc_actuarielle'
            et 'doc_technique'.

    Returns:
        Chaîne de caractères contenant le contenu RST complet,
        prêt à être écrit dans un fichier.
    """
    
    # Définir les chemins
    doc_actuarielle_dir = source_dir / "doc_actuarielle"
    doc_technique_dir = source_dir / "doc_technique"
    
    # Récupérer les fichiers .rst de chaque dossier
    actuarielle_files = get_rst_files(doc_actuarielle_dir)
    technique_files = get_rst_files(doc_technique_dir)
    
    # Construire l'en-tête du fichier index.rst
    content = """Documentation Complète
======================

.. toctree::
    :maxdepth: 2
    :caption: Documentation Actuarielle
    :numbered:                                

"""
    
    # Ajouter les entrées pour la documentation actuarielle
    for filename in actuarielle_files:
        content += f"   doc_actuarielle/{filename}\n"
    
    # Ajouter la section documentation technique
    content += """
.. toctree::
    :maxdepth: 2
    :caption: Documentation Technique
                                  

"""
    
    # Ajouter les entrées pour la documentation technique
    for filename in technique_files:
        content += f"   doc_technique/{filename}\n"
    
    return content


def main()-> None:
    """
    Point d'entrée principal du script.

    Orchestre la génération du fichier index.rst:
    1. Vérifie l'existence du dossier source
    2. Génère le contenu du fichier index.rst
    3. Écrit le fichier sur le disque
    4. Affiche un récapitulatif à l'utilisateur
    """
    # Configuration du chemin du dossier source
    # Par défaut: relatif au répertoire d'exécution
    source_dir = Path("source")
    
    # Alternative: chemin absolu (décommenter si nécessaire)
    # source_dir = Path("/chemin/vers/votre/projet/source")
    
    # Vérification de l'existence du dossier source
    if not source_dir.exists():
        print(f"Le dossier source '{source_dir}' n'existe pas.")
        print("   Vérifiez que vous exécutez le script depuis le bon répertoire.")
        return
    
    # Génération du contenu RST
    index_content = generate_index_content(source_dir)
    
    # Écriture du fichier index.rst
    index_path = source_dir / "index.rst"
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    # Affichage du résultat
    print(f"Fichier {index_path} généré avec succès !")
    print("\nContenu généré :")
    print("-" * 40)
    print(index_content)


if __name__ == "__main__":
    main()
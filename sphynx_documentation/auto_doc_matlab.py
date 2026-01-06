"""
Ce module permet de générer automatiquement un fichier reStructuredText (.rst)
décrivant l'arborescence de dossiers contenant des fichiers MATLAB (.m).
Il est conçu pour s'intégrer avec Sphinx et l'extension sphinxcontrib-matlabdomain.
"""

import os

def has_m_files(folder_path: str) -> bool:
        """
        Vérifie si un dossier contient des fichiers MATLAB.

        Args:
            folder_path: Chemin vers le dossier à analyser.

        Returns:
            True si le dossier contient au moins un fichier .m, False sinon.
            Retourne False en cas d'erreur d'accès au dossier.
        """
        try:
            return any(f.endswith('.m') for f in os.listdir(folder_path))
        except:
            return False


def find_leaf_folders(root_path: str, current_path: str = "") -> dict:
    """
    Parcourt l'arborescence du dossier et des sous-dossiers pour identifier 
    les fichiers MATLAB (.m) à documenter.

    Construit une structure de dictionnaires imbriqués représentant
    la hiérarchie des dossiers. Trois types de dossiers sont identifiés:
    - "LEAF": dossier terminal contenant uniquement des fichiers .m
    - Dict avec "__functions__": dossier mixte (fichiers .m + sous-dossiers)
    - Dict sans "__functions__": dossier parent (sous-dossiers uniquement)

    Args:
        root_path: Chemin absolu du dossier à explorer.
        current_path: Ne pas spécifier lors de l'appel initial.

    Returns:
        Dictionnaire représentant la structure hiérarchique.
        Les clés sont les noms de dossiers.
    """
    structure = {}
    
    try:
        items = os.listdir(root_path)
    except:
        return structure
    
    # Trier alphabétiquement les éléments 
    folders = sorted([
        item for item in items 
        if os.path.isdir(os.path.join(root_path, item))
        ])
    
    for folder in folders:
        folder_path = os.path.join(root_path, folder)
        
        # Explorer récursivement les sous-dossiers
        sub_structure = find_leaf_folders(
            folder_path, 
            os.path.join(current_path, folder) if current_path else folder
            )
        
        # Vérifier si ce dossier contient des fichiers matlab (.m)
        has_m = has_m_files(folder_path)
        
        if has_m and sub_structure:
            # Dossier mixte : contient des .m ET des sous-dossiers
            structure[folder] = {"__functions__": "LEAF", **sub_structure}
        elif has_m:
            # Dossier terminal : contient seulement des .m
            structure[folder] = "LEAF"
        elif sub_structure:
            # Dossier parent : contient seulement des sous-dossiers
            structure[folder] = sub_structure
                    
    return structure


def generate_rst_content(structure: dict,
        level: int = 0,
        parent_path: str = ""
        ) -> list[str]:
    """
    Génère le fichier .rst indiquant la structure des dossiers
    à documenter.
    
    Args:
        structure: Dictionnaire de la structure des dossiers (issu de
            find_leaf_folders).
        level: Niveau de profondeur (0 pour le dossier racine).
        parent_path: Chemin du dossier parent en notatation pointée
            suivant le format Dossier.Sous_dossier (ex: "Audit.Test")
    """
    content = []
    underline_chars = ['=', '-', '~', '^', '+', '*', '#']
    
    for folder_name, sub_content in structure.items():
        # Construire le chemin complet pour automodule
        if parent_path:
            full_module_path = f"{parent_path}.{folder_name}"
        else:
            full_module_path = folder_name
        
        # Ajouter le titre (nom du dossier) avec le soulignement approprié
        content.append(folder_name)
        underline_char = underline_chars[min(level, len(underline_chars)-1)]
        content.append(underline_char * len(folder_name))
        content.append("")
        
        if sub_content == "LEAF":
            # Dossier terminal avec des fonctions .m
            # La directive automodule est indiquée pour documenter les fonctions locales
            content.append(f".. automodule:: {full_module_path}")
            content.append("   :members:")
            content.append("")
        elif isinstance(sub_content, dict) and "__functions__" in sub_content:
            # Dossier mixte : documenter les fonctions locales puis les sous-dossiers
            content.append(f".. automodule:: {full_module_path}")
            content.append("   :members:")
            content.append("")
            
            # Traiter les sous-dossiers (exclure __functions__)
            sub_dict = {k: v for k, v in sub_content.items() if k != "__functions__"}
            if sub_dict:
                sub_rst = generate_rst_content(sub_dict, level + 1, full_module_path)
                content.extend(sub_rst)
        else:
            # Dossier parent, traiter récursivement les sous-dossiers
            sub_rst = generate_rst_content(sub_content, level + 1, full_module_path)
            content.extend(sub_rst)
    
    return content

def generate_hierarchical_rst(code_folder_path: str, output_file: str = "documentation.rst") -> None:
    """
    Génère un fichier RST documentant la hiérarchie complète d'un projet MATLAB.

    Parcourt l'arborescence de dossiers à partir du chemin spécifié,
    identifie les dossiers contenant des fichiers .m, et génère un fichier RST
    structuré avec les directives automodule appropriées pour l'extension sphinxcontrib-matlabdomain.

    Args:
        code_folder_path: Chemin vers le dossier racine du code.
        output_file: Nom du fichier RST de sortie. Par défaut "documentation.rst".
    """
        
    # Vérifier que le dossier racine du code existe
    if not os.path.exists(code_folder_path):
        print(f"Erreur: Le dossier {code_folder_path} n'existe pas")
        return
    
    # Phase 1: Analyser la structure du dossier racine
    print("Analyse de la structure des dossiers...")
    folder_structure = find_leaf_folders(code_folder_path)
    
    if not folder_structure:
        print("Aucun dossier contenant des fichiers .m trouvé")
        return
    
    # Phase 2: Générer le contenu du fichier .rst indiquant les dossiers à documenter
    rst_content = []
    # Ajouter la structure hierarchique des dossiers à documenter
    hierarchical_content = generate_rst_content(folder_structure)
    rst_content.extend(hierarchical_content)
    
    # Phase 3: Écriture du fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rst_content))
    
    print(f"Fichier {output_file} généré avec succès!")
    print("Structure détectée:")
    print_structure(folder_structure)

def print_structure(structure: dict, indent: int = 0) -> None:
    """
    Affiche la structure des dossiers de manière lisible dans la console.

    Utilisé pour vérifier visuellement la structure détectée après
    l'analyse des dossiers.

    Args:
        structure: Dictionnaire de la structure à afficher.
        indent: Niveau d'indentation actuel (usage interne pour la récursion).
    """
    for name, content in structure.items():
        print("  " * indent + f"- {name}")
        if content != "LEAF":
            print_structure(content, indent + 1)
        else:
            print("  " * (indent + 1) + "(contient des fichiers .m)")


# Point d'entrée pour l'execution du code
if __name__ == "__main__":

    # Chemin vers le dossier racine du code MATLAB à documenter
    code_path = r"C:\Projets\Interne\MAIF\Documentation_Git_Versioning\documentation_sphynx\demo_code" 

    # Chemin vers le dossier où enregistrer le fichier RST généré
    output_path = r"C:\Projets\Interne\MAIF\Documentation_Git_Versioning\documentation_sphynx\sphynx_documentation\source\documentation_hierarchique.rst"

    # Générer le fichier RST documentant la hiérarchie du projet MATLAB
    generate_hierarchical_rst(code_path, output_path)

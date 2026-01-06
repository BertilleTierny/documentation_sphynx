import os

def generate_hierarchical_rst(code_folder_path, output_file="documentation.rst"):
    """
    Génère un fichier .rst avec hiérarchie complète des dossiers
    
    Args:
        code_folder_path (str): Chemin vers le dossier 'Code'
        output_file (str): Nom du fichier de sortie .rst
    """
    
    def has_m_files(folder_path):
        """Vérifie si un dossier contient des fichiers .m"""
        try:
            return any(f.endswith('.m') for f in os.listdir(folder_path))
        except:
            return False
    
    

    def find_leaf_folders(root_path, current_path=""):
        """
        Trouve récursivement tous les dossiers contenant des fichiers .m
        Retourne: dict avec structure hiérarchique
        """
        structure = {}
        
        try:
            items = os.listdir(root_path)
        except:
            return structure
        
        # Trier les éléments
        folders = sorted([item for item in items if os.path.isdir(os.path.join(root_path, item))])
        
        for folder in folders:
            folder_path = os.path.join(root_path, folder)
            
            # Explorer récursivement d'abord
            sub_structure = find_leaf_folders(folder_path, 
                                            os.path.join(current_path, folder) if current_path else folder)
            
            # Vérifier si ce dossier contient des .m
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

    
    def generate_rst_content(structure, level=0, parent_path=""):
        """
        Génère le contenu RST récursivement avec notation hiérarchique
        
        Args:
            structure: Structure des dossiers
            level: Niveau de profondeur pour les titres
            parent_path: Chemin parent pour la notation (ex: "Audit.Test")
        """
        content = []
        underline_chars = ['=', '-', '~', '^', '+', '*', '#']
        
        for folder_name, sub_content in structure.items():
            # Construire le chemin complet pour automodule
            if parent_path:
                full_module_path = f"{parent_path}.{folder_name}"
            else:
                full_module_path = folder_name
            
            # Ajouter le titre (nom simple du dossier)
            content.append(folder_name)
            underline_char = underline_chars[min(level, len(underline_chars)-1)]
            content.append(underline_char * len(folder_name))
            content.append("")
            
            if sub_content == "LEAF":
                # Dossier terminal avec des fonctions .m
                content.append(f".. automodule:: {full_module_path}")
                content.append("   :members:")
                content.append("")
            elif isinstance(sub_content, dict) and "__functions__" in sub_content:
                # Dossier mixte : documenter les fonctions puis les sous-dossiers
                content.append(f".. automodule:: {full_module_path}")
                content.append("   :members:")
                content.append("")
                
                # Traiter les sous-dossiers (exclure __functions__)
                sub_dict = {k: v for k, v in sub_content.items() if k != "__functions__"}
                if sub_dict:
                    sub_rst = generate_rst_content(sub_dict, level + 1, full_module_path)
                    content.extend(sub_rst)
            else:
                # Dossier parent, traiter récursivement
                sub_rst = generate_rst_content(sub_content, level + 1, full_module_path)
                content.extend(sub_rst)
        
        return content

        
    # Vérifier que le dossier existe
    if not os.path.exists(code_folder_path):
        print(f"Erreur: Le dossier {code_folder_path} n'existe pas")
        return
    
    # Analyser la structure
    print("Analyse de la structure des dossiers...")
    folder_structure = find_leaf_folders(code_folder_path)
    
    if not folder_structure:
        print("Aucun dossier contenant des fichiers .m trouvé")
        return
    
    # Générer le contenu RST
    rst_content = [
        # "Documentation technique",
        # # "=" * 37,
        # "",
        # "Cette section documente automatiquement tout le code MATLAB.",
        # ""
    ]
    
    # Ajouter le contenu hiérarchique
    hierarchical_content = generate_rst_content(folder_structure)
    rst_content.extend(hierarchical_content)
    
    # Écrire le fichier
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rst_content))
    
    print(f"Fichier {output_file} généré avec succès!")
    print("Structure détectée:")
    print_structure(folder_structure)

def print_structure(structure, indent=0):
    """Affiche la structure détectée pour vérification"""
    for name, content in structure.items():
        print("  " * indent + f"- {name}")
        if content != "LEAF":
            print_structure(content, indent + 1)
        else:
            print("  " * (indent + 1) + "(contient des fichiers .m)")


if __name__ == "__main__":
    code_path = r"C:\Projets\Interne\MAIF\vscode_demo" 
    output_path= r"C:\Projets\Interne\MAIF\vscode_demo\sphynx_documentation\source\documentation_hierarchique.rst"
    generate_hierarchical_rst(code_path, output_path)
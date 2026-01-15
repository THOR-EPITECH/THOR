"""
Script pour nettoyer le projet en supprimant les fichiers inutiles.
"""
import os
import shutil
from pathlib import Path

def clean_pycache():
    """Supprime tous les dossiers __pycache__."""
    removed = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = Path(root) / '__pycache__'
            shutil.rmtree(pycache_path)
            removed.append(str(pycache_path))
    return removed

def clean_temp_files():
    """Supprime les fichiers temporaires."""
    patterns = ['.DS_Store', '*.pyc', '*.py~', '*~', '.pytest_cache']
    removed = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = Path(root) / file
            if any(file_path.match(pattern) for pattern in patterns):
                file_path.unlink()
                removed.append(str(file_path))
    
    # Supprime aussi les dossiers de cache pytest
    for root, dirs, files in os.walk('.'):
        if '.pytest_cache' in dirs:
            cache_path = Path(root) / '.pytest_cache'
            shutil.rmtree(cache_path)
            removed.append(str(cache_path))
    
    return removed

def clean_empty_dirs():
    """Supprime les dossiers vides (sauf ceux importants)."""
    important_dirs = {'.git', 'src', 'data', 'configs', 'scripts', 'docs', 'results', 'models'}
    removed = []
    
    for root, dirs, files in os.walk('.', topdown=False):
        root_path = Path(root)
        
        # Ignore les dossiers importants
        if any(important in root_path.parts for important in important_dirs):
            continue
        
        # Supprime si vide
        if not dirs and not files and root_path.exists():
            try:
                root_path.rmdir()
                removed.append(str(root_path))
            except OSError:
                pass
    
    return removed

def clean_test_results():
    """Supprime les fichiers de résultats de test individuels (garde les rapports)."""
    removed = []
    
    # Fichiers JSON de test individuels dans results/pipeline
    pipeline_dir = Path('results/pipeline')
    if pipeline_dir.exists():
        for file in pipeline_dir.glob('sample_*_result.json'):
            # Garde les rapports .md mais supprime les JSON de test individuels
            # (on peut les régénérer)
            file.unlink()
            removed.append(str(file))
    
    # Fichiers JSON de test dans results/
    for file in Path('results').glob('*_test.json'):
        file.unlink()
        removed.append(str(file))
    
    return removed

def main():
    """Point d'entrée principal."""
    print("🧹 Nettoyage du projet...\n")
    
    # Nettoie __pycache__
    print("1. Suppression des dossiers __pycache__...")
    pycache = clean_pycache()
    print(f"   ✅ {len(pycache)} dossiers supprimés")
    
    # Nettoie les fichiers temporaires
    print("\n2. Suppression des fichiers temporaires...")
    temp_files = clean_temp_files()
    print(f"   ✅ {len(temp_files)} fichiers supprimés")
    
    # Nettoie les dossiers vides
    print("\n3. Suppression des dossiers vides...")
    empty_dirs = clean_empty_dirs()
    print(f"   ✅ {len(empty_dirs)} dossiers supprimés")
    
    # Nettoie les résultats de test individuels
    print("\n4. Suppression des fichiers de test individuels...")
    test_results = clean_test_results()
    print(f"   ✅ {len(test_results)} fichiers supprimés")
    
    print(f"\n✨ Nettoyage terminé !")
    print(f"   - {len(pycache)} dossiers __pycache__")
    print(f"   - {len(temp_files)} fichiers temporaires")
    print(f"   - {len(empty_dirs)} dossiers vides")
    print(f"   - {len(test_results)} fichiers de test")

if __name__ == "__main__":
    main()



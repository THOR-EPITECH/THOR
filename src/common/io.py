"""
Utilitaires pour la lecture/écriture de fichiers.
"""
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Iterator
import pandas as pd


def read_jsonl(file_path: str | Path) -> Iterator[Dict[str, Any]]:
    """
    Lit un fichier JSONL ligne par ligne.
    
    Args:
        file_path: Chemin vers le fichier JSONL
    
    Yields:
        Dictionnaire pour chaque ligne
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(file_path: str | Path, data: List[Dict[str, Any]]):
    """
    Écrit un fichier JSONL.
    
    Args:
        file_path: Chemin vers le fichier de sortie
        data: Liste de dictionnaires à écrire
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def write_csv(file_path: str | Path, data: List[Dict[str, Any]]):
    """
    Écrit un fichier CSV.
    
    Args:
        file_path: Chemin vers le fichier de sortie
        data: Liste de dictionnaires à écrire
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not data:
        return
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8')


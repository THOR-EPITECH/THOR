"""
Configuration du logging unifié pour l'application THOR.

Ce module fournit une fonction utilitaire pour configurer de manière cohérente
le logging dans tous les modules de l'application.
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    module: Optional[str] = None
) -> logging.Logger:
    """
    Configure et retourne un logger Python standard.
    
    Le logger est configuré avec:
    - Un formatter avec timestamp
    - Un handler console (stdout)
    - Un handler fichier optionnel
    - Prévention des handlers dupliqués
    
    Args:
        level (str, optional): Niveau de log. Valeurs: DEBUG, INFO, WARNING, ERROR, CRITICAL.
            Par défaut "INFO".
        log_file (Optional[str], optional): Chemin vers le fichier de log. Si fourni, les logs
            seront également écrits dans ce fichier.
        module (Optional[str], optional): Nom du module pour identifier le logger.
            Si None, utilise "thor" comme nom par défaut.
    
    Returns:
        logging.Logger: Instance de logger configurée.
        
    Example:
        >>> logger = setup_logging(level="DEBUG", module="pathfinding")
        >>> logger.info("Recherche d'itinéraire en cours...")
        >>> logger.error("Aucun chemin trouvé")
    """
    logger_name = module or "thor"
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


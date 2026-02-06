"""
Gestion de la configuration via YAML et variables d'environnement.

Ce module fournit une classe Config pour gérer la configuration hiérarchique
de l'application THOR avec support de fichiers YAML et variables d'environnement.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """
    Gestionnaire de configuration hiérarchique.
    
    Cette classe permet de charger et fusionner des configurations depuis plusieurs sources:
    - Fichier de configuration de base (configs/base.yaml)
    - Fichier de configuration spécifique (optionnel)
    - Dictionnaire d'overrides
    - Variables d'environnement
    
    Attributes:
        config (Dict[str, Any]): Dictionnaire contenant la configuration complète.
        
    Example:
        >>> config = Config("configs/production.yaml")
        >>> api_key = config.get("api.key", "default_key")
        >>> db_host = config["database"]["host"]
    """
    
    def __init__(self, config_path: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None):
        """
        Initialise et charge la configuration depuis plusieurs sources.
        
        Args:
            config_path (Optional[str]): Chemin vers le fichier YAML de configuration spécifique.
                Si None, seule la configuration de base est chargée.
            overrides (Optional[Dict[str, Any]]): Dictionnaire pour surcharger des valeurs
                de configuration. Ces valeurs ont la priorité la plus élevée.
                
        Note:
            L'ordre de priorité est: overrides > config_path > base.yaml > env vars
        """
        # Charge les variables d'environnement
        load_dotenv()
        
        # Charge la config de base
        base_config_path = Path(__file__).parent.parent.parent / "configs" / "base.yaml"
        self.config = self._load_yaml(base_config_path) if base_config_path.exists() else {}
        
        # Charge la config spécifique si fournie
        if config_path:
            specific_config = self._load_yaml(config_path)
            self.config = self._merge_config(self.config, specific_config)
        
        # Applique les overrides
        if overrides:
            self.config = self._merge_config(self.config, overrides)
        
        # Remplace les variables d'environnement
        self.config = self._replace_env_vars(self.config)
    
    @staticmethod
    def _load_yaml(path: str | Path) -> Dict[str, Any]:
        """
        Charge et parse un fichier YAML.
        
        Args:
            path (str | Path): Chemin vers le fichier YAML.
            
        Returns:
            Dict[str, Any]: Contenu du fichier YAML parsé.
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
            yaml.YAMLError: Si le fichier YAML est mal formaté.
        """
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    @staticmethod
    def _merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fusionne récursivement deux configurations.
        
        Les valeurs de 'override' écrasent celles de 'base'. Pour les dictionnaires imbriqués,
        la fusion est récursive.
        
        Args:
            base (Dict[str, Any]): Configuration de base.
            override (Dict[str, Any]): Configuration à fusionner (prioritaire).
            
        Returns:
            Dict[str, Any]: Configuration fusionnée.
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remplace récursivement les références aux variables d'environnement.
        
        Les chaînes au format ${VAR_NAME} sont remplacées par la valeur de la variable
        d'environnement correspondante.
        
        Args:
            config (Dict[str, Any]): Configuration contenant potentiellement des références.
            
        Returns:
            Dict[str, Any]: Configuration avec variables d'environnement résolues.
            
        Example:
            >>> os.environ["API_KEY"] = "secret123"
            >>> config = {"api": {"key": "${API_KEY}"}}
            >>> Config._replace_env_vars(config)
            {'api': {'key': 'secret123'}}
        """
        if isinstance(config, dict):
            return {k: Config._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [Config._replace_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            var_name = config[2:-1]
            return os.getenv(var_name, config)
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration avec support de clés imbriquées.
        
        Les clés imbriquées peuvent être accédées avec la notation pointée (ex: "api.key").
        
        Args:
            key (str): Clé de configuration, peut être imbriquée avec des points.
            default (Any, optional): Valeur par défaut si la clé n'existe pas.
            
        Returns:
            Any: Valeur de configuration ou valeur par défaut.
            
        Example:
            >>> config.get("database.host", "localhost")
            'localhost'
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def __getitem__(self, key: str) -> Any:
        """
        Accès direct à la configuration via l'opérateur [].
        
        Args:
            key (str): Clé de configuration.
            
        Returns:
            Any: Valeur de configuration.
            
        Raises:
            KeyError: Si la clé n'existe pas.
        """
        return self.config[key]
    
    def __contains__(self, key: str) -> bool:
        """
        Vérifie si une clé existe dans la configuration.
        
        Args:
            key (str): Clé à vérifier.
            
        Returns:
            bool: True si la clé existe, False sinon.
        """
        return key in self.config


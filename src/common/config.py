"""
Gestion de la configuration via YAML et variables d'environnement.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Gestionnaire de configuration hiérarchique."""
    
    def __init__(self, config_path: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None):
        """
        Charge la configuration.
        
        Args:
            config_path: Chemin vers le fichier YAML de configuration
            overrides: Dictionnaire pour override des valeurs
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
        """Charge un fichier YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    @staticmethod
    def _merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Fusionne deux configurations (override prend le dessus)."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        """Remplace les références ${VAR} par les variables d'environnement."""
        if isinstance(config, dict):
            return {k: Config._replace_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [Config._replace_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            var_name = config[2:-1]
            return os.getenv(var_name, config)
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration (supporte les clés imbriquées avec '.')."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def __getitem__(self, key: str) -> Any:
        """Accès direct à la configuration."""
        return self.config[key]
    
    def __contains__(self, key: str) -> bool:
        """Vérifie si une clé existe."""
        return key in self.config


"""
Utilitaires NLP partagés.

Fonction principale: ensure_origin_destination_distinct
Assure que origin et destination ne sont pas identiques (cas-insensible).
Si elles sont identiques, on considère que l'extraction manque d'information et on
met destination à None (on pourrait aussi décider l'inverse selon contexte).
"""
from typing import Optional, Tuple


def ensure_origin_destination_distinct(origin: Optional[str], destination: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Assure que origin et destination sont différentes.

    - Si origin et destination sont strictement identiques (après strip et lower),
      on garde origin et on vide destination (destination=None) car l'utilisateur a
      probablement mentionné une seule ville.
    - Si l'un est None, retourne tels quels.
    - Retourne un tuple (origin, destination) normalisé.
    """
    if not origin or not destination:
        return origin, destination

    o_norm = origin.strip().lower()
    d_norm = destination.strip().lower()
    if o_norm == d_norm:
        # On considère que la phrase ne contient qu'une ville; évite d'assigner la même ville aux deux rôles
        return origin, None

    return origin, destination


"""
CLI pour le module Pathfinding.
"""
import argparse
from pathlib import Path
from src.common.config import Config
from src.common.logging import setup_logging
from src.pathfinding.eval.evaluate import evaluate_model

logger = setup_logging(module="cli.pathfinding")


def load_model(model_name: str, config: Config) -> "PathfindingModel":
    """Charge un modèle Pathfinding."""
    if model_name == "dijkstra":
        from src.pathfinding.models.dijkstra import DijkstraPathfindingModel
        pathfinding_config = config.get("pathfinding", {})
        return DijkstraPathfindingModel({
            "path_gares": pathfinding_config.get("path_gares", "data/train_station/dataset_gares.json"),
            "path_liaisons": pathfinding_config.get("path_liaisons", "data/train_station/dataset_liaisons.json")
        })
    else:
        raise ValueError(f"Unknown model: {model_name}. Available: dijkstra")


def find_route_command(args):
    """Commande pour trouver un itinéraire."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    logger.info(f"Finding route from {args.origin} to {args.destination} with {args.model}")
    result = model.find_route(args.origin, args.destination)
    
    if result.steps:
        print(f"\n=== Itinéraire trouvé ===")
        print(f"Origine: {result.origin}")
        print(f"Destination: {result.destination}")
        print(f"Distance: {result.total_distance:.2f} km" if result.total_distance else "Distance: N/A")
        print(f"Nombre d'étapes: {len(result.steps)}")
        print("\nÉtapes:")
        for i, step in enumerate(result.steps, 1):
            print(f"  {i}. {step}")
    else:
        print(f"\n❌ Aucun itinéraire trouvé")
        if result.metadata.get("error"):
            print(f"Erreur: {result.metadata['error']}")


def evaluate_command(args):
    """Commande pour évaluer un modèle."""
    config = Config(args.config) if args.config else Config()
    model = load_model(args.model, config)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Evaluating {args.model} on {args.dataset}")
    metrics = evaluate_model(model, args.dataset, output_dir)
    
    print("\n=== Metrics ===")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="THOR Pathfinding CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commande find-route
    find_parser = subparsers.add_parser("find-route", help="Find a route between two cities")
    find_parser.add_argument("--origin", required=True, help="Origin city")
    find_parser.add_argument("--destination", required=True, help="Destination city")
    find_parser.add_argument("--model", default="dijkstra", help="Pathfinding model to use")
    find_parser.add_argument("--config", help="Path to config file")
    
    # Commande evaluate
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a model")
    eval_parser.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    eval_parser.add_argument("--model", default="dijkstra", help="Pathfinding model to use")
    eval_parser.add_argument("--config", help="Path to config file")
    eval_parser.add_argument("--output-dir", default="results/pathfinding", help="Output directory")
    
    args = parser.parse_args()
    
    if args.command == "find-route":
        find_route_command(args)
    elif args.command == "evaluate":
        evaluate_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

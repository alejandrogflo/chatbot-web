import argparse
import json
import sys

from seminario_chatbot.ai.graph import graph_mermaid, run_chat


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consulta el catálogo de películas y videojuegos con LangGraph."
    )
    parser.add_argument("question", nargs="?", help="Pregunta en español")
    parser.add_argument(
        "--show-graph",
        action="store_true",
        help="Imprime el diagrama Mermaid del workflow sin llamar a la IA.",
    )
    args = parser.parse_args()

    if args.show_graph:
        print(graph_mermaid())
        return 0
    if not args.question:
        parser.print_help()
        return 2

    try:
        result = run_chat(args.question)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception:
        print(
            "No se pudo iniciar el workflow. Revisa las variables de .env y las dependencias.",
            file=sys.stderr,
        )
        return 1

    print("\nRespuesta\n---------")
    print(result.get("answer", "No se produjo una respuesta."))
    if result.get("plan"):
        print("\nPlan de consulta")
        print(json.dumps(result["plan"], ensure_ascii=False, indent=2))
    print("\nEvaluación")
    print(json.dumps(result.get("evaluation", {}), ensure_ascii=False, indent=2))
    print("\nTraza del grafo")
    print(json.dumps(result.get("trace", []), ensure_ascii=False, indent=2))
    if result.get("error_message"):
        print(f"\nNota: {result['error_message']}")
    print(
        "\nConsumo académico: "
        f"{result.get('tokens_palabras', 0)} palabras/token(s); "
        f"Groq reportó {result.get('tokens_proveedor', 0)} token(s) reales."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

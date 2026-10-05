import json
from pathlib import Path
from typing import Any

from seminario_chatbot.ai.planner import extract_query_plan
from seminario_chatbot.database import normalize_genre


CASES_PATH = Path(__file__).resolve().parents[3] / "data" / "ai_eval_cases.jsonl"


def _normalize(field: str, value: Any) -> Any:
    if field == "genero" and isinstance(value, str):
        return (normalize_genre(value) or "").casefold()
    if isinstance(value, str):
        return value.strip().casefold()
    return value


def _matches(actual: Any, expected: Any, field: str) -> bool:
    if field in {"calificacion_minima", "calificacion_maxima"}:
        if actual is None or expected is None:
            return actual is expected
        return abs(float(actual) - float(expected)) < 0.001
    return _normalize(field, actual) == _normalize(field, expected)


def load_cases() -> list[dict[str, Any]]:
    with CASES_PATH.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]


def evaluate_cases() -> tuple[int, int]:
    cases = load_cases()
    passed = 0
    for index, case in enumerate(cases, start=1):
        plan, _usage = extract_query_plan(case["question"])
        actual = plan.model_dump()
        differences = {
            field: {"expected": expected, "actual": actual.get(field)}
            for field, expected in case["expected"].items()
            if not _matches(actual.get(field), expected, field)
        }
        is_pass = not differences
        passed += int(is_pass)
        mark = "PASS" if is_pass else "FAIL"
        print(f"[{mark}] {index}. {case['question']}")
        if differences:
            print(json.dumps(differences, ensure_ascii=False, indent=2))
    return passed, len(cases)


def main() -> int:
    try:
        passed, total = evaluate_cases()
    except Exception as exc:
        print(
            f"No se pudo ejecutar la evaluación ({type(exc).__name__}). "
            "Revisa GROQ_API_KEY y la disponibilidad del proveedor."
        )
        return 2
    print(f"Resultado del planificador: {passed}/{total} casos correctos.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())

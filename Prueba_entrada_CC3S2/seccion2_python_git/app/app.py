# Implementa la función summarize y el CLI.
# Requisitos:
# - summarize(nums) -> dict con claves: count, sum, avg
# - Valida que nums sea lista no vacía y elementos numéricos (acepta strings convertibles a float).
# - CLI: python -m app "1,2,3" imprime: sum=6.0 avg=2.0 count=3


def summarize(nums):  # TODO: tipado opcional
    if not nums:
        raise ValueError("La lista nums no pede ser vacia")

    numeros = []
    for item in nums:
        try:
            numeros.append(float(item))
        except:
            raise ValueError(f"La lista nums contiene un elemento no numerico: {item}")
    count = len(numeros)
    total = sum(numeros)
    avg = total / count
    return {"count": count, "sum": sum, "avg": avg}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: Debes proporcionar numeros separados por comas")
        print('Ejm: python -m app "1,2,3"')
    # input_string = sys.argv[1]

    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    items = [p.strip() for p in raw.split(",") if p.strip()]
    try:
        result = summarize(items)
        print(f"sum={result['sum']} avg={result['avg']} count={result['count']}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

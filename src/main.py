from src.graph import graph


initial_state = {
    "task": """
    Criar uma API REST de gerenciamento de pedidos.

    A API deve permitir criar, consultar e cancelar pedidos.
    Um pedido possui itens e deve possuir um valor total.
    """,

    "iteration": 0,
    "status": "STARTED",
}


result = graph.invoke(initial_state)


print()
print("Workflow finalizado.")
print()

print("Requirements:")
print(result["requirements"].model_dump_json(indent=2))

print()
print("Architecture:")
print(result["architecture"].model_dump_json(indent=2))

print()
print("Implementation:")
print(result["implementation"].model_dump_json(indent=2))
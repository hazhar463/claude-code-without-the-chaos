from quote import total_cents


def execute_plan(actions):
    if type(actions) is not list or not 1 <= len(actions) <= 5:
        raise ValueError("Supply one to five actions")
    results = []
    for action in actions:
        if type(action) is not dict:
            raise TypeError("Each action must be an object")
        if set(action) != {"tool", "arguments"}:
            raise ValueError("Unexpected action fields")
        if action["tool"] != "calculate_total":
            raise ValueError("Tool is not allowed")
        arguments = action["arguments"]
        if type(arguments) is not dict:
            raise TypeError("Arguments must be an object")
        if set(arguments) != {"unit_cents", "quantity"}:
            raise ValueError("Unexpected argument fields")
        results.append(total_cents(**arguments))
    return results

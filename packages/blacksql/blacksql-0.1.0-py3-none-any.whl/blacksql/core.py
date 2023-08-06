def statements(sql):
    return [statement.strip() for statement in sql.split("\n\n")]


def tokenize(statement):
    for c in "(),;-+/=":
        statement = statement.replace(f"{c}", f" {c} ")
    statement = statement.lower()
    return statement.split()


def indent(statement):
    stack = []
    output = []
    LEVEL = "  "

    def newline():
        output.append("\n" + (LEVEL * len(stack)))

    top = (
        "select",
        "from",
        "insert",
        "update",
        "delete",
        "group",
        "order",
        "where",
        "create",
        "output",
    )
    for word in tokenize(statement):
        if word in top:
            while stack and stack[-1] != "(":
                stack.pop(-1)
            stack.append(word)
            newline()
        if word == "(":
            stack.append(word)
        if word in ("left", "right"):
            newline()
            output[-1] += LEVEL
        if word == ")" and "(" in stack:
            while stack and stack[-1] != "(":
                stack.pop(-1)
            if stack:
                stack.pop(-1)
        # ------
        output.append(word)
        # ------
        if word == ",":
            newline()
            output[-1] += LEVEL
    return " ".join(output)


def format(sql):
    output = []
    for statement in statements(sql):
        output.append(indent(statement))
    return "\n".join(output)

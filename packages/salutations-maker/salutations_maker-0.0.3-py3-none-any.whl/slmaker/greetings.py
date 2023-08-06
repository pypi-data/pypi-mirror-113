def say_hello(name: str, language: str) -> None:
    """A simple helper to say hello

    Args:
        name (str): The name to greet
        language (str): The language to greet name with

    Raises:
        Exception: Exeception raised if the language isn't implemented yet
    """
    if language=="FR":
        print(f"Bonjour {name}")

    elif language=="NL":
        print(f"Dag {name}")

    elif language=="EN":
        print(f"Hello {name}")

    else:
        raise Exception("You didn't inputed known language")
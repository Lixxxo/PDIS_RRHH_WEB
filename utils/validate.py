
def validate_run(rut):
    from itertools import cycle

    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revert = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revert, factors))
    res = (-s) % 11

    if str(res) == dv:
        return f"{aux}-{dv}"
    elif dv == "K" and res == 10:
        return f"{aux}-{dv}"
    else:
        return False

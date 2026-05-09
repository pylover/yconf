

def _list(l, indent, indentsize):
    for v in l:
        yield f'{" " * indent}- {v}'

    else:
        yield ''


def _dict(d, indent, indentsize):
    for k, v in d.items():
        yield f'{" " * indent}{k}: {v}'

    else:
        yield ''


def _dump(obj, indent, indentsize):
    if isinstance(obj, list):
        return _list(obj, indent, indentsize)

    if isinstance(obj, dict):
        return _dict(obj, indent, indentsize)

    return str(obj)


def dumps(obj, indent=0, indentsize=2):
    return '\n'.join(_dump(obj, indent, indentsize))



def _list(lst, indent, indentsize):
    for v in lst:
        if isinstance(v, (dict, list)):
            yield f'{" " * indent}-'
            yield from _dump(v, indent + indentsize, indentsize)
        else:
            yield f'{" " * indent}- {v}'


def _dict(d, indent, indentsize):
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            yield f'{" " * indent}{k}:'
            yield from _dump(v, indent + indentsize, indentsize)
        else:
            yield f'{" " * indent}{k}: {v}'


def _dump(obj, indent, indentsize):
    if isinstance(obj, list):
        yield from _list(obj, indent, indentsize)

    if isinstance(obj, dict):
        yield from _dict(obj, indent, indentsize)

    return str(obj)


def dumps(obj, indent=0, indentsize=2):
    out = list(_dump(obj, indent, indentsize))
    if out:
        out.append('')
    return '\n'.join(out)

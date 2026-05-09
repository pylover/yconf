import io


def dump(obj, file, indent=0, indentsize=2):
    if isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                file.write(f'{" " * indent}-\n')
                dump(v, file, indent + indentsize, indentsize)
            else:
                file.write(f'{" " * indent}- {v}\n')

    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                file.write(f'{" " * indent}{k}:\n')
                dump(v, file, indent + indentsize, indentsize)
            else:
                file.write(f'{" " * indent}{k}: {v}\n')
    else:
        file.write(f'{obj}\n')


def dumps(obj, indent=0, indentsize=2):
    with io.StringIO() as file:
        dump(obj, file, indent, indentsize)
        return file.getvalue()

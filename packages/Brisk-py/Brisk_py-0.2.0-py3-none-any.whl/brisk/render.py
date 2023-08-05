import re
from os import path
from typing import Optional, Any

def html(file: str, eval_expr: bool = True, **scope: Optional[Any]) -> str:
    """Renders the HTML passed in
    :param str file: Name of the HTML file
    :param bool eval_expr: Boolean if the Python in HTML should be executed
    :param Optional scope: Variables to be in the scope of the file
    :return: Generated HTML
    :rtype: str
    """

    filepath = path.join(path.abspath('./template'), file)
    with open(filepath) as f:
        data = f.read()

    if eval_expr:
        return _html(file, data, **scope)
    return data

def _html(file: str, data: str, **scope: Optional[Any]) -> str:
    """Renders the HTML passed in
    :param str file: name of file
    :param str data:
    :param Optional scope:
    :return: Generated HTML
    :rtype: str
    """

    def shrink_lines(stuff: list):
        # stuff.pop(0)
        raise NotImplementedError()


    output = []

    # scoped functions for inline python
    def _print(args):
        output.append(str(args))
    def importer(filename: str):
        if not path.exists(f'./template/{filename}'):
            filename = f'{filename}.html'

        with open(f'./template/{filename}', 'r') as f:
            d = f.read()

        return _html(filename, d, **scope)

    _globals = scope | {'print': _print}
    _util = {'import': importer}


    full, sections = parse(data)

    variables = re.findall(r'({{ ?([_\w\d]+) ?}})', full)
    for match in variables:
        full = full.replace(match[0], scope.get(match[1], ''))
    imports = re.findall(r'({% ?([\w\d_]+) ["\']([\w\d_.]+)["\'] ?%})', full)
    print(f'{imports=}')
    for match in imports:
        print(f'{match=}')
        g = _util.get(match[1], lambda *args: '')(match[2])
        print(f'{g=}')
        full = full.replace(match[0], g)

    for section in sections:
        output.clear()

        section = '\n'.join(section)

        compiled = compile(section, f'<{file}>', 'exec')
        exec(compiled, _globals)
        full = full.replace(''.join(['<--\n', section, '\n-->']), '\n'.join(output))

    return full

def parse(data: str):
    code = []
    is_code = False
    block_no = -1

    for line in data.split('\n'):
        if line.startswith('-->'):
            is_code = False
        elif is_code:
            orig = line
            if line.strip().startswith('<'):
                diff = len(line) - len(line.lstrip())
                char = line[0] if line[0] in [' ', '\t'] else ''
                indent = diff * char
                line = line.replace(r"'", r"\'")
                line = f'{indent}print(f\'{line}\')'
            data = data.replace(orig, line)
            code[block_no].append(line)
        elif line.startswith('<--'):
            block_no += 1
            code.append([])
            is_code = True

    return data, code
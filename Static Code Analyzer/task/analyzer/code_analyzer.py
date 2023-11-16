# write your code here
import sys
import re
import ast
from pathlib import Path
from collections.abc import MutableSequence


def s001(s):
    return len(s) > 79


def s002(s):
    return (len(s) - len(s.lstrip(' '))) % 4 > 0


def s003(s):
    c1 = 0
    for ch in s:
        if ch == '#':
            return False
        if ch == '\'':
            c1 += 1
            continue
        if ch == ';' and c1 % 2 == 0:
            return True
    return False


def s004(s):
    if s.strip(' ').startswith('#'):
        return False
    i = s.find('#')
    if i == -1:
        return False
    if s[i - 1] == ' ' and s[i - 2] == ' ':
        return False
    return True


def s005(s: str):
    if s.count('#'):
        if s.upper().find('TODO', s.find('#')) > -1:
            return True
    return False


class S006:

    def __init__(self):
        self.blank_lines_count = 0

    def __call__(self, line):
        if self.blank_lines_count > 2 and len(line) > 1:
            self.blank_lines_count = 0
            return True
        if len(line) == 1:
            self.blank_lines_count += 1
        else:
            self.blank_lines_count = 0
        return False


class S007:

    def __init__(self):
        self.message = ''

    def __call__(self, s: str) -> bool:
        ls = s.split()
        if len(ls) > 0 and ls[0] in ('def', 'class'):
            if re.match(f'{ls[0]} [A-Za-z0-9_]', s.lstrip()) is not None:
                return False
            else:
                self.message = f'S007: Too many spaces after {ls[0]}'
                return True
        return False

    def __str__(self):
        return self.message


class S008:

    def __init__(self):
        self.message = ''

    def __call__(self, s: str):
        ls = s.split()
        if len(ls) > 1 and ls[0] == 'class':
            if re.match('[A-Z][A-Za-z0-9]*?[(:]', ls[1]) is not None:
                return False
            else:
                self.message = f'S008: Class name {ls[1]} should be written in CamelCase'
                return True
        return False

    def __str__(self):
        return self.message


class S009:

    def __init__(self):
        self.message = ''

    def __call__(self, s: str):
        ls = s.split()
        if len(ls) > 1 and ls[0] == 'def':
            if re.match('[a-z_][a-z0-9_]*?[(]', ls[1]) is not None:
                return False
            else:
                self.message = f'S009: Function name {ls[1]} should be written in snake_case'
                return True
        return False

    def __str__(self):
        return self.message


class S000:

    def __init__(self, name, message, func):
        self.__name = name
        self.__message = message
        self.__func = func

    def __call__(self, s):
        return self.__func(s)

    def __str__(self):
        return f'{self.__name} {self.__message}'


warnings = [
    S000('S001', 'Too long', s001),
    S000('S002', 'Indentation is not a multiple of four', s002),
    S000('S003', 'Unnecessary semicolon', s003),
    S000('S004', 'At least two spaces required before inline comments', s004),
    S000('S005', 'TODO found', s005),
    S000('S006', 'More than two blank lines used before this line', S006()),
    S007(), S008(), S009()
]


def walk_nodes(module):
    res = {}
    nodes = ast.walk(module)
    for node in nodes:
        if type(node) is ast.FunctionDef:
            for arg in node.args.args:
                if re.match('[a-z_][a-z0-9_]*?', arg.arg) is None:
                    if arg.lineno not in res:
                        res[arg.lineno] = []
                    res[arg.lineno].append(f'S010: Argument name {arg.arg} should be written in snake_case')

            nds = ast.walk(node)
            for n in nds:
                if type(n) is ast.Assign:
                    for target in n.targets:
                        if type(target) is ast.Name:
                            if re.match('[a-z_][a-z0-9_]*?', target.id) is None:
                                if target.lineno not in res:
                                    res[target.lineno] = []
                                res[target.lineno].append(f'S011: Variable {target.id} should be written in snake_case')

            for default_val in node.args.defaults:
                val = default_val.value if type(default_val) is ast.Constant else default_val.elts
                if isinstance(val, MutableSequence):
                    if default_val.lineno not in res:
                        res[default_val.lineno] = []
                    res[default_val.lineno].append(f'S012: The default argument value is mutable')
    return res


def check_file(file_path):
    with open(file_path) as f:
        module = ast.parse(f.read())
    with open(file_path) as f:
        contents = f.readlines()

    warns_dict = walk_nodes(module)

    for i, line in enumerate(contents):
        line_num = i + 1
        for warn in warnings:
            if warn(line):
                print(f'{file_path}: Line {line_num}: {warn}')
        if line_num in warns_dict:
            for warn in warns_dict[line_num]:
                print(f'{file_path}: Line {line_num}: {warn}')


def main():
    if len(sys.argv) != 2:
        print('The program takes one command line argument')
        return

    path = Path(sys.argv[len(sys.argv) - 1])
    if path.is_file():
        check_file(path)
    elif path.is_dir():
        for f in path.iterdir():
            if f.is_file() and f.suffix == '.py':
                check_file(f)
    else:
        print(f"Input argument: {path} is not existing directory or file")


if __name__ == '__main__':
    main()

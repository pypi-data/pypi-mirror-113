import argparse
import os
import sys

from architest.model import Project
from architest.utils.colorprint import ColorPrint as color

VERSION_NUMBER = '0.1.7'


def print_fill(message: str, fill_char: str = '=', print_function=print):  # noqa: T002
    terminal_width = os.get_terminal_size().columns
    wing_width = round((terminal_width - len(message) - 4) / 2) - 1
    wing = fill_char * wing_width
    print_function(wing + f'  {message}  ' + wing + '\n')


def search_violations(project: Project):
    project.read_project()
    project.search_violations()
    return project.violations


def _normalized_module_name_for_puml(name: str):
    return name.replace('.', '__').replace(' ', '')


def generate_plant_uml(root: str, args=None):  # noqa: C901
    project = Project(root)
    if args and args.hide_connections:
        hidden_connections = args.hide_connections
    else:
        hidden_connections = []
    project.hidden_connections = project.hidden_connections + hidden_connections
    project.read_project()

    print('@startuml')  # noqa: T001
    style = """
    skinparam linetype ortho
skinparam backgroundColor #4D5566
skinparam fontColor #B3B1AD
skinparam fontName "Avenir"
skinparam fontSize 11
skinparam stereotypeFontColor #aaa
skinparam stereotypeFontSize #fff
skinparam ArrowColor #a1db8a
skinparam rectangle {
  backgroundColor #0A0E14
  borderColor #1b1b1b
  fontColor #fff
  fontName 'Avenir'
  fontSize 11
  stereotypeFontColor #aaa
  stereotypeFontSize 11
}
skinparam frame {
  backgroundColor #5D6677
  borderColor #1b1b1b
  fontColor #000
  fontName 'Avenir'
  fontSize 10
  stereotypeFontColor #aaa
  stereotypeFontSize 11
}
skinparam title {
  fontColor #ccc
  borderColor #ccc
  fontName 'Avenir'
  fontSize 10
  stereotypeFontColor #aaa
  stereotypeFontSize 11
}
    """
    print(style)  # noqa: T001
    if args and args.title:
        print(f'title {args.title}')  # noqa: T001
    upper_modules = []
    for module in project.modules_in_rules:
        if not any(map(lambda ignored: module.path.path.startswith(ignored), args.isolate)):
            continue
        upper_module = module.path.upper_module_name
        if upper_modules and upper_module != upper_modules[-1]:
            print('\n\n}')  # noqa: T001
        if upper_module not in upper_modules:
            print(f'frame {upper_module}', end='')  # noqa: T001
            print('{\n\n')  # noqa: T001
            upper_modules.append(upper_module)

        print(f'rectangle {_normalized_module_name_for_puml(module.path.path)} [')  # noqa: T001
        print(f'  <b>{module.name}</b>')  # noqa: T001
        print('---')  # noqa: T001
        print(f'<i>{module.path.path}</i>')  # noqa: T001
        print('---')  # noqa: T001
        for doc in module.docstrings:
            print(f'"{doc}"')  # noqa: T001
            print()  # noqa: T001
        print(']')  # noqa: T001
        print()  # noqa: T001
    for rule in project.real_rules.rules:
        if rule.connection.name in project.hidden_connections:
            continue
        if not any(map(lambda ignored: rule.module_from.path.path.startswith(ignored), args.isolate)):
            continue
        if not any(map(lambda ignored: rule.module_to.path.path.startswith(ignored), args.isolate)):
            continue
        print(_normalized_module_name_for_puml(rule.module_from.path.path) + ' '  # noqa: T001
            + rule.connection.uml + ' '
            + _normalized_module_name_for_puml(rule.module_to.path.path))  # noqa: T001
    print('@enduml')  # noqa: T001


def main(root: str):
    print()  # noqa: T001
    print_fill('Starting Architest', print_function=color.print_bold)
    print_fill('firmitatis · utilitatis · venustatis', ' ')
    print(f'version: {VERSION_NUMBER} · target project: {root}\n')  # noqa: T001

    file_path = root + '/' + '.architest.yml'
    if not os.path.exists(file_path):
        print_fill('No .architest.yml file found at project root', print_function=color.print_warn)
        sys.exit(1)

    print_fill('Searching for design violations', '-')

    project = Project(root)
    violations = search_violations(project)
    if len(violations) > 0:
        for violation in violations:
            print(violation.violation_error())  # noqa: T001
        print()  # noqa: T001
        print_fill(f'Found {len(violations)} violation{"" if len(violations) == 1 else "s"}',
                   print_function=color.print_fail)
        sys.exit(1)
    else:
        print_fill('Design conforms to config', print_function=color.print_pass)

    print()  # noqa: T001
    sys.exit(0)


def entry_point(args: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--draw', action='store_true')
    parser.add_argument('--hide-connections', nargs='+', default=[])
    parser.add_argument('-i', '--isolate', nargs='+', default=[])
    parser.add_argument('-t', '--title', type=str)
    parser.add_argument('project_path')
    arguments = parser.parse_args()

    if arguments.draw:
        generate_plant_uml(arguments.project_path, arguments)
        sys.exit(0)
    main(arguments.project_path)

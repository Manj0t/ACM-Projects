from STinterpreter import Interpreter

with open("file", "r") as file:
    program_lines = [line.strip() for line in file.readlines()]

interpreter = Interpreter(program_lines)

while interpreter.program_lines[interpreter.line_num] != "halt":
    try:
        command = interpreter.current_line[0]
        if command in interpreter.commands:
            interpreter.commands[command]()
        elif command == '*':
            # Comment line, do nothing
            pass
        elif command.endswith(':'):
            interpreter.add_label(command)
            interpreter.current_line.pop(0)  # Remove the label
            continue
        else:
            raise SyntaxError(f"Syntax error on line {interpreter.line_num}")
    except IndexError:
        # Handle empty lines
        pass

    interpreter.line_num += 1
    interpreter.current_line = interpreter.program_lines[interpreter.line_num].split()
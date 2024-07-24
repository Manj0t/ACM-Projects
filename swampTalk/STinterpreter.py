class Interpreter:
    def __init__(self, program_lines):
        self.variables = {}
        self.label_tracker = {}
        self.operations = ["+", "-"]
        self.line_num = 0
        self.program_lines = program_lines
        self.commands = {
            'show'    : self.print_msg,
            'set'     : self.set_variable,
            'gotoifp' : self.gotoifp,
            'gotoifm' : self.gotoifm,
            'gotoifz' : self.gotoifz
        }
        self.current_line = program_lines[self.line_num].split()

    # def current_line(self):
    #     return self.program_lines[self.line_num]
    def set_variable(self):
        variable = self.current_line[1]
        expression = self.program_lines[self.line_num].split(f'set {variable} ')[1]
        value = self.evaluate_expression(expression, variable)
        self.variables[variable] = value

    def check_type(self, value):
        try:
            value = float(value)
            if value.is_integer():
                return int(value)
            return value
        except ValueError:
            return value

    def get_variable(self, name):
        return self.variables[name]

    def evaluate_expression(self, expression, variable=None):

        split_expression = []
        current = []

        for char in expression:
            if char == " ":
                continue
            if current and char in self.operations:
                split_expression.append(''.join(current))
                split_expression.append(char)
                current = []
            else:
                current.append(char)
        if current:
            split_expression.append(''.join(current))

        if len(split_expression) == 1:
            var = split_expression[0]
            if var in self.variables:
                value = self.variables[var]
                return value
            value = self.check_type(var)
            return value

        result = 0
        current_operation = '+'

        for element in split_expression:
            if element in self.operations:
                current_operation = element
                continue

            value = self.check_type(element)
            if value == element:
                try:
                    value = self.variables[element]
                    if isinstance(value, str):
                        raise ValueError("Incorrect usage")
                        exit(1)
                except:
                    if value == variable:
                        value = 0
                    else:
                        raise ValueError(f"{element} not found")
                        exit(1)

            if current_operation == '+':
                result += value
            elif current_operation == '-':
                result -= value

        return result

    def get_label(self, label):
        if label in self.label_tracker:
            return self.label_tracker[label]
        else:
            for i in range(self.line_num, len(self.program_lines)):
                label = self.program_lines[i].split()[0]
                if label.endswith(":"):
                    self.add_label(label, i)
                    return i

            raise SyntaxError("Label not found")

    def add_label(self, label, line_num=None):
        if line_num is None:
            line_num = self.line_num
        try:
            label = label.replace(":", "")
            if label not in self.label_tracker:
                self.label_tracker[label] = line_num
        except:
            raise SyntaxError(f"{label} is not a label")

    def print_msg(self):
        message = self.current_line[1]
        if message in self.variables:
            print(self.variables[message])
        else:
            print(message)

    def gotoifp(self):
        label = self.program_lines[self.line_num].split()[1]
        expression = self.program_lines[self.line_num].split(f' {label} ')[1]
        value = self.evaluate_expression(expression)
        if value > 0:
            self.line_num = self.get_label(label) - 1

    def gotoifm(self):
        label = self.program_lines[self.line_num].split()[1]
        expression = self.program_lines[self.line_num].split(f' {label} ')[1]
        value = self.evaluate_expression(expression)
        if value < 0:
            self.line_num = self.get_label(label) - 1

    def gotoifz(self):
        label = self.program_lines[self.line_num].split()[1]
        expression = self.program_lines[self.line_num].split(f' {label} ')[1]
        value = self.evaluate_expression(expression)
        if value == 0:
            self.line_num = self.get_label(label) - 1

#!/usr/bin/env python3

import fileinput
from copy import deepcopy
import re

class Module:
    def __init__(self, name: str, outputs: list[str]):
        self.name = name
        self.outputs = outputs

    def reset_state(self, modules: dict):
        return

    def process(self, input_name: str, input: bool) -> list:
        return []

class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.outputs = outputs

    def reset_state(self, modules: dict):
        self.state = False

    def process(self, input_name: str, input: bool) -> list:
        return [(self.name, output, input) for output in self.outputs]

    def __str__(self):
        return f'Broadcaster({self.outputs})'
    __repr__ = __str__

class FlipFlop(Module):
    def __init__(self, name:str, outputs: list[str]):
        super().__init__(name, outputs)
        self.state = False

    def reset_state(self, modules: dict):
        self.state = False

    def process(self, input_name: str, input: bool) -> list:
        if input:
            return []
        
        self.state = not self.state
        return [(self.name, output, self.state) for output in self.outputs]

    def __str__(self):
        return f'FlipFlop({self.state}, {self.outputs})'
    __repr__ = __str__

class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.state = {}

    def reset_state(self, modules: dict):
        inputs = [k for k, v in modules.items() for o in v.outputs if o == self.name]
        self.state = {input_name: False for input_name in inputs}

    def process(self, input_name: str, input: bool) -> list:
        self.state[input_name] = input
        output_state = not all(self.state.values())
        
        return [(self.name, output, output_state) for output in self.outputs]

    def __str__(self):
        return f'Conjunction({self.state}, {self.outputs})'
    __repr__ = __str__


def parse_line(line: str, modules: dict) -> dict:
    m = re.findall('([a-z%&]+) -> ([a-z, ]+)', line)
    print(m)

    outputs = [s.strip() for s in m[0][1].split(',')]
    if m[0][0] == 'broadcaster':
        modules[m[0][0]] = Broadcaster(m[0][0], outputs)
    elif m[0][0][0] == '%':
        modules[m[0][0][1:]] = FlipFlop(m[0][0][1:], outputs)
    elif m[0][0][0] == '&':
        modules[m[0][0][1:]] = Conjunction(m[0][0][1:], outputs)

    return modules

def button_press(modules: dict, count: int, p2: bool) -> list:
    pulse_count = [0, 0]
    mg_inputs = [k for k, v in modules.items() if 'mg' in v.outputs]
    cycle_start = {}
    cycle_high = {}
    print(mg_inputs)
    for c in range(count):
        pulse_queue = [('button', 'broadcaster', False)]
        #print('button -low-> broadcaster')
        while len(pulse_queue) > 0:
            input_name, module_name, value = pulse_queue.pop(0)
            if module_name not in modules:
                modules[module_name] = Module(module_name, [])
            pulse_count[value] += 1
            outputs = modules[module_name].process(input_name, value)
            for o in outputs:
                if (module_name in mg_inputs) and o[2]:
                    if module_name not in cycle_start:
                        cycle_start[module_name] = c
                        cycle_high[module_name] = c
                    else:
                        print(f'Cycle detected for {module_name} at {c} : start = {cycle_start[module_name]}, period = {c - cycle_high[module_name]}')
                        cycle_high[module_name] = c

                    print(f'{pulse_count} : {module_name} -{"high" if o[2] else "low"}-> {o[1]}')
                pass
            pulse_queue.extend(outputs)

    return pulse_count
        

def main():
    modules = {}
    for line in fileinput.input():
        modules = parse_line(line.strip(), modules)
        print(modules)
    
    for m in modules.values():
        m.reset_state(modules)

    low, high = button_press(modules, 1000, False)
    print(f'Low: {low}, High: {high}, Product: {low * high}')

    for m in modules.values():
        m.reset_state(modules)
    low, high = button_press(deepcopy(modules), 1000000000000000000000, True)

if __name__ == '__main__':
    main()

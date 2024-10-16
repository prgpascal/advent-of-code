import os
from collections import deque
from dataclasses import dataclass
from utils.io import write_output
from math import lcm
from abc import ABC, abstractmethod


@dataclass
class Instruction:
    source: str
    target: str
    pulse: int


@dataclass
class Module(ABC):
    id: str
    destinations: list[str]

    @abstractmethod
    def receive_pulse(self, instruction) -> list[Instruction]:
        ...


@dataclass
class Conjunction(Module):
    history: dict[str, int]

    def receive_pulse(self, instruction):
        self.history[instruction.source] = instruction.pulse
        new_pulse = 1 if any(v for v in self.history.values() if v < 0) else -1
        next_instructions = []
        for dest in self.destinations:
            next_instructions.append(Instruction(self.id, dest, new_pulse))
        return next_instructions


@dataclass
class FlipFlop(Module):
    status = False

    def receive_pulse(self, instruction):
        if instruction.pulse > 0:
            return []
        else:
            new_pulse = -1 if self.status else 1
            self.status = not self.status
            next_instructions = []
            for dest in self.destinations:
                next_instructions.append(Instruction(self.id, dest, new_pulse))
            return next_instructions


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        modules = dict()
        broadcaster_targets = []
        conjunction_modules = []
        for line in file:
            source, destinations = line.strip().split("->")
            destinations = [x.strip() for x in destinations.split(",")]
            id = source.strip()

            if id[0] == "%":
                id = id[1:]
                module = FlipFlop(id, destinations)
                modules[id] = module
            elif id[0] == "&":
                id = id[1:]
                module = Conjunction(id, destinations, dict())
                modules[id] = module
                conjunction_modules.append(id)
            else:
                broadcaster_targets.extend(destinations)

        # update the sources of conjunction nodes
        for k, v in modules.items():
            for dest in v.destinations:
                if dest in conjunction_modules:
                    modules[dest].history[k] = -1

    return (broadcaster_targets, modules)


def solve_1(input):
    BUTTON_CLICKS = 1000
    broadcaster_targets, modules = input
    queue: deque[Instruction] = deque()
    high_pulses = 0
    low_pulses = 0

    for _ in range(BUTTON_CLICKS):
        # Push the button (send a low pulse to the broadcaster)
        low_pulses += 1

        for target in broadcaster_targets:
            queue.append(Instruction("broadcaster", target, -1))

        while queue:
            instruction = queue.popleft()
            high_pulses += 1 if instruction.pulse > 0 else 0
            low_pulses += 1 if instruction.pulse < 0 else 0

            if instruction.target in modules:
                target_module = modules[instruction.target]
                next_instructions = target_module.receive_pulse(instruction)
                queue.extend(next_instructions)

    return low_pulses * high_pulses


def solve_2(input):
    broadcaster, modules = input
    last_conjunction_id = [k for k, v in modules.items() if "rx" in v.destinations][0]
    last_conjunction_module = modules[last_conjunction_id]
    last_conjunction_min_steps = dict()
    queue: deque[Instruction] = deque()
    button_presses = 0

    while len(last_conjunction_min_steps) < 4:
        # Push the button (send a low pulse to the broadcaster)
        button_presses += 1

        for target in broadcaster:
            queue.append(Instruction("broadcaster", target, -1))

        while queue:
            instruction = queue.popleft()

            if instruction.target not in modules:
                for k, v in last_conjunction_module.history.items():
                    if v > 0 and k not in last_conjunction_min_steps:
                        last_conjunction_min_steps[k] = button_presses
            else:
                target_module = modules[instruction.target]
                next_instructions = target_module.receive_pulse(instruction)
                queue.extend(next_instructions)

    return lcm(*last_conjunction_min_steps.values())


write_output(solve_1(read_input()), solve_2(read_input()))

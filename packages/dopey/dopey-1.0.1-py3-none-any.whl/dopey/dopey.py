#!/usr/bin/env python

import sys
from typing import Dict, List

class MismatchBracketException(Exception):
    """ TODO line number and column """
    pass

class MemoryException(Exception):
    """ TODO line number and column """
    pass

class _Memory:
    BUFFER_SIZE = 30_000
    buffer = []
    pointer = 0
    input_buffer = []

    @classmethod
    def get_pointer(cls) -> int:
        return cls.pointer

    @classmethod
    def reset(cls):
        cls.buffer = [0 for _ in range(cls.BUFFER_SIZE)]
        cls.pointer = 0
        cls.input_buffer = []

class _Operation:
    SHIFT_LEFT = "<"
    SHIFT_RIGHT = ">"
    INCREMENT = "+"
    DECREMENT = "-"
    OUTPUT = "."
    INPUT = ","
    OPEN_LOOP = "["
    CLOSE_LOOP = "]"

    loop_stack = []
    loop_ignore_stack = []

    @classmethod
    def perform(cls, operation: str, program: List, switch: Dict) -> None:
        # if operation does not exist, skip
        if operation not in switch:
            return

        # dont perform any non loop operations if inside an ignore loop
        if len(cls.loop_ignore_stack) and operation != _Operation.CLOSE_LOOP and operation != _Operation.OPEN_LOOP:
            return

        switch[operation](program)

    @classmethod
    def shift_left(cls, _) -> None:
        _Memory.pointer -= 1
        if _Memory.pointer < 0:
            raise MemoryException
    
    @classmethod
    def shift_right(cls, _) -> None:
        _Memory.pointer += 1
        if _Memory.pointer >= _Memory.BUFFER_SIZE:
            raise MemoryException

    @classmethod    
    def increment(cls, _) -> None:
        _Memory.buffer[_Memory.get_pointer()] += 1

    @classmethod
    def decrement(cls, _) -> None:
        _Memory.buffer[_Memory.get_pointer()] -= 1

    @classmethod
    def output(cls, _) -> None:
        sys.stdout.write(chr(_Memory.buffer[_Memory.get_pointer()]))
        sys.stdout.flush() # TODO possible performance issue

    @classmethod
    def input(cls, _) -> None:
        if not len(_Memory.input_buffer):
            input_ = sys.stdin.readline()
            _Memory.input_buffer += list(input_)
        if len(_Memory.input_buffer):
            _Memory.buffer[_Memory.get_pointer()] = ord(_Memory.input_buffer.pop(0))

    @classmethod
    def open_loop(cls, program: List) -> None:
        if not _Memory.buffer[_Memory.get_pointer()]:
            # enter ignore loop if byte at pointer is zero
            cls.loop_ignore_stack.append(_Operation.OPEN_LOOP)
        else:
            # save start loop position should we need to return
            cls.loop_stack.append(program[1]-1)
    
    @classmethod
    def close_loop(cls, program: List) -> None:
        # check if in ignore loop
        if len(cls.loop_ignore_stack):
           cls.loop_ignore_stack.pop()
           return

        # check if there is a bracket mismatch
        if not len(cls.loop_stack):
            raise MismatchBracketException

        # check if we need to repeat
        last_open_loop_pos = cls.loop_stack.pop()
        if _Memory.buffer[_Memory.get_pointer()]:
            program[1] = last_open_loop_pos

    @classmethod
    def get_operations_in_switch(cls) -> Dict:
        return {
            cls.SHIFT_LEFT: cls.shift_left,
            cls.SHIFT_RIGHT: cls.shift_right,
            cls.INCREMENT: cls.increment,
            cls.DECREMENT: cls.decrement,
            cls.OUTPUT: cls.output,
            cls.INPUT: cls.input,
            cls.OPEN_LOOP: cls.open_loop,
            cls.CLOSE_LOOP: cls.close_loop
        }

class Interpreter:
    def __init__(self):
        pass

    def execute(self, str_program: str) -> None:
        _Memory.reset()

        program = [str_program, 0] # TODO create program class
        switch = _Operation.get_operations_in_switch()

        while program[1] < len(program[0]):
            operation = program[0][program[1]]
            program[1] += 1
            _Operation.perform(operation, program, switch)

        if len(_Operation.loop_stack):
            raise MismatchBracketException

def _main() -> None:
    file_location = None
    if len(sys.argv) != 2:
        print("Invalid or missing arguments...")
        sys.exit()
    else:
        file_location = sys.argv[1]

    file = open(file_location, "r")
    str_program = file.read()
    file.close()

    interpreter = Interpreter()
    interpreter.execute(str_program)

if __name__ == "__main__":
    _main()
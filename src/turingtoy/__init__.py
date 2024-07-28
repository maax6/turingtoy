from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    # Initialisation
    blank_symbol = machine['blank']
    actual_state = machine['start state']
    final_state = set(machine['final states'])
    transition_table = machine['table']
    
    tape = list(input_)
    head_position = 0
    history = []

    def add_history(state, reading, memory, transition, position):
        history.append({
            "state": state,
            "reading": reading,
            "position": position,
            "memory": "".join(memory),
            "transition": transition
        })
    
    step = 0
    while steps is None or step < steps:
        if head_position < 0:
            tape.insert(0, blank_symbol)
            head_position = 0
        if head_position >= len(tape):
            tape.append(blank_symbol)
        
        actual_symbol = tape[head_position]
        if actual_state in transition_table and actual_symbol in transition_table[actual_state]:
            transition = transition_table[actual_state][actual_symbol]
            add_history(actual_state, actual_symbol, tape, transition, head_position)

            if isinstance(transition, str):
                if transition == "R":
                    head_position += 1
                if transition == "L":
                    head_position -= 1
            else:
                if 'write' in transition:
                    tape[head_position] = transition['write']
                if 'R' in transition:
                    actual_state = transition['R']
                    head_position += 1
                if 'L' in transition:
                    actual_state = transition['L']
                    head_position -= 1
            
            step += 1

            if actual_state in final_state:
                break
        else:
            add_history(actual_state, actual_symbol, tape, None, head_position)
            break
    
    output = ''.join(tape).strip(blank_symbol)
    halted = actual_state in final_state
    return output, history, halted

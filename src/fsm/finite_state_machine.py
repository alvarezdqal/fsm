from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from fsm.exceptions import TransitionError
from fsm.typing import InputLetter, State
from fsm.validation import (
    validate_alphabet,
    validate_final_states,
    validate_initial_state,
    validate_state_transition_function,
    validate_states,
)


@dataclass
class FiniteStateMachine:
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        final_states: Set[State],
    ) -> None:

        validate_alphabet(input_alphabet)
        self.input_alphabet = input_alphabet

        validate_states(states)
        self.states = states

        validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        validate_state_transition_function(state_transition_function, states, input_alphabet)
        self.state_transition_function = state_transition_function

        validate_final_states(final_states, states)
        self.final_states = final_states

        return

    def accepts(self, seq: List[InputLetter], print_path: bool = False) -> bool:

        state_map = f"[{self.initial_state}]"
        current_state = self.initial_state
        for elem in seq:
            try:
                next_state = self.state_transition_function[(current_state, elem)]
            except KeyError:
                raise TransitionError(
                    "The following encountered (state, input) pair is "
                    f"undefined in the state transition fuction: ({current_state},{elem})"
                ) from None
            current_state = next_state
            state_map += f" --({elem})-> [{current_state}]"
            if current_state in self.final_states:
                break

        if print_path:
            print(state_map)

        return current_state in self.final_states

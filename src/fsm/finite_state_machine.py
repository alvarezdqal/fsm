from dataclasses import dataclass
from typing import Dict, Set, Tuple

from fsm.typing import InputLetter, State
from fsm.validation import (
    validate_alphabet,
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
    ) -> None:

        validate_alphabet(input_alphabet)
        self.input_alphabet = input_alphabet

        validate_states(states)
        self.states = states

        validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        validate_state_transition_function(state_transition_function, states, input_alphabet)
        self.state_transition_function = state_transition_function

        return

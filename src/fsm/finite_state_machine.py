from dataclasses import dataclass
from typing import Dict, Generic, Set, Tuple

from fsm.typevars import InputLetter, State
from fsm.validation import (
    validate_alphabet,
    validate_initial_state,
    validate_state_transition_function,
    validate_states,
)


@dataclass
class FiniteStateMachine(Generic[InputLetter, State]):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
    ) -> None:

        validate_alphabet(alphabet=input_alphabet)
        self.input_alphabet = input_alphabet

        validate_states(states=states)
        self.states = states

        validate_initial_state(initial_state=initial_state, states=states)
        self.initial_state = initial_state

        validate_state_transition_function(
            state_transition_function=state_transition_function,
            input_alphabet=input_alphabet,
            states=states,
        )
        self.state_transition_function = state_transition_function

        return

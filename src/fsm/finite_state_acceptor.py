from dataclasses import dataclass
from typing import Dict, Generic, List, Set, Tuple

from fsm.exceptions import StateTransitionError
from fsm.finite_state_machine import FiniteStateMachine
from fsm.typing import InputLetter, State
from fsm.validation import validate_final_states


@dataclass
class FiniteStateAcceptor(FiniteStateMachine, Generic[InputLetter, State]):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        final_states: Set[State],
    ) -> None:

        super().__init__(
            input_alphabet=input_alphabet,
            states=states,
            initial_state=initial_state,
            state_transition_function=state_transition_function,
        )

        validate_final_states(final_states=final_states, states=states)
        self.final_states = final_states

    def accepts(self, seq: List[InputLetter], print_path: bool = False) -> bool:

        state_map = f"[{self.initial_state}]"
        current_state: State = self.initial_state
        for elem in seq:

            try:
                next_state: State = self.state_transition_function[(current_state, elem)]
            except KeyError:
                raise StateTransitionError(
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

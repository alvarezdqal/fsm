from typing import Dict, List, Set, Tuple

from fsm.finite_state_machine import FiniteStateMachine
from fsm.typing import Letter, OutputLetter, State


def _validate_output_aphabet() -> None:
    pass


def _validate_output_function() -> None:
    pass


class FiniteStateTransducer(FiniteStateMachine):
    def __init__(
        self,
        alphabet: Set[Letter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, Letter], State],
        final_states: Set[State],
        output_aphabet: Set[Letter],
        output_function: Dict[Tuple[State, Letter], OutputLetter],
    ) -> None:
        super().__init__(alphabet, states, initial_state, state_transition_function, final_states)

        _validate_output_aphabet()
        self.output_aphabet = output_aphabet

        _validate_output_function()
        self.output_function = output_function

        return

    def transduce(self, seq: List[Letter]) -> List[OutputLetter]:
        pass

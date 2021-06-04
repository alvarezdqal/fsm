from typing import Dict, List, Set, Tuple

from fsm.finite_state_machine import FiniteStateMachine
from fsm.typing import InputLetter, OutputLetter, State


def _validate_output_aphabet() -> None:
    pass


def _validate_output_function() -> None:
    pass


class FiniteStateTransducer(FiniteStateMachine):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        final_states: Set[InputLetter],
        output_aphabet: Set[InputLetter],
        output_function: Dict[Tuple[State, InputLetter], OutputLetter],
    ) -> None:

        super().__init__(
            input_alphabet=input_alphabet,
            states=states,
            initial_state=initial_state,
            state_transition_function=state_transition_function,
            final_states=final_states,
        )

        _validate_output_aphabet()
        self.output_aphabet = output_aphabet

        _validate_output_function()
        self.output_function = output_function

        return

    def transduce(self, seq: List[InputLetter]) -> List[OutputLetter]:
        pass

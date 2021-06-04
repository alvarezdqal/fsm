from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from fsm.exceptions import TransductionError
from fsm.finite_state_machine import FiniteStateMachine
from fsm.typing import InputLetter, OutputLetter, State
from fsm.validation import validate_alphabet, validate_output_function


@dataclass
class FiniteStateTransducer(FiniteStateMachine):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        output_alphabet: Set[InputLetter],
        output_function: Dict[Tuple[State, InputLetter], OutputLetter],
    ) -> None:

        super().__init__(
            input_alphabet=input_alphabet,
            states=states,
            initial_state=initial_state,
            state_transition_function=state_transition_function,
        )

        validate_alphabet(alphabet=output_alphabet)
        self.output_alphabet = output_alphabet

        validate_output_function(
            output_function=output_function,
            input_alphabet=input_alphabet,
            states=states,
            output_alphabet=output_alphabet,
        )
        self.output_function = output_function

        return

    def transduce(self, seq: List[InputLetter]) -> List[OutputLetter]:

        raise TransductionError(f"TODO: {self}")

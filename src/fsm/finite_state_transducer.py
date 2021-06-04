from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from fsm.finite_state_acceptor import FiniteStateAcceptor
from fsm.typing import InputLetter, OutputLetter, State
from fsm.validation import validate_alphabet, validate_output_function


@dataclass
class FiniteStateTransducer(FiniteStateAcceptor):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        output_aphabet: Set[InputLetter],
        output_function: Dict[Tuple[State, InputLetter], OutputLetter],
    ) -> None:

        super().__init__(
            input_alphabet=input_alphabet,
            states=states,
            initial_state=initial_state,
            state_transition_function=state_transition_function,
            final_states=set(),
        )

        validate_alphabet(output_aphabet)
        self.output_aphabet = output_aphabet

        validate_output_function(output_function)
        self.output_function = output_function

        return

    def transduce(self, seq: List[InputLetter]) -> List[OutputLetter]:
        pass

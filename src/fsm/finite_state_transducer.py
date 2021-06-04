from dataclasses import dataclass
from typing import Dict, Generic, List, Set, Tuple

from fsm.exceptions import StateTransitionError, TransductionError
from fsm.finite_state_machine import FiniteStateMachine
from fsm.typevars import InputLetter, OutputLetter, State
from fsm.validation import validate_alphabet, validate_output_function


@dataclass
class FiniteStateTransducer(FiniteStateMachine, Generic[InputLetter, OutputLetter, State]):
    def __init__(
        self,
        input_alphabet: Set[InputLetter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, InputLetter], State],
        output_alphabet: Set[OutputLetter],
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

    def transduce(self, seq: List[InputLetter], print_path: bool = False) -> List[OutputLetter]:

        state_map = f"[{self.initial_state}]"
        output_seq: List[OutputLetter] = []
        current_state: State = self.initial_state
        for elem in seq:

            try:
                output: OutputLetter = self.output_function[(current_state, elem)]
            except KeyError:
                raise TransductionError(
                    "The following encountered (state, input) pair is "
                    f"undefined in the output fuction: ({current_state},{elem})"
                ) from None
            output_seq.append(output)

            try:
                next_state: State = self.state_transition_function[(current_state, elem)]
            except KeyError:
                raise StateTransitionError(
                    "The following encountered (state, input) pair is "
                    f"undefined in the state transition fuction: ({current_state},{elem})"
                ) from None
            current_state = next_state

            state_map += f" --({elem})-> [{current_state}]"

        if print_path:
            print(state_map)

        return output_seq

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from fsm.exceptions import (
    FinalStatesError,
    InitialStateError,
    InputAlphabetError,
    StatesError,
    StateTransitionFunctionError,
    TransitionError,
)
from fsm.typing import InputLetter, State


def _validate_input_alphabet(input_alphabet: Set[InputLetter]) -> None:

    # Checking non-empty set
    if not input_alphabet or not isinstance(input_alphabet, set):
        raise InputAlphabetError(f"The passed input_alphabet not a non-empty set: {input_alphabet}")

    # Checking that the elements are same type
    if len(input_alphabet) > 1:
        types = {type(lett) for lett in input_alphabet}
        if len(types) > 1:
            raise InputAlphabetError(f"The passed letters do not have same type: {types}")

    return


def _validate_states(states: Set[State]) -> None:

    # Checking non-empty set
    if not states or not isinstance(states, set):
        raise StatesError(f"The passed states not a non-empty set: {states}")

    # Checking that the elements are same type
    if len(states) > 1:
        types = {type(s) for s in states}
        if len(types) > 1:
            raise StatesError(f"The passed states do not have same type: {types}")

    return


def _validate_initial_state(initial_state: State, states: Set[State]) -> None:

    # Checking that initial state in states
    if initial_state not in states:
        raise InitialStateError(f"The passed initial state is not an element of passed states: '{initial_state}'")

    return


def _validate_state_transition_function(
    state_transition_function: Dict[Tuple[State, InputLetter], State],
    states: Set[State],
    input_alphabet: Set[InputLetter],
) -> None:

    # Checking that keys tuples of length 2
    non_tuples_of_length_two = set(
        k for k in state_transition_function.keys() if not isinstance(k, tuple) or len(k) != 2
    )
    if non_tuples_of_length_two:
        raise StateTransitionFunctionError(
            "The following keys passed to the state transition function are "
            f"not tuples of length 2: {non_tuples_of_length_two}"
        )

    # Checking that keys valid elements of cross-product of states and input_alphabet
    non_elements_of_states = set(k[0] for k in state_transition_function.keys()) - states
    non_elements_of_input_alphabet = set(k[1] for k in state_transition_function.keys()) - input_alphabet
    if non_elements_of_states:
        raise StateTransitionFunctionError(
            "The following states passed to the state transition function are "
            f"not elements of the passed states: {non_elements_of_states}"
        )
    if non_elements_of_input_alphabet:
        raise StateTransitionFunctionError(
            "The following letters passed to the state transition function are "
            f"not elements of the passed alphebet: {non_elements_of_input_alphabet}"
        )

    # Checking that values valid states
    non_elements_of_states = set(state_transition_function.values()) - states
    if non_elements_of_states:
        raise StateTransitionFunctionError(
            "The following states passed to the state transition function are "
            f"not elements of the passed states: {non_elements_of_states}"
        )

    return


def _validate_final_states(final_states: Set[State], states: Set[State]) -> None:

    # Checking that set
    if not isinstance(final_states, set):
        raise FinalStatesError(f"The passed final states is not a set: {final_states}")

    # Checking that subset of states
    if not final_states.issubset(states):
        raise FinalStatesError(f"The passed set of final states is not a subset of passed states: {final_states}")

    return


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

        _validate_input_alphabet(input_alphabet)
        self.input_alphabet = input_alphabet

        _validate_states(states)
        self.states = states

        _validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        _validate_state_transition_function(state_transition_function, states, input_alphabet)
        self.state_transition_function = state_transition_function

        _validate_final_states(final_states, states)
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

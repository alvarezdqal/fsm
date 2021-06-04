from typing import Dict, Set, Tuple, Union

from fsm.exceptions import AlphabetError, FinalStatesError, InitialStateError, StatesError, StateTransitionFunctionError
from fsm.typing import InputLetter, OutputLetter, State


def validate_alphabet(alphabet: Set[Union[InputLetter, OutputLetter]]) -> None:

    # Checking non-empty set
    if not alphabet or not isinstance(alphabet, set):
        raise AlphabetError(f"The passed alphabet not a non-empty set: {alphabet}")

    # Checking that elements same type
    if len(alphabet) > 1:
        types = {type(lett) for lett in alphabet}
        if len(types) > 1:
            raise AlphabetError(f"The passed letters do not have same type: {types}")

    return


def validate_final_states(final_states: Set[State], states: Set[State]) -> None:

    # Checking that set
    if not isinstance(final_states, set):
        raise FinalStatesError(f"The passed final states is not a set: {final_states}")

    # Checking that subset of states
    if not final_states.issubset(states):
        raise FinalStatesError(f"The passed set of final states is not a subset of passed states: {final_states}")

    return


def validate_initial_state(initial_state: State, states: Set[State]) -> None:

    # Checking that initial state in states
    if initial_state not in states:
        raise InitialStateError(f"The passed initial state is not an element of passed states: '{initial_state}'")

    return


def validate_output_function(output_function: Dict[Tuple[State, InputLetter], OutputLetter]) -> None:
    return


def validate_state_transition_function(
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


def validate_states(states: Set[State]) -> None:

    # Checking non-empty set
    if not states or not isinstance(states, set):
        raise StatesError(f"The passed states not a non-empty set: {states}")

    # Checking that elements same type
    if len(states) > 1:
        types = {type(s) for s in states}
        if len(types) > 1:
            raise StatesError(f"The passed states do not have same type: {types}")

    return

from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple

from fsm.exceptions import AlphabetError, FinalStatesError, InitialStateError, StatesError, StateTransitionFunctionError


def validate_alphabet(alphabet: Set[str]) -> None:

    # Checking non-empty
    if not alphabet:
        raise AlphabetError(f"The passed alphabet is empty: '{alphabet}'")

    # Checking that set
    if not isinstance(alphabet, set):
        raise AlphabetError(f"The passed alphabet is not a set: {alphabet}")

    # Checking that the elements are strings
    non_strings: Set[Any] = set()
    for letter in alphabet:
        if not isinstance(letter, str):
            non_strings.add(letter)
    if non_strings:
        raise AlphabetError(f"The following elements of the passed alphabet are not strings: {non_strings}")

    return


def validate_states(states: Set[str]) -> None:

    # Checking non-empty
    if not states:
        raise StatesError(f"The passed states is empty: '{states}'")

    # Checking that set
    if not isinstance(states, set):
        raise StatesError(f"The passed states is not a set: {states}")

    # Checking that the elements are strings
    non_strings: Set[Any] = set()
    for state in states:
        if not isinstance(state, str):
            non_strings.add(state)
    if non_strings:
        raise StatesError(f"The following elements of the passed states are not strings: {non_strings}")

    return


def validate_initial_state(initial_state: str, states: Set[str]) -> None:

    # Checking that initial state in states
    if initial_state not in states:
        raise InitialStateError(f"The passed initial state is not an element of passed states: '{initial_state}'")

    return


def validate_state_transition_function(
    state_transition_function: Dict[Tuple[str, str], str], states: Set[str], alphabet: Set[str], final_states: Set[str]
) -> None:

    # Checking non-empty
    if not state_transition_function:
        raise StateTransitionFunctionError(
            f"The passed state transition function is empty: '{state_transition_function}'"
        )

    # Check that dict
    if not isinstance(state_transition_function, dict):
        raise StateTransitionFunctionError(
            f"The passed state transition function is not a dict: '{state_transition_function}'"
        )

    # Checking that keys tuples of length 2
    non_tuples_of_length_two = set()
    for k in state_transition_function.keys():
        if not isinstance(k, tuple) or len(k) != 2:
            non_tuples_of_length_two.add(k)
    if non_tuples_of_length_two:
        raise StateTransitionFunctionError(
            "The following keys passed to the state transition function are "
            f"not tuples of length 2: {non_tuples_of_length_two}"
        )

    # Checking that keys valid elements of cross-product of states and alphabet
    non_elements_of_states = set()
    non_elements_of_alphabet = set()
    for s, a in state_transition_function.keys():
        if s not in states:
            non_elements_of_states.add(s)
        if a not in alphabet:
            non_elements_of_alphabet.add(a)
    if non_elements_of_states:
        raise StateTransitionFunctionError(
            "The following states passed to the state transition function are "
            f"not elements of the passed states: {non_elements_of_states}"
        )
    if non_elements_of_alphabet:
        raise StateTransitionFunctionError(
            "The following elements passed to the state transition function are "
            f"not elements of the passed alphebet: {non_elements_of_alphabet}"
        )

    # Checking that all states have mapping
    undefined_state_letters = set()
    for s in states - final_states:
        for a in alphabet:
            pair = (s, a)
            if pair not in state_transition_function.keys():
                undefined_state_letters.add(pair)
    if undefined_state_letters:
        raise StateTransitionFunctionError(
            f"The following cases have not been covered in the state transition function: {undefined_state_letters}"
        )

    # Checking that values valid states
    non_elements_of_states = set()
    for v in state_transition_function.values():
        if v not in states:
            non_elements_of_states.add(v)
    if non_elements_of_states:
        raise StateTransitionFunctionError(
            "The following states passed to the state transition function are "
            f"not elements of the passed states: {non_elements_of_states}"
        )

    return


def validate_final_states(final_states: Set[str], states: Set[str]) -> None:

    # Checking that set
    if not isinstance(final_states, set):
        raise FinalStatesError(f"The passed final states if not a set: {final_states}")

    # Checking that subset of states
    if not final_states.issubset(states):
        raise FinalStatesError(f"The passed set of final states is not a subset of passed states: {final_states}")

    return


@dataclass
class FiniteStateMachine:
    def __init__(
        self,
        alphabet: Set[str],
        states: Set[str],
        initial_state: str,
        state_transition_function: Dict[Tuple[str, str], str],
        final_states: Set[str],
    ) -> None:

        validate_alphabet(alphabet)
        self.alphabet = alphabet

        validate_states(states)
        self.states = states

        validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        validate_state_transition_function(state_transition_function, states, alphabet, final_states)
        self.state_transition_function = state_transition_function

        validate_final_states(final_states, states)
        self.final_states = final_states

        return

    def parse(self, seq: List[str]) -> bool:

        state_map = f"[{self.initial_state}]"
        current_state = self.initial_state
        for elem in seq:
            next_state = self.state_transition_function[(current_state, elem)]
            state_map += f" --({elem})-> [{next_state}]"
            current_state = next_state
            if next_state in self.final_states:
                break

        print(state_map)

        return current_state in self.final_states

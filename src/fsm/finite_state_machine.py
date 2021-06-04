from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple, TypeVar

from fsm.exceptions import (
    AlphabetError,
    FinalStatesError,
    InitialStateError,
    StatesError,
    StateTransitionFunctionError,
    TransitionError,
)

A = TypeVar("A")  # elements of the 'alphabet'
S = TypeVar("S")  # elements of the 'states'


def validate_alphabet(alphabet: Set[A]) -> None:

    # Checking non-empty
    if not alphabet:
        raise AlphabetError(f"The passed alphabet is empty: {alphabet}")

    # Checking that set
    if not isinstance(alphabet, set):
        raise AlphabetError(f"The passed alphabet is not a set: {alphabet}")

    # Checking that the elements are strings
    non_strings: Set[Any] = set()
    for letter in alphabet:
        if not isinstance(letter, str):  # TODO make this more flexible
            non_strings.add(letter)
    if non_strings:
        raise AlphabetError(f"The following elements of the passed alphabet are not strings: {non_strings}")

    return


def validate_states(states: Set[S]) -> None:

    # Checking non-empty
    if not states:
        raise StatesError(f"The passed states is empty: {states}")

    # Checking that set
    if not isinstance(states, set):
        raise StatesError(f"The passed states is not a set: {states}")

    # Checking that the elements are strings
    non_strings: Set[Any] = set()
    for state in states:
        if not isinstance(state, str):  # TODO make this more flexible
            non_strings.add(state)
    if non_strings:
        raise StatesError(f"The following elements of the passed states are not strings: {non_strings}")

    return


def validate_initial_state(initial_state: S, states: Set[S]) -> None:

    # Checking that initial state in states
    if initial_state not in states:
        raise InitialStateError(f"The passed initial state is not an element of passed states: '{initial_state}'")

    return


def validate_state_transition_function(
    state_transition_function: Dict[Tuple[S, A], S],
    states: Set[S],
    alphabet: Set[A],
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

    # Checking that keys valid elements of cross-product of states and alphabet
    non_elements_of_states = set(k[0] for k in state_transition_function.keys()) - states
    non_elements_of_alphabet = set(k[1] for k in state_transition_function.keys()) - alphabet
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

    # Checking that values valid states
    non_elements_of_states = set(state_transition_function.values()) - states
    if non_elements_of_states:
        raise StateTransitionFunctionError(
            "The following states passed to the state transition function are "
            f"not elements of the passed states: {non_elements_of_states}"
        )

    return


def validate_final_states(final_states: Set[S], states: Set[S]) -> None:

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
        alphabet: Set[A],
        states: Set[S],
        initial_state: S,
        state_transition_function: Dict[Tuple[S, A], S],
        final_states: Set[S],
    ) -> None:

        validate_alphabet(alphabet)
        self.alphabet = alphabet

        validate_states(states)
        self.states = states

        validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        validate_state_transition_function(state_transition_function, states, alphabet)
        self.state_transition_function = state_transition_function

        validate_final_states(final_states, states)
        self.final_states = final_states

        return

    def parses(self, seq: List[A]) -> bool:

        state_map = f"[{self.initial_state}]"
        current_state = self.initial_state
        for elem in seq:
            try:
                next_state = self.state_transition_function[(current_state, elem)]
            except KeyError:
                raise TransitionError(
                    f"The following encountered (state, input) pair is undefined: ({current_state},{elem})"
                ) from None
            state_map += f" --({elem})-> [{next_state}]"
            current_state = next_state
            if current_state in self.final_states:
                break

        print(state_map)

        return current_state in self.final_states

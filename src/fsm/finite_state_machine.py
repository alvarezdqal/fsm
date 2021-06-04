from dataclasses import dataclass
from typing import Dict, List, Set, Tuple, TypeVar

from fsm.exceptions import (
    AlphabetError,
    FinalStatesError,
    InitialStateError,
    StatesError,
    StateTransitionFunctionError,
    TransitionError,
)

Letter = TypeVar("Letter")  # elements of the 'alphabet'
State = TypeVar("State")  # elements of the 'states'


def __validate_alphabet(alphabet: Set[Letter]) -> None:

    # Checking non-empty set
    if not alphabet or not isinstance(alphabet, set):
        raise AlphabetError(f"The passed alphabet not a non-empty set: {alphabet}")

    # Checking that the elements are same type
    if len(alphabet) > 1:
        types = {type(lett) for lett in alphabet}
        if len(types) > 1:
            raise AlphabetError(f"The passed letters do not have same type: {types}")

    return


def __validate_states(states: Set[State]) -> None:

    # Checking non-empty set
    if not states or not isinstance(states, set):
        raise StatesError(f"The passed states not a non-empty set: {states}")

    # Checking that the elements are same type
    if len(states) > 1:
        types = {type(s) for s in states}
        if len(types) > 1:
            raise StatesError(f"The passed states do not have same type: {types}")

    return


def __validate_initial_state(initial_state: State, states: Set[State]) -> None:

    # Checking that initial state in states
    if initial_state not in states:
        raise InitialStateError(f"The passed initial state is not an element of passed states: '{initial_state}'")

    return


def __validate_state_transition_function(
    state_transition_function: Dict[Tuple[State, Letter], State],
    states: Set[State],
    alphabet: Set[Letter],
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
            "The following letters passed to the state transition function are "
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


def __validate_final_states(final_states: Set[State], states: Set[State]) -> None:

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
        alphabet: Set[Letter],
        states: Set[State],
        initial_state: State,
        state_transition_function: Dict[Tuple[State, Letter], State],
        final_states: Set[State],
    ) -> None:

        __validate_alphabet(alphabet)
        self.alphabet = alphabet

        __validate_states(states)
        self.states = states

        __validate_initial_state(initial_state, states)
        self.initial_state = initial_state

        __validate_state_transition_function(state_transition_function, states, alphabet)
        self.state_transition_function = state_transition_function

        __validate_final_states(final_states, states)
        self.final_states = final_states

        return

    def accepts(self, seq: List[Letter]) -> bool:

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

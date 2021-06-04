from unittest import TestCase

from fsm.exceptions import (
    AlphabetInitialisationError,
    FinalStatesInitialisationError,
    InitialStateInitialisationError,
    StatesInitialisationError,
)
from fsm.validation import (
    validate_alphabet,
    validate_final_states,
    validate_initial_state,
    validate_output_function,
    validate_state_transition_function,
    validate_states,
)


class TestValidation(TestCase):
    def test_validate_alphabet_non_set(self):
        alphabet = []
        self.assertRaises(AlphabetInitialisationError, validate_alphabet, alphabet)

    def test_validate_alphabet_empty(self):
        alphabet = set()
        self.assertRaises(AlphabetInitialisationError, validate_alphabet, alphabet)

    def test_validate_alphabet_different_types(self):
        alphabet = {3, "a", 7.2}
        self.assertRaises(AlphabetInitialisationError, validate_alphabet, alphabet)

    def test_validate_alphabet_pass(self):
        alphabet = {4, 9, 0}
        self.assertIsNone(validate_alphabet(alphabet))

    def test_validate_final_states_non_set(self):
        final_states = []
        states = {0, 1, 2}
        self.assertRaises(FinalStatesInitialisationError, validate_final_states, final_states, states)

    def test_validate_final_states_not_subset(self):
        final_states = {1, 2, 3}
        states = {0, 1, 2}
        self.assertRaises(FinalStatesInitialisationError, validate_final_states, final_states, states)

    def test_validate_final_states_pass(self):
        final_states = {0, 1}
        states = {0, 1, 2}
        self.assertIsNone(validate_final_states(final_states, states))

    def test_validate_initial_state_not_in_states(self):
        initial_state = 3
        states = {0, 1, 2}
        self.assertRaises(InitialStateInitialisationError, validate_initial_state, initial_state, states)

    def test_validate_initial_state_pass(self):
        initial_state = 1
        states = {0, 1, 2}
        self.assertIsNone(validate_initial_state(initial_state, states))

    def test_validate_output_function_non_tuple(self):
        pass  # TODO

    def test_validate_output_function_not_len_two(self):
        pass  # TODO

    def test_validate_output_function_fake_state_arg(self):
        pass  # TODO

    def test_validate_output_function_fake_letter_arg(self):
        pass  # TODO

    def test_validate_output_function_fake_state_value(self):
        pass  # TODO

    def test_validate_output_function_pass(self):
        pass  # TODO

    def test_validate_state_transition_function_non_tuple(self):
        pass  # TODO

    def test_validate_state_transition_function_not_len_two(self):
        pass  # TODO

    def test_validate_state_transition_function_fake_state_arg(self):
        pass  # TODO

    def test_validate_state_transition_function_fake_letter_arg(self):
        pass  # TODO

    def test_validate_state_transition_function_fake_state_value(self):
        pass  # TODO

    def test_validate_state_transition_function_pass(self):
        pass  # TODO

    def test_validate_states_non_set(self):
        states = []
        self.assertRaises(StatesInitialisationError, validate_states, states)

    def test_validate_states_empty(self):
        states = set()
        self.assertRaises(StatesInitialisationError, validate_states, states)

    def test_validate_states_different_types(self):
        states = {3, "a", 7.2}
        self.assertRaises(StatesInitialisationError, validate_states, states)

    def test_validate_states_pass(self):
        states = {4, 9, 0}
        self.assertIsNone(validate_states(states))

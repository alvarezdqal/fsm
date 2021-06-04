from unittest import TestCase

from fsm.exceptions import AlphabetInitialisationError
from fsm.validation import (
    validate_alphabet,
    validate_final_states,
    validate_initial_state,
    validate_output_function,
    validate_state_transition_function,
    validate_states,
)


class TestValidation(TestCase):
    def test_validate_alphabet_empty(self):
        alphabet = {}
        self.assertRaises(AlphabetInitialisationError, validate_alphabet, alphabet)

    def test_validate_alphabet_different_types(self):
        alphabet = {3, "a", 7.2}
        self.assertRaises(AlphabetInitialisationError, validate_alphabet, alphabet)

    def test_validate_alphabet(self):
        alphabet = {4, 9, 0}
        self.assertIsNone(validate_alphabet(alphabet))

    def test_validate_final_states(self):
        pass

    def test_validate_initial_state(self):
        pass

    def test_validate_output_function(self):
        pass

    def test_validate_state_transition_function(self):
        pass

    def test_validate_states(self):
        pass

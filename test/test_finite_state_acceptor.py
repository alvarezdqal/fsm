from unittest import TestCase

from fsm.exceptions import StateTransitionError
from fsm.finite_state_acceptor import FiniteStateAcceptor

fsa = FiniteStateAcceptor(
    input_alphabet={"a", "b", "c"},
    states={0, 1, 2},
    initial_state=0,
    state_transition_function={
        (0, "a"): 0,
        (0, "b"): 1,
        (0, "c"): 2,
        # Intentionally skipping (1, "a")
        (1, "b"): 1,
        (1, "c"): 0,
    },
    final_states={2},
)


class TestFiniteStateAcceptor(TestCase):
    def test_accepts_undefined(self):
        seq = ["b", "a"]
        self.assertRaises(StateTransitionError, fsa.accepts, seq)

    def test_accepts_true(self):
        seq = ["b", "c", "c"]
        self.assertTrue(fsa.accepts(seq))
        pass

    def test_accepts_false(self):
        seq = ["a", "a", "b"]
        self.assertFalse(fsa.accepts(seq))

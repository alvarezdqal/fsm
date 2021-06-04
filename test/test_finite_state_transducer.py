from unittest import TestCase

from fsm.exceptions import StateTransitionError, TransductionError
from fsm.finite_state_transducer import FiniteStateTransducer

fst = FiniteStateTransducer(
    input_alphabet={"a", "b", "c"},
    states={0, 1, 2},
    initial_state=0,
    state_transition_function={
        (0, "a"): 0,
        (0, "b"): 1,
        (0, "c"): 2,
        (1, "a"): 2,
        # Intentionally skipping (1, "b")
        (1, "c"): 0,
    },
    output_alphabet={
        0.0,
        0.1,
        0.2,
        1.0,
        1.1,
        1.2,
    },
    output_function={
        (0, "a"): 0.0,
        (0, "b"): 0.1,
        # Intentionally skipping (0, "c")
        (1, "a"): 1.0,
        (1, "b"): 1.1,
        (1, "c"): 1.2,
    },
)


class TestFiniteStateTransducer(TestCase):
    def test_transduce_undefined_transition(self):
        seq = ["b", "b"]
        self.assertRaises(StateTransitionError, fst.transduce, seq)

    def test_transduce_undefined_transduction(self):
        seq = ["b", "c", "c"]
        self.assertRaises(TransductionError, fst.transduce, seq)

    def test_transduce(self):
        seq = ["b", "c", "b", "a"]
        self.assertEqual(fst.transduce(seq), [0.1, 1.2, 0.1, 1.0])
        pass

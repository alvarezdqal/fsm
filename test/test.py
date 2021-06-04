from fsm.finite_state_machine import FiniteStateMachine


def main() -> None:

    fsm = FiniteStateMachine(
        alphabet={"a", "b", "c"},
        states={0, 1, 2, 3, 4},
        initial_state=0,
        state_transition_function={
            (0, "a"): 0,
            (0, "b"): 1,
            (0, "c"): 2,
            (1, "a"): 3,
            (1, "b"): 4,
            (1, "c"): 1,
            (2, "a"): 2,
            (2, "b"): 0,
            (2, "c"): 4,
        },
        final_states={3, 4},
    )

    seq = ["a", "a", "c", "b", "b", "c"]
    accepts = fsm.accepts(seq, print_path=True)
    if accepts:
        print(f"The passed sequence is accepted: {seq}")
    else:
        print(f"The passed sequence is not accepted: {seq}")

    return


if __name__ == "__main__":
    main()

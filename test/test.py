from fsm.finite_state_machine import FiniteStateMachine


def main() -> None:

    fsm = FiniteStateMachine(
        alphabet={"hello", "there", "world"},
        states={0, 1, 2, 3, 4},
        initial_state=0,
        state_transition_function={
            (0, "hello"): 0,
            (0, "there"): 1,
            (0, "world"): 2,
            (1, "hello"): 3,
            (1, "there"): 4,
            (1, "world"): 1,
            (2, "hello"): 2,
            (2, "there"): 0,
            (2, "world"): 4,
        },
        final_states={3, 4},
    )

    seq = ["hello", "hello", "world", "hello", "there", "world", "world"]
    accepts = fsm.accepts(seq, print_path=True)
    if accepts:
        print("The passed sequence is accepted")
    else:
        print("The passed sequence is not accepted.")

    return


if __name__ == "__main__":
    main()

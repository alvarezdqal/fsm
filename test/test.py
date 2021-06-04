from fsm.finite_state_machine import FiniteStateMachine


def main() -> None:

    fsm = FiniteStateMachine(
        alphabet={"a", "b", "c"},
        states={"i", "x", "y", "t1", "t2"},
        initial_state="i",
        state_transition_function={
            ("i", "a"): "i",
            ("i", "b"): "x",
            ("i", "c"): "y",
            ("x", "a"): "t1",
            ("x", "b"): "t2",
            ("x", "c"): "x",
            ("y", "a"): "y",
            ("y", "b"): "i",
            ("y", "c"): "t2",
        },
        final_states={"t1", "t2"},
    )

    # seq = ["a", "a", "c", "b", "b", "a"]
    seq = ["a", "a", "c", "b", "b", "c"]
    accepts = fsm.accepts(seq, print_path=True)
    as_string = str.join("", seq)
    if accepts:
        print(f"The passed sequence '{as_string}' accepts")
    else:
        print(f"The passed sequence '{as_string}' does not parse")

    return


if __name__ == "__main__":
    main()

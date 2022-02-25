import graphform


def main():

    pairs = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("B", "C"), ("C", "D"),
             ("D", "E"), ("E", "B"), ("B", "F"), ("C", "F"), ("D", "F"), ("E", "F")]

    graphform.Render(pairs)


if __name__ == "__main__":
    main()

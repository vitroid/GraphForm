import graphform

def main():

    pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
            ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
            ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]

    graphform.Render(pairs)


if __name__ == "__main__":
    main()
import graphform

def main():

    # pentagonal bipyramid
    pairs = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("Z", "N"),
             ("A", "Z"), ("B", "Z"), ("C", "Z"), ("D", "Z"), ("E", "Z"),
             ("A", "N"), ("B", "N"), ("C", "N"), ("D", "N"), ("E", "N"), ]

    graphform.Render(pairs)


if __name__ == "__main__":
    main()
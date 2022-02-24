from logging import getLogger, basicConfig, INFO, DEBUG
import graphform

def main():
    # basicConfig(level=INFO, format="%(levelname)s %(message)s")
    basicConfig(level=INFO, format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    pairs  = [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("Z","N"),
            ("A","Z"), ("B","Z"), ("C","Z"), ("D","Z"), ("E","Z"), ("F","Z"),
            ("A","N"), ("B","N"), ("C","N"), ("D","N"), ("E","N"), ("F","N"),]

    graphform.Render(pairs)


if __name__ == "__main__":
    main()
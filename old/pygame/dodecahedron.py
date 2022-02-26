from logging import getLogger, basicConfig, INFO, DEBUG
import graphform


def main():
    # basicConfig(level=INFO, format="%(levelname)s %(message)s")
    basicConfig(level=INFO, format="%(levelname)s %(message)s")
    logger = getLogger()
    logger.debug("Debug mode.")

    # Dodecahedron
    pairs = [("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("4", "0"),
             ("0", "5"), ("1", "6"), ("2", "7"), ("3", "8"), ("4", "9"),
             ("10", "5"), ("11", "6"), ("12", "7"), ("13", "8"), ("14", "9"),
             ("10", "6"), ("11", "7"), ("12", "8"), ("13", "9"), ("14", "5"),
             ("10", "15"), ("11", "16"), ("12", "17"), ("13", "18"), ("14", "19"),
             ("19", "15"), ("15", "16"), ("16", "17"), ("17", "18"), ("18", "19"), ]
    # does not work. why?
    # なぜなら、三角形を表示するモードでは五角形は表示できないから。
    # -stiff.pyのほうを使う必要があるがまだ移植できてない。
    graphform.Render(pairs)


if __name__ == "__main__":
    main()

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(And(AKnight, AKnave), AKnight),
    Biconditional(Not(And(AKnight, AKnave)), AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(And(AKnave, BKnave), AKnight),
    Biconditional(Not(And(AKnave, BKnave)), AKnave),
    Or(BKnave, BKnight),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)), AKnight),
    Biconditional(Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))), AKnave),
    Biconditional(Or(And(AKnight, BKnave), And(AKnave, BKnight)), BKnight),
    Biconditional(Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))), BKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(And(Biconditional(AKnight, AKnight), Biconditional(Not(AKnight), AKnave)), And(Biconditional(AKnave, AKnight), Biconditional(Not(AKnave), AKnave))),
    Biconditional(And(Biconditional(AKnave, AKnight), Biconditional(Not(AKnave), AKnave)), BKnight),
    Biconditional(Not(And(Biconditional(AKnave, AKnight), Biconditional(Not(AKnave), AKnave))), BKnave),
    Biconditional(CKnave, BKnight),
    Biconditional(Not(CKnave), BKnave),
    Biconditional(AKnight, CKnight),
    Biconditional(Not(AKnight), CKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

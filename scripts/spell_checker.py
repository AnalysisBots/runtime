import sys

from enchant.checker import SpellChecker

def has_error(filename):
    with open(filename, "r") as file_to_check:
        data = file_to_check.read()
        checker = SpellChecker("en_US")
        checker.set_text(data)
        for err in checker:
            return true
        return false

def suggest_correction(filename):
    with open(filename, "r") as file_to_check:
        data = file_to_check.read()
        checker = SpellChecker("en_US")
        checker.set_text(data)
        for err in checker:
            # avoid IndexOutOfBounds
            err.replace(checker.suggest()[0])
        return checker.get_text()

def auto_correct(filename):
    correction = suggest_correction(filename)
    with open(filename, "w") as file_to_correct:
        file_to_correct.write(correction)

if __name__ == '__main__':
    auto_correct(sys.argv[1])

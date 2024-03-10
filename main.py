import sys

# regex_f = open(sys.argv[1], "r")
# texts_f = open(sys.argv[2], "r")

regex_f = open("regex1.txt", "r")
texts_f = open("retazce1.txt", "r")

regex = [None] + regex_f.readlines()
texts = [None] + texts_f.readlines()

print(regex)
print(texts)


def regex_magic():
    pass


def empty_string():
    pass


def one_symbol():
    pass


def union():
    pass


def concat():
    pass


def iteration():
    pass

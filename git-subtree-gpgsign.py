#!/usr/bin/env python
from sys import argv
import getopt


def subtree(fname: str, reverse=False, encoding="UTF-8"):
    with open(fname, "r", encoding=encoding) as f:
        text = f.read()
    if reverse:
        text = text.replace("git commit-tree -S \"", "git commit-tree \"")
    else:
        text = text.replace("git commit-tree \"", "git commit-tree -S \"")
    with open(fname, "wb") as f:
        f.write(text.encode(encoding))
    print("done!")


reverse = False
filename = None
opts, args = getopt.getopt(argv[1:], "-r:-f:-h", ["filename=", "help"])
for s in args:
    filename = s
for o, a in opts:
    if o in ("-r"):
        reverse = True
    if o in ("-f", "--filename"):
        filename = a
    if o in ("-h", "--help"):
        print("{} [option]:".format(argv[0]))
        print("options:")
        print("\t-r\treverse")
        print("arguments:")
        print("\t-f,--filename [git-subtree]")
        exit()
if filename:
    subtree(filename, reverse)

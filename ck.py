#!/usr/bin/env python
import hashlib
import sys
import io
import os


README = "README.txt"
ENCODING = "UTF-8"


def hash(name: str) -> str:
    ret = hashlib.sha256()
    with open(name, "rb") as f:
        while True:
            data = f.read(io.DEFAULT_BUFFER_SIZE)
            if not data:
                break
            ret.update(data)
    return ret.hexdigest()


def scan(path: str = '.') -> list:
    ret = list()
    path = os.path.relpath(path)
    names = os.listdir(path)
    if README in names:
        names.remove(README)
    for name in names:
        name = os.path.join(path, name)
        if os.path.isfile(name):
            ret.append(name)
    return ret


def read(path: str = '.') -> dict:
    ret = dict()
    name = os.path.join(path, README)
    if not os.path.exists(name):
        return ret
    with open(name, "r", encoding=ENCODING) as f:
        text = f.read()
    for line in text.split('\n'):
        if len(line) < 66 or line[64] != ' ':
            continue
        hash = line[:64]
        try:
            int(hash, 16)
        except:
            continue
        name = line[65:].strip()
        if name[0] == "*":
            name = name[1:]
        ret[name] = hash
    return ret


def check(path: str = '.') -> str:
    ret = str()
    path = os.path.relpath(path)
    info = read(path)
    for name in scan(path):
        sha = hash(name)
        name = os.path.basename(name)
        line = sha + ' ' + name + '\n'
        if info.get(name):
            if info.get(name) != sha:
                print("修改", name)
                print("  旧", info.get(name))
                print("  新", sha)
            else:
                print("OK", name)
        else:
            print(line, end='')
            ret += line
    return ret


def write(text: str, path: str = '.') -> None:
    name = os.path.join(path, README)
    with open(name, "ab+") as f:
        f.write(text.encode(ENCODING))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        write(check())
    for path in sys.argv[1:]:
        write(check(path), path)

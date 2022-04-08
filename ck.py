#!/usr/bin/env python
import hashlib
import sys
import io
import os


README = "README.txt"
ENCODING = "UTF-8"


def hash(name: str) -> str:
    ret = hashlib.sha256()
    f = open(name, "rb")
    while True:
        data = f.read(io.DEFAULT_BUFFER_SIZE)
        if not data:
            break
        ret.update(data)
    f.close()
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


def check(path: str = '.') -> tuple:
    ret = list()
    isok = True
    path = os.path.relpath(path)
    info = read(path)
    names = scan(path)
    for i in range(len(names)):
        name = names[i]
        sha = hash(name)
        names[i] = name = os.path.basename(name)
        if info.get(name):
            if info.get(name) != sha:
                print("修改", name)
                print("  旧", info.get(name))
                print("  新", sha)
                isok = False
        else:
            ret.append((sha, name))
            print(sha, name)
            isok = False
    if isok:
        print("OK")
    for name in info.keys():
        if name not in names:
            print("缺失", name)
    return tuple(ret)


def write(info: tuple, path: str = '.') -> None:
    name = os.path.join(path, README)
    f = open(name, "ab+")
    for line in info:
        text = "{} {}\n".format(*line)
        f.write(text.encode(ENCODING))
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        write(check())
    for path in sys.argv[1:]:
        write(check(path), path)

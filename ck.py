#!/usr/bin/env python
import hashlib
import getopt
import sys
import io
import os


class ck:
    README = "README"
    ENCODING = "UTF-8"

    def __init__(self, path: str = ".", hash: str = "sha256") -> None:
        self._hash = hash
        self._data = list()
        self._path = os.path.relpath(path)
        self._size = hashlib.new(hash).digest_size << 1
        self._name = os.path.join(self._path, self.README + '.' + hash)

    def hash(self, name: str) -> str:
        ret = hashlib.new(self._hash)
        f = open(name, "rb")
        data = f.read(io.DEFAULT_BUFFER_SIZE)
        while data:
            ret.update(data)
            data = f.read(io.DEFAULT_BUFFER_SIZE)
        f.close()
        return ret.hexdigest()

    def scan(self) -> list:
        ret = list()
        names = os.listdir(self._path)
        for name in names:
            if self.README in name:
                continue
            name = os.path.join(self._path, name)
            if os.path.isfile(name):
                ret.append(name)
        return ret

    def read(self) -> dict:
        ret = dict()
        if not os.path.exists(self._name):
            return ret
        with open(self._name, "r", encoding=self.ENCODING) as f:
            text = f.read()
        for line in text.split('\n'):
            if len(line) < self._size + 2 or line[self._size] != ' ':
                continue
            hash = line[: self._size]
            try:
                int(hash, 16)
            except:
                continue
            name = line[self._size + 1 :].strip()
            if name[0] == "*":
                name = name[1:]
            ret[name] = hash
        return ret

    def check(self):
        isok = True
        info = self.read()
        names = self.scan()
        for i in range(len(names)):
            name = names[i]
            sha = self.hash(name)
            name = os.path.basename(name)
            record = info.get(name)
            names[i] = name
            if record:
                if record != sha:
                    print("修改", os.path.join(self._path, name))
                    print("  旧", record)
                    print("  新", sha)
                    isok = False
            else:
                self._data.append((sha, name))
                print(sha, os.path.join(self._path, name))
                isok = False
        if isok:
            print("OK")
        for name in info.keys():
            if name not in names:
                print("缺失", os.path.join(self._path, name))
        return self

    def write(self) -> None:
        f = open(self._name, "ab+")
        for line in self._data:
            text = "{} {}\n".format(*line)
            f.write(text.encode(self.ENCODING))
        f.close()


if __name__ == "__main__":

    def usage() -> None:
        help = "{} [option] [dirs]\n".format(sys.argv[0])
        help += "-l --list\t\t- 显示可用算法\n"
        help += "-a --algorithm [hash]\t- 选择校验算法，默认 sha256\n"
        help += "-h --help\t\t- 显示此帮助信息并退出"
        print(help)

    opt_algorithm = "sha256"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:l", ["help", "list", "algorithm="])
    except getopt.GetoptError:
        exit(usage())
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            exit(usage())
        elif opt in ("-l", "--list"):
            exit(print(*hashlib.algorithms_available, sep='\n'))
        elif opt in ("-a", "--algorithm"):
            try:
                hashlib.new(arg)
                opt_algorithm = arg
            except Exception as e:
                exit(print(e))

    if len(args) == 0:
        exit(ck(hash=opt_algorithm).check().write())
    for arg in args:
        ck(arg, hash=opt_algorithm).check().write()

#!/usr/bin/env python
import hashlib
import getopt
import sys
import os


opt_verbose = False
opt_remove = False
opt_rename = False
opt_empty = False
opt_files = []
opt_dirs = []


def usage() -> None:
    help = "{} [option] [dirs]\n".format(sys.argv[0])
    help += "-v --verbose\t- 详细显示进行的步骤\n"
    help += "-r --remove\t- 删除文件\n"
    help += "-R --rename\t- 重命名文件\n"
    help += "-e --empty\t- 选择空文件\n"
    help += "-h --help\t- 显示此帮助信息并退出"
    print(help)


try:
    opts, args = getopt.getopt(
        sys.argv[1:], "hvrRe", ["help", "verbose", "remove", "rename", "empty"]
    )
except getopt.GetoptError:
    exit(usage())
for arg in args:
    if os.path.isfile(arg):
        opt_files.append(arg)
    elif os.path.isdir(arg):
        opt_dirs.append(arg)
    else:
        print("未知", arg)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        exit(usage())
    elif opt in ("-v", "--verbose"):
        opt_verbose = True
    elif opt in ("-r", "--remove"):
        opt_remove = True
    elif opt in ("-R", "--rename"):
        opt_rename = True
    elif opt in ("-e", "--empty"):
        opt_empty = True


def exe_remove(filenames: list) -> None:
    removes = set()
    if not filenames:
        return
    for i, file1 in enumerate(filenames):
        size1 = os.path.getsize(file1)
        if opt_empty and size1 == 0:
            removes.add(file1)
            continue
        m1 = ''
        for j, file2 in enumerate(filenames):
            if i == j:
                continue
            size2 = os.path.getsize(file2)
            if size1 == size2:
                if m1 == '':
                    with open(file1, "rb") as f1:
                        m1 = hashlib.md5(f1.read()).hexdigest()
                with open(file2, "rb") as f2:
                    m2 = hashlib.md5(f2.read()).hexdigest()
                if m1 == m2:
                    if os.path.getmtime(file1) > os.path.getmtime(file2):
                        removes.add(file1)
                    else:
                        removes.add(file2)
    for filename in removes:
        if opt_remove:
            os.remove(filename)
        if opt_verbose:
            print("删除", filename)


def exe_rename(filenames: list) -> None:
    sizes = []
    renames = []
    if not filenames:
        return
    for filename in filenames:
        sizes.append(os.path.getsize(filename))
    namemax = len("%u" % max(sizes))
    for i, filename in enumerate(filenames):
        dirpath, basename = os.path.split(filename)
        namefix = os.path.splitext(basename)[-1]
        namebase = "%0{}u".format(namemax) % (sizes[i])
        sizename = os.path.join(dirpath, namebase + namefix).replace('\\', '/')
        idx = 1
        while sizename in renames:
            sizename = os.path.join(
                dirpath, namebase + '-%u' % (idx) + namefix
            ).replace('\\', '/')
            idx += 1
        renames.append(sizename)
    for i, filename in enumerate(filenames):
        if filename != renames[i] and not os.path.exists(renames[i]):
            if opt_rename:
                os.rename(filename, renames[i])
            if opt_verbose:
                dirpath, srcname = os.path.split(filename)
                dirpath, dstname = os.path.split(renames[i])
                if not dirpath:
                    dirpath = '.'
                print("{}/{{{} <= {}}}".format(dirpath, dstname, srcname))


def exe_walk(dir: str, func):
    for dirpath, dirnames, filenames in os.walk(dir):
        files = []
        for filename in filenames:
            filename = os.path.join(dirpath, filename).replace('\\', '/')
            files.append(filename)
        if files:
            func(files)
        del files
        for dirname in dirnames:
            dirname = os.path.join(dirpath, dirname).replace('\\', '/')
            exe_walk(dirname, func)


if __name__ == "__main__":
    for dir in opt_dirs:
        exe_walk(dir, exe_remove)
        exe_walk(dir, exe_rename)
    exe_remove(opt_files)
    exe_rename(opt_files)

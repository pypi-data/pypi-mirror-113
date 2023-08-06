import sys
from miquido_latest_version_check import get_latest


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        eprint('Too few arguments')
    if len(sys.argv) == 2:
        print(get_latest(sys.argv[1]))
    else:
        print(get_latest(sys.argv[1], sys.argv[2]))

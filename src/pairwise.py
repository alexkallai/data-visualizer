
# about 40% slower than itertools.pairwise,
# but that's available from python 3.10 only
def pairwise(iterable):
    for x in zip(iterable, iterable[1:]):
        yield x


if __name__ == "__main__":
    print(pairwise(range(10)))
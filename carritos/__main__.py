import sys

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    print("Main module speaking")

if __name__ == '__main__':
    sys.exit(main())

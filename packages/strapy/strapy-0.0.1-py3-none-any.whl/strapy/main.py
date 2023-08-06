from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        prog="strapy",
        description="Bootstrap CLI Framework"
    )
    parser.set_defaults(func=lambda __: parser.print_help())

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

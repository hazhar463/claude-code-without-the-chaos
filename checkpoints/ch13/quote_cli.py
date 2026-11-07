import argparse

from quote import total_cents


def format_usd(cents):
    return f"USD {cents // 100}.{cents % 100:02d}"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Calculate a workshop quote; no booking is made."
    )
    parser.add_argument("unit_cents", type=int,
                        help="price per seat in whole cents")
    parser.add_argument("quantity", type=int,
                        help="whole seats, from 1 through 200")
    args = parser.parse_args(argv)

    try:
        result = total_cents(args.unit_cents, args.quantity)
    except ValueError as error:
        parser.error(str(error))

    print(f"Total: {format_usd(result)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

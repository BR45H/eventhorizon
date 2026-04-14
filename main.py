from core.exceptions import EventHorizonError
from core import output
from cli.parser import build_parser

def main() -> None:
    parser = build_parser()

    try:
        args = parser.parse_args()
        args.func(args)

    except EventHorizonError as exc:
        output.error(str(exc))
        
if __name__ == "__main__":
    main()
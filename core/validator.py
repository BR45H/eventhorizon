from core.exceptions import ValidationError

def validate_smb_connect_args(args) -> None:
    if args.anonymous and (args.user or args.password):
        raise ValidationError(
            "--anonymous cannot be used with other authentication options"
        )
    if args.user and not args.password:
        raise ValidationError("--user requires --password")
    if args.password and not args.user:
        raise ValidationError("--password requires --user")
    
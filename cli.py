# cli.py
import argparse
import utils

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="chain-guard: software supply chain analysis tool")

    # Add subcommands for each utility function
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add arguments for other functions
    subparsers.add_parser("pip-audit", help="Run pip-audit")

    grype_parser = subparsers.add_parser("grype", help="Run Grype against a target")
    grype_parser.add_argument("target", type=str, help="Target to analyze")
    grype_parser.add_argument("--output", type=str, help="Path to save the output report (JSON)")

    trivy_parser = subparsers.add_parser("trivy", help="Run Trivy against a target")
    trivy_parser.add_argument("target", type=str, help="Target to analyze")
    trivy_parser.add_argument("--output", type=str, help="Path to save the output report (JSON)")


    sbom_parser = subparsers.add_parser("generate-sbom", help="Generate an SBOM using Syft")
    sbom_parser.add_argument("target", type=str, help="Target to analyze")
    sbom_parser.add_argument("--output", type=str, help="Path to save the output report (JSON)")


    hash_parser = subparsers.add_parser("hash", help="Calculate a hash for a file")
    hash_parser.add_argument("file", type=str, help="File to hash")
    hash_parser.add_argument("--output", type=str, help="Path to save the output report (JSON)")


    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the subcommand
    if args.command == "pip-audit":
        print(utils.run_pip_audit())

    elif args.command == "grype":
        result = utils.run_grype(args.target)
        if args.output:
            with open(args.output, "w") as f:
                f.write(result)
            print(f"Results saved to {args.output}")
        else:
            print(result)

    elif args.command == "trivy":
        result = utils.run_trivy(args.target)
        if args.output:
            with open(args.output, "w") as f:
                f.write(result)
            print(f"Results saved to {args.output}")
        else:
            print(result)

    elif args.command == "generate-sbom":
        result = utils.generate_sbom(args.target)
        if args.output:
            with open(args.output, "w") as f:
                f.write(result)
            print(f"SBOM saved to {args.output}")
        else:
            print(result)

    elif args.command == "hash":
        result = utils.calculate_hash(args.target)
        if args.output:
            with open(args.output, "w") as f:
                f.write(result)
            print(f"Hash saved to {args.output}")
        else:
            print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
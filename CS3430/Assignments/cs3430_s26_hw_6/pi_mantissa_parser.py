# pi_parse_pi_mantissa.py
# this utility allows us to parse "99_999DigitsOfPi.txt"

def parse_pi_mantissa(filename: str, n_digits: int) -> str:
    """
    Parse exactly n_digits of the decimal mantissa of pi from a reference file.

    Parsing rules:
    - Ignore all characters before and including the first occurrence of '3.'
    - Keep only decimal digits ('0'–'9')
    - Remove all whitespace (spaces, newlines, tabs)
    - Return exactly n_digits digits of the mantissa as a single string

    This function deliberately eliminates formatting differences so that
    hashing and verification depend only on mathematical content, not layout.
    """

    # Read the entire file as text
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # Find the start of the decimal expansion ("3.")
    idx = text.find("3.")
    if idx == -1:
        raise ValueError("Reference file does not contain '3.'")

    # Keep everything after the decimal point
    mantissa_text = text[idx + 2:]

    # Filter out all non-digit characters (this removes whitespace)
    digits = [ch for ch in mantissa_text if ch.isdigit()]

    if len(digits) < n_digits:
        raise ValueError(
            f"Reference file contains only {len(digits)} digits, "
            f"but {n_digits} were requested."
        )

    # Return exactly the first n_digits of the mantissa
    return "".join(digits[:n_digits])

if __name__ == "__main__":
    # This main block allows the parser to be used as a command-line tool.
    #
    # Example usage:
    #   python parse_pi.py OneHundredDigitsOfPi.txt 100000 > pi_ref_100k.txt
    #
    # This prints exactly N digits of the pi mantissa to stdout, which can
    # be redirected to a file using standard shell redirection.

    import argparse

    # Create a command-line argument parser
    parser = argparse.ArgumentParser(
        description=(
            "Extract exactly N digits of the decimal mantissa of pi from "
            "a reference file, removing all whitespace and formatting."
        )
    )

    # Positional argument: path to the reference file
    parser.add_argument(
        "filename",
        type=str,
        help="Path to the reference file containing digits of pi"
    )

    # Positional argument: number of mantissa digits to extract
    parser.add_argument(
        "n_digits",
        type=int,
        help="Number of decimal mantissa digits to extract"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the canonical parser
    mantissa = parse_pi_mantissa(args.filename, args.n_digits)

    # Print the result to stdout.
    # Users are expected to redirect this output to a file if needed.
    print(mantissa)

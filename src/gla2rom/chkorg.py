#!/usr/bin/env python3
import sys
import re

def parse_bytes_here(filename):
    pattern = re.compile(
        r'^(BYTES_HERE_[A-Za-z0-9_]+).*?Number\s+([0-9A-Fa-f\-]+)h'
    )

    results = []

    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if not match:
                continue

            full_tag = match.group(1)
            hex_str = match.group(2)

            tag = full_tag.replace("BYTES_HERE_", "")

            value = int(hex_str, 16)
            signed_value = value
            negative = value < 0

            #if value & 0x8000:
            #    signed_value = value - 0x10000
            #    negative = True
            #else:
            #    signed_value = value
            #    negative = False

            results.append((tag, hex_str, signed_value, negative))

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: chk_bh.py <filename> [/V]")
        sys.exit(1)

    err = False
    filename = sys.argv[1]
    verbose = any(arg.upper() == "/V" for arg in sys.argv[2:])

    entries = parse_bytes_here(filename)

    for tag, hex_str, signed_value, negative in entries:
        if verbose or negative:
            flag = " *** ERROR: OUT OF BYTES" if negative else ""
            print(f"{tag}: {flag} {signed_value} bytes ({hex_str}h) ***")
            if negative:
                err = True

    if err:
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# save_as_fortigate.py
# Usage:
#   save_as_fortigate.py <MM.DD_유해IP.txt> [--no-dedupe] [--exclude-private] [--year 2025]
#
# Behavior:
#   - Extracts MM.DD from filename, builds YYYYMMDD (default year=2025).
#   - Extracts IPv4 only (ignores domains/URLs/labels), preserves original order.
#   - Deduplicates by default (can disable with --no-dedupe).
#   - Writes UTF-8 "fortigate_block_YYYYMMDD_script.txt".

import re, sys, ipaddress, argparse, pathlib

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except Exception:
        return False

def is_private(ip):
    return ipaddress.IPv4Address(ip).is_private

def parse_args():
    p = argparse.ArgumentParser(description="Generate FortiGate block script from MM.DD_유해IP.txt")
    p.add_argument("input_file", help="input filename (MM.DD_유해IP.txt)")
    p.add_argument("--no-dedupe", action="store_true", help="Do not deduplicate (keep duplicates)")
    p.add_argument("--exclude-private", action="store_true", help="Exclude RFC1918 private ranges")
    p.add_argument("--year", type=int, default=2025, help="Year for YYYYMMDD (default: 2025)")
    return p.parse_args()

def extract_date_from_name(name, year):
    m = re.search(r"(\d{2})\.(\d{2})", name)
    if not m:
        raise SystemExit("Filename does not contain MM.DD pattern")
    mm, dd = m.groups()
    return f"{year}{mm}{dd}"

def main():
    args = parse_args()
    p = pathlib.Path(args.input_file)
    if not p.exists():
        raise SystemExit(f"File not found: {p}")
    text = p.read_text(encoding="utf-8", errors="ignore")

    # Extract & validate IPv4
    found = IP_RE.findall(text)
    valid = [ip for ip in found if is_valid_ipv4(ip)]
    if args.exclude_private:
        valid = [ip for ip in valid if not is_private(ip)]

    # Keep original order; dedupe by default
    if args.no_dedupe:
        ordered = valid[:]
    else:
        seen = set()
        ordered = []
        for ip in valid:
            if ip not in seen:
                seen.add(ip)
                ordered.append(ip)

    yyyymmdd = extract_date_from_name(p.name, args.year)
    out_name = f"fortigate_block_{yyyymmdd}_script.txt"

    # Build FortiGate CLI blocks
    lines = ["config firewall address"]
    for ip in ordered:
        lines.append(f'edit "Block-{yyyymmdd}-{ip}"')
        lines.append(f"    set subnet {ip}/32")
        lines.append("next")
    lines.append("end")
    content = "\n".join(lines) + "\n"

    pathlib.Path(out_name).write_text(content, encoding="utf-8")
    print(f"Wrote {len(ordered)} entries to {out_name} (UTF-8)")

if __name__ == "__main__":
    main()
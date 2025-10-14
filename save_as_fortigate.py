#!/usr/bin/env python3
import re, ipaddress, pathlib, os

def valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except:
        return False

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def process_file(path: pathlib.Path, year=2025):
    mmdd = re.search(r"(\d{2})\.(\d{2})", path.name)
    if not mmdd:
        print(f"❌ {path.name}: 파일명에서 MM.DD 패턴을 찾지 못함")
        return
    yyyymmdd = f"{year}{mmdd.group(1)}{mmdd.group(2)}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    ips = [ip for ip in IP_RE.findall(text) if valid_ipv4(ip)]
    seen, ordered = set(), []
    for ip in ips:
        if ip not in seen:
            seen.add(ip)
            ordered.append(ip)
    lines = ["config firewall address"]
    for ip in ordered:
        lines.append(f'edit "Block-{yyyymmdd}-{ip}"')
        lines.append(f"    set subnet {ip}/32")
        lines.append("next")
    lines.append("end")
    out_name = f"fortigate_block_{yyyymmdd}_script.txt"
    pathlib.Path(out_name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ {path.name} → {out_name} ({len(ordered)} IP)")

def main():
    txts = list(pathlib.Path(".").glob("*유해IP.txt"))
    if not txts:
        print("⚠️ 변환할 *_유해IP.txt 파일이 없습니다.")
    else:
        for t in txts:
            process_file(t)
    os.system("pause")

if __name__ == "__main__":
    main()

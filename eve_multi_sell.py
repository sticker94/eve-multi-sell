#!/usr/bin/env python3
import math
import requests
import pyperclip
import sys

# —— CONFIG ——
ESI_BASE        = "https://esi.evetech.net/latest"
IDS_ENDPOINT    = f"{ESI_BASE}/universe/ids/"
MARKET_ENDPOINT = f"{ESI_BASE}/markets/10000002/orders/"  # Jita = 10000002
DATASOURCE      = "tranquility"
LANG            = "en"

# —— UTILITIES ——

def tick_size(price: float) -> float:
    """One‐tick size under CCP’s four‐significant‐figures rule."""
    D = math.floor(math.log10(price)) + 1
    return 10 ** (D - 4)

def undercut(price: float) -> float:
    """Compute one tick below the given price."""
    return price - tick_size(price)

def fetch_jita_price(type_id: int) -> float:
    """Return the lowest current Jita sell price for a given type ID."""
    r = requests.get(
        MARKET_ENDPOINT,
        params={"type_id": type_id, "order_type": "sell", "page": 1}
    )
    r.raise_for_status()
    orders = r.json()
    return min(o["price"] for o in orders)

# —— MAIN FLOW ——

def main():
    # 1) Read your lines from stdin or (if no pipe) from the clipboard
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raw = pyperclip.paste()
    lines = [l.strip() for l in raw.splitlines() if l.strip()]

    # 2) Parse into (display_name, clean_name, qty)
    items = []
    for ln in lines:
        if "\t" in ln:
            name, qty_s = ln.split("\t", 1)
        else:
            parts = ln.rsplit(None, 1)
            if len(parts) == 2 and parts[1].isdigit():
                name, qty_s = parts
            else:
                name, qty_s = ln, ""
        qty = int(qty_s) if qty_s.isdigit() else None
        clean = name.replace("'", "").strip()
        items.append((name, clean, qty))

    # 3) Bulk-resolve all distinct clean names → type_ids
    distinct = list({clean for (_, clean, _) in items})
    resp = requests.post(
        IDS_ENDPOINT,
        params={"datasource": DATASOURCE, "language": LANG},
        json=distinct,
        headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json()

    # map clean_name → type_id (inventory_types only)
    id_map = {entry["name"]: entry["id"]
              for entry in data.get("inventory_types", [])}

    # 4) For each item, look up its ID, fetch price, undercut, format
    out_lines = []
    for disp, clean, qty in items:
        try:
            tid = id_map.get(clean)
            if not tid:
                raise KeyError(f"no ID for '{clean}'")
            price = fetch_jita_price(tid)
            u = undercut(price)
            # format price with up to 4 decimals, strip trailing zeros
            ps = f"{u:.4f}".rstrip("0").rstrip(".")
            if qty is not None:
                out_lines.append(f"{disp}\t{ps}\t{qty}")
            else:
                out_lines.append(f"{disp}\t{ps}")
        except Exception as e:
            out_lines.append(f"# ERROR: {disp}: {e}")

    # 5) Copy back to clipboard and echo
    result = "\n".join(out_lines)
    pyperclip.copy(result)
    print(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Superavit — Bank Statement Parser

Detects format/bank and parses bank statements into normalized JSON.

Usage:
    python parse_statement.py detect <filepath>
    python parse_statement.py parse <filepath> [bank]

Output: JSON to stdout, errors to stderr.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORTED_BANKS = {
    "nubank": {"formats": ["csv", "pdf"], "csv_encoding": "utf-8-sig", "csv_sep": ","},
    "itau": {"formats": ["csv", "ofx"], "csv_encoding": "latin-1", "csv_sep": ";"},
    "bradesco": {"formats": ["ofx"]},
    "inter": {"formats": ["csv"], "csv_encoding": "utf-8-sig", "csv_sep": ";"},
}

# Header patterns for bank detection (lowercased)
BANK_CSV_HEADERS = {
    "nubank": ["date", "category", "title", "amount"],
    "itau": ["data", "lançamento", "valor"],
    "inter": ["data lançamento", "descrição", "valor", "saldo"],
}

# OFX BANKID mapping
OFX_BANKIDS = {
    "0341": "itau",
    "0237": "bradesco",
}


# ---------------------------------------------------------------------------
# Format Detection
# ---------------------------------------------------------------------------

def detect_format(filepath: str) -> str:
    """Detect file format by extension and content."""
    path = Path(filepath)
    ext = path.suffix.lower()

    if ext == ".csv":
        return "csv"
    elif ext in (".ofx", ".qfx"):
        return "ofx"
    elif ext == ".pdf":
        return "pdf"
    else:
        # Try reading first bytes for OFX signature
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                header = f.read(200).upper()
            if "OFXHEADER" in header or "<OFX>" in header:
                return "ofx"
        except Exception:
            pass
        raise ValueError(f"Unknown file format: {ext}")


def detect_bank_csv(filepath: str) -> tuple[str, str]:
    """Detect bank from CSV headers."""
    for encoding in ["utf-8-sig", "latin-1", "utf-8"]:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                header_line = f.readline().strip().lower()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        raise ValueError("Could not read CSV file with any supported encoding")

    for bank, headers in BANK_CSV_HEADERS.items():
        if all(h in header_line for h in headers):
            return bank, "high"

    # Fallback: check filename
    filename = Path(filepath).name.lower()
    for bank in SUPPORTED_BANKS:
        if bank in filename:
            return bank, "medium"

    return "unknown", "low"


def detect_bank_ofx(filepath: str) -> tuple[str, str]:
    """Detect bank from OFX BANKID."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(2000)
    except Exception:
        return "unknown", "low"

    # Look for BANKID in SGML or XML format
    match = re.search(r"<BANKID>(\d+)", content)
    if match:
        bankid = match.group(1)
        if bankid in OFX_BANKIDS:
            return OFX_BANKIDS[bankid], "high"

    # Fallback: filename
    filename = Path(filepath).name.lower()
    for bank in SUPPORTED_BANKS:
        if bank in filename:
            return bank, "medium"

    return "unknown", "low"


def detect_bank_pdf(filepath: str) -> tuple[str, str]:
    """Detect bank from PDF content keywords."""
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber is required for PDF parsing: pip install pdfplumber")

    try:
        with pdfplumber.open(filepath) as pdf:
            first_page = pdf.pages[0].extract_text() or ""
            text = first_page.lower()
    except Exception:
        return "unknown", "low"

    if "nubank" in text or "nu pagamentos" in text:
        return "nubank", "high"

    filename = Path(filepath).name.lower()
    for bank in SUPPORTED_BANKS:
        if bank in filename:
            return bank, "medium"

    return "unknown", "low"


def detect(filepath: str) -> dict:
    """Detect format and bank for a statement file."""
    fmt = detect_format(filepath)

    if fmt == "csv":
        bank, confidence = detect_bank_csv(filepath)
    elif fmt == "ofx":
        bank, confidence = detect_bank_ofx(filepath)
    elif fmt == "pdf":
        bank, confidence = detect_bank_pdf(filepath)
    else:
        bank, confidence = "unknown", "low"

    return {"format": fmt, "bank": bank, "confidence": confidence}


# ---------------------------------------------------------------------------
# Hash
# ---------------------------------------------------------------------------

def compute_hash(account_id: str, date: str, amount: float, description: str) -> str:
    """SHA-256 hash for deduplication: account_id|date|amount|original_description."""
    raw = f"{account_id}|{date}|{amount}|{description}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# CSV Parsers
# ---------------------------------------------------------------------------

def parse_csv_nubank(filepath: str) -> list[dict]:
    """Parse Nubank CSV: UTF-8 BOM, comma-separated, date/category/title/amount."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for CSV parsing: pip install pandas")

    df = pd.read_csv(filepath, encoding="utf-8-sig", sep=",")
    df.columns = [c.strip().lower() for c in df.columns]

    transactions = []
    for _, row in df.iterrows():
        # Nubank: positive amount = expense (debit)
        raw_amount = float(row.get("amount", row.get("valor", 0)))
        amount = -abs(raw_amount) if raw_amount > 0 else abs(raw_amount)

        title = str(row.get("title", row.get("titulo", ""))).strip()
        transactions.append({
            "date": str(row.get("date", row.get("data", ""))).strip(),
            "description": title,
            "original_description": title,
            "amount": round(amount, 2),
        })

    return transactions


def parse_csv_itau(filepath: str) -> list[dict]:
    """Parse Itaú CSV: Latin-1, semicolon, data/lançamento/valor with comma decimal."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for CSV parsing: pip install pandas")

    df = pd.read_csv(filepath, encoding="latin-1", sep=";", decimal=",")
    df.columns = [c.strip().lower() for c in df.columns]

    transactions = []
    for _, row in df.iterrows():
        desc = str(row.get("lançamento", row.get("lancamento", row.get("histórico", "")))).strip()
        date_val = str(row.get("data", "")).strip()
        # Convert DD/MM/YYYY to YYYY-MM-DD
        if "/" in date_val:
            parts = date_val.split("/")
            if len(parts) == 3:
                date_val = f"{parts[2]}-{parts[1]}-{parts[0]}"

        amount = float(row.get("valor", 0))
        transactions.append({
            "date": date_val,
            "description": desc,
            "original_description": desc,
            "amount": round(amount, 2),
        })

    return transactions


def parse_csv_inter(filepath: str) -> list[dict]:
    """Parse Inter CSV: UTF-8 BOM, semicolon, Data Lançamento/Descrição/Valor/Saldo."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for CSV parsing: pip install pandas")

    df = pd.read_csv(filepath, encoding="utf-8-sig", sep=";", decimal=",")
    df.columns = [c.strip().lower() for c in df.columns]

    transactions = []
    for _, row in df.iterrows():
        desc_col = next((c for c in df.columns if "descri" in c), None)
        date_col = next((c for c in df.columns if "data" in c), None)
        valor_col = next((c for c in df.columns if "valor" in c), None)

        desc = str(row.get(desc_col, "")).strip() if desc_col else ""
        date_val = str(row.get(date_col, "")).strip() if date_col else ""
        # Convert DD/MM/YYYY to YYYY-MM-DD
        if "/" in date_val:
            parts = date_val.split("/")
            if len(parts) == 3:
                date_val = f"{parts[2]}-{parts[1]}-{parts[0]}"

        amount = float(row.get(valor_col, 0)) if valor_col else 0.0
        transactions.append({
            "date": date_val,
            "description": desc,
            "original_description": desc,
            "amount": round(amount, 2),
        })

    return transactions


# ---------------------------------------------------------------------------
# OFX Parser
# ---------------------------------------------------------------------------

def parse_ofx(filepath: str) -> list[dict]:
    """Parse OFX/QFX files using ofxtools."""
    try:
        from ofxtools.Parser import OFXTree
    except ImportError:
        raise ImportError("ofxtools is required for OFX parsing: pip install ofxtools")

    parser = OFXTree()
    parser.parse(filepath)
    ofx = parser.convert()

    transactions = []

    for stmt in ofx.statements:
        for txn in stmt.transactions:
            date_val = txn.dtposted.strftime("%Y-%m-%d") if txn.dtposted else ""
            desc = (txn.memo or txn.name or "").strip()
            amount = float(txn.trnamt)

            transactions.append({
                "date": date_val,
                "description": desc,
                "original_description": desc,
                "amount": round(amount, 2),
            })

    return transactions


# ---------------------------------------------------------------------------
# PDF Parser
# ---------------------------------------------------------------------------

def parse_pdf(filepath: str, bank: str = "unknown") -> list[dict]:
    """Parse PDF bank statements using pdfplumber table extraction."""
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber is required for PDF parsing: pip install pdfplumber")

    transactions = []
    date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}|\d{2}/\d{2}")

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 3:
                        continue

                    # Heuristic: find date, description, amount columns
                    row_str = [str(cell).strip() if cell else "" for cell in row]

                    # Find date
                    date_val = None
                    desc_parts = []
                    amount_val = None

                    for cell in row_str:
                        if not cell:
                            continue
                        if date_pattern.match(cell) and not date_val:
                            # Convert DD/MM/YYYY or DD/MM to YYYY-MM-DD
                            parts = cell.split("/")
                            if len(parts) == 3:
                                date_val = f"{parts[2]}-{parts[1]}-{parts[0]}"
                            elif len(parts) == 2:
                                # Assume current year
                                date_val = f"2026-{parts[1]}-{parts[0]}"
                        elif _is_amount(cell) and amount_val is None:
                            amount_val = _parse_amount(cell)
                        else:
                            desc_parts.append(cell)

                    if date_val and amount_val is not None:
                        desc = " ".join(desc_parts).strip()
                        if desc:
                            transactions.append({
                                "date": date_val,
                                "description": desc,
                                "original_description": desc,
                                "amount": round(amount_val, 2),
                            })

    return transactions


def _is_amount(text: str) -> bool:
    """Check if text looks like a monetary amount."""
    cleaned = text.replace(".", "").replace(",", "").replace("-", "").replace("+", "").replace(" ", "").replace("R$", "")
    return cleaned.isdigit() and len(cleaned) >= 2


def _parse_amount(text: str) -> float:
    """Parse Brazilian monetary format (1.234,56 or -1.234,56) to float."""
    negative = "-" in text
    cleaned = text.replace("R$", "").replace(" ", "").replace("-", "").replace("+", "").strip()
    # Brazilian format: 1.234,56 → 1234.56
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        val = float(cleaned)
        return -val if negative else val
    except ValueError:
        return 0.0


# ---------------------------------------------------------------------------
# Main Parse Dispatch
# ---------------------------------------------------------------------------

def parse(filepath: str, bank: str = None) -> dict:
    """Parse a statement file and return normalized JSON."""
    detection = detect(filepath)
    fmt = detection["format"]
    if bank is None:
        bank = detection["bank"]

    if fmt == "csv":
        if bank == "nubank":
            txns = parse_csv_nubank(filepath)
        elif bank == "itau":
            txns = parse_csv_itau(filepath)
        elif bank == "inter":
            txns = parse_csv_inter(filepath)
        else:
            raise ValueError(f"Unsupported bank for CSV: {bank}")
    elif fmt == "ofx":
        txns = parse_ofx(filepath)
    elif fmt == "pdf":
        txns = parse_pdf(filepath, bank)
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    if not txns:
        return {
            "transactions": [],
            "total_rows": 0,
            "date_range": {"start": None, "end": None},
            "source_bank": bank,
            "source_format": fmt,
        }

    # Sort by date
    txns.sort(key=lambda t: t["date"])

    dates = [t["date"] for t in txns if t["date"]]
    return {
        "transactions": txns,
        "total_rows": len(txns),
        "date_range": {
            "start": min(dates) if dates else None,
            "end": max(dates) if dates else None,
        },
        "source_bank": bank,
        "source_format": fmt,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage:", file=sys.stderr)
        print("  python parse_statement.py detect <filepath>", file=sys.stderr)
        print("  python parse_statement.py parse <filepath> [bank]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if not Path(filepath).exists():
        print(json.dumps({"error": f"File not found: {filepath}"}), file=sys.stderr)
        sys.exit(1)

    try:
        if command == "detect":
            result = detect(filepath)
        elif command == "parse":
            bank = sys.argv[3] if len(sys.argv) > 3 else None
            result = parse(filepath, bank)
        else:
            print(json.dumps({"error": f"Unknown command: {command}"}), file=sys.stderr)
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except ImportError as e:
        print(json.dumps({"error": str(e), "type": "missing_dependency"}), file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(json.dumps({"error": str(e), "type": "parse_error"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "type": "unexpected_error"}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

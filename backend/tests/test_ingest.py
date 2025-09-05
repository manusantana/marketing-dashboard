import pandas as pd
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from services.ingest import parse_sales_from_excel


def test_parse_sales_from_excel_uses_correct_engine(monkeypatch, tmp_path):
    """Ensure the proper pandas engine is used for each Excel extension."""
    used_engines = []

    def fake_read_excel(path, engine=None):  # pragma: no cover - trivial stub
        used_engines.append(engine)
        return pd.DataFrame()

    monkeypatch.setattr(pd, "read_excel", fake_read_excel)

    # Test old .xls files
    xls_file = tmp_path / "sample.xls"
    xls_file.write_bytes(b"")
    parse_sales_from_excel(xls_file)

    # Test modern .xlsx files
    xlsx_file = tmp_path / "sample.xlsx"
    xlsx_file.write_bytes(b"")
    parse_sales_from_excel(xlsx_file)

    assert used_engines == ["xlrd", "openpyxl"]

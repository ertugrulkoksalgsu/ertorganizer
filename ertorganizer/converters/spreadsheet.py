import csv
import json
import os

from .base import Converter, ConversionResult, register
from ._libreoffice import convert_via_libreoffice


class SpreadsheetConverter(Converter):
    """Excel (.xlsx) ↔ CSV / JSON / PDF."""
    name = "spreadsheet"

    def supports(self, in_ext, out_ext):
        if in_ext == '.xlsx' and out_ext in {'.csv', '.json', '.pdf'}:
            return True
        if in_ext == '.csv' and out_ext == '.xlsx':
            return True
        return False

    def convert(self, input_path, output_path):
        in_ext = os.path.splitext(input_path)[1].lower()
        out_ext = os.path.splitext(output_path)[1].lower()

        if in_ext == '.xlsx' and out_ext == '.csv':
            return self._xlsx_to_csv(input_path, output_path)
        if in_ext == '.xlsx' and out_ext == '.json':
            return self._xlsx_to_json(input_path, output_path)
        if in_ext == '.xlsx' and out_ext == '.pdf':
            return self._xlsx_to_pdf(input_path, output_path)
        if in_ext == '.csv' and out_ext == '.xlsx':
            return self._csv_to_xlsx(input_path, output_path)
        return ConversionResult(False, f"Desteklenmeyen tablo dönüşümü: {in_ext} -> {out_ext}")

    def _load_openpyxl(self):
        try:
            import openpyxl
            return openpyxl
        except ImportError:
            return None

    def _xlsx_to_csv(self, input_path, output_path):
        openpyxl = self._load_openpyxl()
        if openpyxl is None:
            return ConversionResult(False, "Eksik bağımlılık: openpyxl. Kurmak için: pipx inject ertorganizer openpyxl")
        try:
            wb = openpyxl.load_workbook(input_path, read_only=True, data_only=True)
            sheets = wb.sheetnames
            if len(sheets) <= 1:
                ws = wb[sheets[0]]
                with open(output_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    for row in ws.iter_rows(values_only=True):
                        writer.writerow(row)
                wb.close()
                return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
            # Multiple sheets → one CSV per sheet
            base, ext = os.path.splitext(output_path)
            written = []
            for name in sheets:
                ws = wb[name]
                safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
                target = f"{base}__{safe}{ext}"
                with open(target, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    for row in ws.iter_rows(values_only=True):
                        writer.writerow(row)
                written.append(target)
            wb.close()
            return ConversionResult(
                True,
                f"{len(written)} sayfa CSV olarak yazıldı:\n  - " + "\n  - ".join(written),
                written[0],
            )
        except Exception as e:
            return ConversionResult(False, f"XLSX→CSV hatası: {e}")

    def _xlsx_to_json(self, input_path, output_path):
        openpyxl = self._load_openpyxl()
        if openpyxl is None:
            return ConversionResult(False, "Eksik bağımlılık: openpyxl. Kurmak için: pipx inject ertorganizer openpyxl")
        try:
            wb = openpyxl.load_workbook(input_path, read_only=True, data_only=True)
            payload = {}
            for name in wb.sheetnames:
                ws = wb[name]
                rows = list(ws.iter_rows(values_only=True))
                if not rows:
                    payload[name] = []
                    continue
                headers = [str(h) if h is not None else f"col{i+1}" for i, h in enumerate(rows[0])]
                records = []
                for row in rows[1:]:
                    records.append({headers[i]: row[i] if i < len(row) else None for i in range(len(headers))})
                payload[name] = records
            wb.close()
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"XLSX→JSON hatası: {e}")

    def _xlsx_to_pdf(self, input_path, output_path):
        ok, msg = convert_via_libreoffice(input_path, output_path, "pdf")
        if ok:
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        return ConversionResult(False, (
            f"XLSX→PDF için LibreOffice gerekir.\n{msg}"
        ))

    def _csv_to_xlsx(self, input_path, output_path):
        openpyxl = self._load_openpyxl()
        if openpyxl is None:
            return ConversionResult(False, "Eksik bağımlılık: openpyxl. Kurmak için: pipx inject ertorganizer openpyxl")
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = os.path.splitext(os.path.basename(input_path))[0][:31] or "Sheet"
            with open(input_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    ws.append(row)
            wb.save(output_path)
            return ConversionResult(True, f"Başarıyla dönüştürüldü: {output_path}", output_path)
        except Exception as e:
            return ConversionResult(False, f"CSV→XLSX hatası: {e}")

    def pairs(self):
        return [
            ('.xlsx', '.csv'),
            ('.xlsx', '.json'),
            ('.xlsx', '.pdf'),
            ('.csv', '.xlsx'),
        ]

    def required_for(self, in_ext, out_ext):
        if in_ext == '.xlsx' and out_ext == '.pdf':
            return ['libreoffice', 'openpyxl']
        if in_ext == '.xlsx' or out_ext == '.xlsx':
            return ['openpyxl']
        return []


register(SpreadsheetConverter())

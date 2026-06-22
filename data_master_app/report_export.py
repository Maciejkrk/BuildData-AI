from __future__ import annotations

from io import BytesIO
import json
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


HEADER_FILL = PatternFill("solid", fgColor="D9EAD3")
TECH_FILL = PatternFill("solid", fgColor="E7E6E6")
WARNING_FILL = PatternFill("solid", fgColor="FCE4D6")


def mapping_report_xlsx_bytes(report: dict[str, Any]) -> bytes:
    workbook = Workbook()
    overview = workbook.active
    overview.title = "Instrukcja"

    _write_rows(
        overview,
        [
            ["BuildData AI - raport mapowania", ""],
            ["Plik źródłowy", report.get("source_file", "")],
            ["Produkty wygenerowane", report.get("products_generated", "")],
            ["Elementy budowlane wygenerowane", report.get("building_elements_generated", "")],
            ["", ""],
            ["Jak używać", "Arkusz 'Mapowanie' zawiera docelowe cechy PIM i kolumny klienta. Klient może poprawić kolumny źródłowe, czyszczenie oraz mapę opcji."],
            ["Import zwrotny", "Nie usuwaj kolumn technicznych profile_key i target_path. Dzięki nim poprawiony Excel będzie możliwy do automatycznego wczytania."],
        ],
    )
    overview["A1"].font = Font(bold=True, size=14)

    _mapping_sheet(workbook, report)
    _choice_sheet(workbook, report)
    _row_rules_sheet(workbook, report)
    _tables_sheet(workbook, report)
    _unmapped_sheet(workbook, report)
    _warnings_sheet(workbook, report)
    _json_sheet(workbook, report)

    for sheet in workbook.worksheets:
        _format_sheet(sheet)

    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


def _mapping_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    sheet = workbook.create_sheet("Mapowanie")
    profile = report.get("product_mapping_profile") or {}
    rows = [[
        "profile_key",
        "source_column",
        "target_path",
        "target_label",
        "target_group",
        "target_value_kind",
        "target_unit",
        "trim",
        "parse_number",
        "decimal_comma",
        "remove_text",
        "replace_from",
        "replace_to",
        "split_by",
        "split_part",
        "unit_source_column",
        "unit_conversion_factor",
        "choice_map",
        "uwagi_klienta",
    ]]
    for profile_key, item in profile.items():
        if str(profile_key).startswith("_") or not isinstance(item, dict):
            continue
        cleanup = item.get("cleanup") or {}
        rows.append([
            profile_key,
            item.get("source_column", ""),
            item.get("target_path", ""),
            item.get("target_label", ""),
            item.get("target_group", ""),
            item.get("target_value_kind", ""),
            item.get("target_unit", ""),
            _yes_no(cleanup.get("trim", True)),
            _yes_no(cleanup.get("parseNumber", False)),
            _yes_no(cleanup.get("decimalComma", False)),
            cleanup.get("removeText", ""),
            cleanup.get("replaceFrom", ""),
            cleanup.get("replaceTo", ""),
            cleanup.get("splitBy", ""),
            cleanup.get("splitPart", ""),
            cleanup.get("unitSourceColumn", ""),
            cleanup.get("unitConversionFactor", ""),
            _format_choice_map(item.get("choice_map") or cleanup.get("choiceMap") or {}),
            "",
        ])
    if len(rows) == 1:
        fallback = report.get("column_mapping") or report.get("system_column_mapping") or {}
        for source_column, target_path in fallback.items():
            rows.append([source_column, source_column, target_path, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""])
    _write_rows(sheet, rows)


def _choice_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    sheet = workbook.create_sheet("Mapy opcji")
    rows = [["profile_key", "source_column", "target_path", "wartość klienta", "opcja PIM", "uwagi_klienta"]]
    for profile_key, item in (report.get("product_mapping_profile") or {}).items():
        if str(profile_key).startswith("_") or not isinstance(item, dict):
            continue
        choice_map = item.get("choice_map") or (item.get("cleanup") or {}).get("choiceMap") or {}
        for source_value, target_value in choice_map.items():
            rows.append([
                profile_key,
                item.get("source_column", ""),
                item.get("target_path", ""),
                source_value,
                target_value,
                "",
            ])
    _write_rows(sheet, rows)


def _row_rules_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    sheet = workbook.create_sheet("Reguły wierszy")
    rows = [["rule_index", "field", "value"]]
    rules = ((report.get("product_mapping_profile") or {}).get("_row_rules") or {}).get("rules") or []
    for index, rule in enumerate(rules, start=1):
        for key, value in rule.items():
            rows.append([index, key, _json_or_text(value)])
    _write_rows(sheet, rows)


def _tables_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    rows = [["nazwa tabeli", "liczba wierszy", "score produktów", "score elementów"]]
    for table in report.get("tables_detected") or []:
        rows.append([table.get("name", ""), table.get("rows", ""), table.get("product_score", ""), table.get("system_score", "")])
    _write_rows(workbook.create_sheet("Tabele"), rows)


def _unmapped_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    rows = [["typ", "kolumna"]]
    for column in report.get("unmapped_columns") or []:
        rows.append(["produkty", column])
    for column in report.get("system_unmapped_columns") or []:
        rows.append(["elementy budowlane", column])
    _write_rows(workbook.create_sheet("Nieprzypisane kolumny"), rows)


def _warnings_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    rows = [["obszar", "wartość"]]
    for key, value in (report.get("warnings") or {}).items():
        if isinstance(value, list):
            if not value:
                rows.append([key, ""])
            for item in value:
                rows.append([key, _json_or_text(item)])
        elif isinstance(value, dict):
            rows.append([key, json.dumps(value, ensure_ascii=False)])
        else:
            rows.append([key, value])
    _write_rows(workbook.create_sheet("Ostrzeżenia"), rows)


def _json_sheet(workbook: Workbook, report: dict[str, Any]) -> None:
    sheet = workbook.create_sheet("__mapping_json")
    sheet.sheet_state = "hidden"
    _write_rows(
        sheet,
        [
            ["schema", "builddata.mapping_report.xlsx.v1"],
            ["product_mapping_profile", json.dumps(report.get("product_mapping_profile") or {}, ensure_ascii=False, indent=2)],
            ["product_mapping", json.dumps(report.get("product_mapping") or {}, ensure_ascii=False, indent=2)],
            ["full_report", json.dumps(report, ensure_ascii=False, indent=2)],
        ],
    )


def _write_rows(sheet: Any, rows: list[list[Any]]) -> None:
    for row in rows:
        sheet.append(row)


def _format_sheet(sheet: Any) -> None:
    if sheet.max_row:
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.fill = TECH_FILL if str(cell.value or "").endswith("_key") or cell.value == "target_path" else HEADER_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    for column_cells in sheet.columns:
        letter = get_column_letter(column_cells[0].column)
        max_length = max(len(str(cell.value or "")) for cell in column_cells[:100])
        sheet.column_dimensions[letter].width = min(max(max_length + 2, 12), 60)


def _yes_no(value: Any) -> str:
    return "tak" if bool(value) else "nie"


def _format_choice_map(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    return "\n".join(f"{source} = {target}" for source, target in value.items())


def _json_or_text(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)

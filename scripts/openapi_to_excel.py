"""
OpenAPI Schema Extractor & Excel/CSV Documentation Generator.
Extracts OpenAPI specification directly from FastAPI app instances and converts them to Excel (.xlsx) and CSV (.csv) snapshots.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure root workspace directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import FastAPI App instances
from apps.time_series.main import app as ts_app
from apps.non_time_series.main import app as nts_app


def generate_openapi_json() -> Dict[str, Dict[str, Any]]:
    """
    Extract OpenAPI schemas directly from FastAPI App Objects and save to JSON files.
    Returns dictionary mapping app key to openapi schema dict.
    """
    schemas = {}

    apps_map = {
        "time_series": {
            "app": ts_app,
            "json_path": ROOT_DIR / "apps" / "time_series" / "openapi.json",
        },
        "non_time_series": {
            "app": nts_app,
            "json_path": ROOT_DIR / "apps" / "non_time_series" / "openapi.json",
        },
    }

    for app_key, info in apps_map.items():
        fastapi_app = info["app"]
        json_path = info["json_path"]

        # Extract schema from app
        schema = fastapi_app.openapi()
        schemas[app_key] = schema

        # Ensure parent directory exists
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # Save openapi.json file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        print(f"Saved OpenAPI JSON schema to {json_path}")

    return schemas


def get_schema_fields(components: Dict[str, Any], model_name: str) -> str:
    """
    Format properties/fields of a Pydantic schema model from components.schemas.
    """
    schema = components.get(model_name, {})
    props = schema.get("properties", {})
    if not props:
        return ""
    fields = []
    required_list = schema.get("required", [])
    for field_name, prop_info in props.items():
        ftype = prop_info.get("type", "any")
        is_req = "*" if field_name in required_list else ""
        fields.append(f"{field_name}{is_req}: {ftype}")
    return ", ".join(fields)


def parse_openapi_schema(schema: Dict[str, Any], service_name: str) -> List[Dict[str, Any]]:
    """
    Parse OpenAPI schema JSON into structured records for Excel / CSV export.
    """
    records = []
    components = schema.get("components", {}).get("schemas", {})
    paths = schema.get("paths", {})

    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                continue

            http_method = method.upper()
            tags = ", ".join(details.get("tags", []))
            summary = details.get("summary", "")
            description = details.get("description", "").strip()

            # Process Parameters (path, query, header, cookie)
            param_list = details.get("parameters", [])
            formatted_params = []
            for p in param_list:
                name = p.get("name", "")
                in_type = p.get("in", "")
                required = "required" if p.get("required", False) else "optional"
                p_schema = p.get("schema", {})
                p_type = p_schema.get("type", "string")
                formatted_params.append(f"{name} ({in_type}, {p_type}, {required})")
            parameters_str = "; ".join(formatted_params) if formatted_params else "None"

            # Process Request Body
            req_body = details.get("requestBody", {})
            req_body_str = "None"
            if req_body:
                content = req_body.get("content", {})
                req_parts = []
                for content_type, content_info in content.items():
                    schema_ref = content_info.get("schema", {})
                    ref = schema_ref.get("$ref", "")
                    if ref:
                        model_name = ref.split("/")[-1]
                        fields = get_schema_fields(components, model_name)
                        req_parts.append(f"{content_type}: {model_name} [{fields}]")
                    else:
                        stype = schema_ref.get("type", "object")
                        req_parts.append(f"{content_type}: {stype}")
                req_body_str = "; ".join(req_parts) if req_parts else "Present"

            # Process Response Models
            responses = details.get("responses", {})
            resp_parts = []
            for status_code, resp_info in responses.items():
                resp_desc = resp_info.get("description", "")
                content = resp_info.get("content", {})
                content_types = []
                for ctype, cinfo in content.items():
                    schema_ref = cinfo.get("schema", {})
                    ref = schema_ref.get("$ref", "")
                    if ref:
                        model_name = ref.split("/")[-1]
                        content_types.append(f"{ctype} ({model_name})")
                    else:
                        content_types.append(f"{ctype}")
                c_str = f" -> {', '.join(content_types)}" if content_types else ""
                resp_parts.append(f"HTTP {status_code}: {resp_desc}{c_str}")
            responses_str = " | ".join(resp_parts) if resp_parts else "Default"

            records.append({
                "Service Application": service_name,
                "Endpoint Path": path,
                "HTTP Method": http_method,
                "Tags": tags,
                "Summary": summary,
                "Description": description,
                "Parameters": parameters_str,
                "Request Body": req_body_str,
                "Response Models": responses_str,
            })

    return records


def export_snapshots(records: List[Dict[str, Any]], export_paths: Dict[str, List[Path]]) -> None:
    """
    Export records to Excel (.xlsx) and CSV (.csv) files at all specified target locations.
    Applies professional styling to Excel workbooks using openpyxl.
    """
    df = pd.DataFrame(records)

    # 1. Export CSV files
    for csv_path in export_paths["csv"]:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"Exported CSV snapshot to: {csv_path}")

    # 2. Export Excel files with styling
    for xlsx_path in export_paths["excel"]:
        xlsx_path.parent.mkdir(parents=True, exist_ok=True)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "API Overview"

        # Headers
        headers = list(df.columns)
        ws.append(headers)

        # Data rows
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # Styling definitions
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        cell_font = Font(name="Calibri", size=10)
        thin_border = Border(
            left=Side(style="thin", color="D9D9D9"),
            right=Side(style="thin", color="D9D9D9"),
            top=Side(style="thin", color="D9D9D9"),
            bottom=Side(style="thin", color="D9D9D9"),
        )
        alt_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")

        method_fills = {
            "GET": PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid"),
            "POST": PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid"),
            "PUT": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
            "DELETE": PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid"),
        }

        # Apply Header Formatting
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Apply Data Cell Formatting
        for row_idx in range(2, ws.max_row + 1):
            method_cell_val = str(ws.cell(row=row_idx, column=3).value).upper()
            is_even = row_idx % 2 == 0

            for col_idx in range(1, len(headers) + 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.font = cell_font
                cell.border = thin_border

                if col_idx in [1, 3, 4]:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

                if col_idx == 3 and method_cell_val in method_fills:
                    cell.fill = method_fills[method_cell_val]
                elif is_even:
                    cell.fill = alt_fill

        # Auto-adjust Column Widths
        ws.row_dimensions[1].height = 28
        for col_idx, col_name in enumerate(headers, 1):
            col_letter = get_column_letter(col_idx)
            widths = {
                "Service Application": 25,
                "Endpoint Path": 32,
                "HTTP Method": 14,
                "Tags": 18,
                "Summary": 30,
                "Description": 45,
                "Parameters": 40,
                "Request Body": 45,
                "Response Models": 50,
            }
            ws.column_dimensions[col_letter].width = widths.get(col_name, 25)

        wb.save(xlsx_path)
        print(f"Exported Styled Excel snapshot to: {xlsx_path}")


def main():
    """
    Main execution workflow.
    """
    print("==================================================")
    print("Starting OpenAPI Extraction and Excel/CSV Snapshot Generator...")
    print("==================================================")

    # 1. Generate openapi.json files directly from FastAPI apps
    schemas = generate_openapi_json()

    # 2. Extract records for both applications
    all_records = []

    ts_schema = schemas.get("time_series", {})
    ts_records = parse_openapi_schema(ts_schema, service_name="Time-Series API")
    all_records.extend(ts_records)

    nts_schema = schemas.get("non_time_series", {})
    nts_records = parse_openapi_schema(nts_schema, service_name="Non-Time-Series API")
    all_records.extend(nts_records)

    print(f"Extracted Total Endpoints: {len(all_records)} (Time-Series: {len(ts_records)}, Non-Time-Series: {len(nts_records)})")

    # 3. Define output paths
    downloads_dir = Path(os.path.expanduser("~")) / "Downloads"
    export_paths = {
        "excel": [
            ROOT_DIR / "scripts" / "api_snapshot.xlsx",
            downloads_dir / "api_snapshot.xlsx",
        ],
        "csv": [
            ROOT_DIR / "scripts" / "api_snapshot.csv",
            downloads_dir / "api_snapshot.csv",
        ],
    }

    # 4. Export snapshots
    export_snapshots(all_records, export_paths)

    print("==================================================")
    print("Snapshot Generation Completed Successfully!")
    print("==================================================")


if __name__ == "__main__":
    main()

import os
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from app.helpers.value import is_empty, random_string
from app.config import file_dir

def export(column_data: dict, row_data: list[dict], file_name: str = None, sub_path: str = None):
    if isinstance(file_name, str) and not is_empty(file_name):
        file_name = file_name.split('.')[0].strip()
    else:
        file_name = "output"

    # replace multiple space with one space replace then space with underscore
    file_name = file_name.replace('  ', ' ').replace(' ', '_')
    # concat with random string and file extension
    file_name += f"-{random_string(16, True)}.xlsx";

    today = datetime.now()
    ymd = today.strftime('%Y/%m/%d')
    file_path = f"{file_dir}/ymd"

    if isinstance(sub_path, str) and not is_empty(sub_path):
        # replace multiple slashes with a single slash and clean up the path
        sub_path = sub_path.replace('//', '/').strip('/')
        file_path = f"{file_dir}/{sub_path}/{ymd}"

    os.makedirs(file_path, exist_ok=True)

    # create a new workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = file_name.split('.')[0]
    column = []

    for key, value in column_data.items():
        width = max(len(value), 20)
        column.append({"header": value, "key": key, "width": width})

    # set the header row
    for col_idx, col in enumerate(column, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col["header"])
        cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        cell.font = Font(bold=True)
        cell.border = Border(
            top=Side(style="thin"), 
            left=Side(style="thin"), 
            bottom=Side(style="thin"), 
            right=Side(style="thin")
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = col["width"]

    # add rows of data
    for row_idx, row in enumerate(row_data, start=2):
        for col_idx, col in enumerate(column, start=1):
            value = row.get(col['key'], '')
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = Border(
                top=Side(style="thin"), 
                left=Side(style="thin"), 
                bottom=Side(style="thin"), 
                right=Side(style="thin")
            )
    
    # Save the workbook
    wb.save(f"{file_path}/{file_name}")

    # get file stats
    file_size = os.path.getsize(f"{file_path}/{file_name}")

    return {
        "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "destination": f"{file_path}/{file_name}",
        "filename": file_name,
        "path": file_path,
        "size": file_size
    }
import gspread
from oauth2client.service_account import ServiceAccountCredentials

google_sheet_name = "Code Checker Webapps"
json_file_name = 'code-checker-webapps-ad47b751bd5c.json'
scope = [
  'https://spreadsheets.google.com/feeds',
  'https://www.googleapis.com/auth/drive'
]
spreadsheet = gspread.authorize(
  ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, 
    scope
  )
).open(google_sheet_name)

def writeto(sheet, position, value):
  if "int" in str(type(sheet)):
    worksheet = spreadsheet.get_worksheet(sheet)
  else:
    worksheet = spreadsheet.worksheet(sheet)
  worksheet.update_cell(position[0], position[1], value)

def writeSubmission(sheet, submission):
  row = 1
  worksheet = spreadsheet.worksheet(sheet) 
  while worksheet.cell(row, 1).value is not None: 
    row += 1

  col = 1
  for element in submission:
    writeto(sheet, (row, col), element)
    col += 1

def to_sheet_cell(failures):
  if len(failures) == 0:
    return "None"
  else:
    result = ""
    for fault in failures:
      result += f"Required [{ str(fault[1]) }] for grade of { fault[0] }\n"
    return result
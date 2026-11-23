@st.cache_data(ttl=0)
def fetch_live_matrix_data():
    """Fetch cell values AND hover cell notes directly using Google Sheets API v4"""
    current_month_upper = datetime.now().strftime("%B").upper()  # Automatic e.g., "NOVEMBER"
    if GOOGLE_API_KEY:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}?includeGridData=true&key={GOOGLE_API_KEY}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                sheets = data.get("sheets", [])
                for sheet in sheets:
                    title = sheet.get("properties", {}).get("title", "").upper()
                    if current_month_upper in title:
                        grid = sheet.get("data", [])[0]
                        row_data = grid.get("rowData", [])
                        parsed_matrix = []
                        for r in row_data:
                            parsed_row = []
                            for c in r.get("values", []):
                                val = str(c.get("formattedValue", "") or c.get("userEnteredValue", {}).get("stringValue", ""))
                                note = str(c.get("note", ""))
                                parsed_row.append({"val": val, "note": note})
                            parsed_matrix.append(parsed_row)
                        return parsed_matrix
        except Exception:
            pass

    return fetch_gviz_fallback()

from miscSupports import flip_list


class SheetData:
    def __init__(self, sheet_name, sheet_headers, data):

        # Basic info
        self.name = sheet_name
        self.header = sheet_headers

        # Set data
        self.column_data = data
        self.row_data = flip_list(data)

        # Counts
        self.col_count = len(self.column_data)
        self.row_count = len(self.row_data)

    def __repr__(self):
        """Human readable text"""
        return f"Sheet '{self.name}': {self.col_count}-{self.row_count}"

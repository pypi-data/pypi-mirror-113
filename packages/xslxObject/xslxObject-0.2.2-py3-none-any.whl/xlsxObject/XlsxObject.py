from .SheetData import SheetData

from openpyxl.utils import get_column_letter
from miscSupports import validate_path
from openpyxl import load_workbook


class XlsxObject:
    """
    This class is designed to create a Xlsx object using openpyxl to parse in the information from an xlsx file.
    """

    def __init__(self, read_file, file_headers=True):
        """
        This object takes a read file directory as its core argument. By default file headers are turned on, but if a
        file doesn't have any file headers users can turn file headers of.

        This object has the following attributes:

        file_name: The file name of the read file minus any file extension

        sheet_column_lengths: The number of columns of data that exist with each given sheet. Keep in mind, this
        operation assumes that even if you don't have column headers, that the first row of every column does have
        content in it as this determines the length.

        sheet_row_lengths: The number of rows of data for the columns within a given sheet. Keep in mind, this operation
        assumes equal length columns and only takes the length of the first column in each sheet as the true value
        for all other columns within the sheet.

        sheet_headers: If headers are set to true, this will isolate the first row of each given column for each given
        sheet and use these values as the header value for a given column in a given sheet.

        sheet_data: This contains the data from all the sheets in a sheet-column-row format.

        :param read_file: The xlsx file path you want to read in to an object
        :type read_file: str | Path

        :param file_headers: If the xlsx file has file headers or not
        :type file_headers: bool
        """

        self._read_file = validate_path(read_file)
        self._workbook = load_workbook(self._read_file)
        self._file_headers = file_headers

        self.file_name = self._read_file.stem
        self.sheet_names = self._set_sheet_names()
        self.sheet_col_count = self._count_sheet_rows()
        self.sheet_row_count = self._count_sheet_columns()
        self.sheet_headers = self._set_sheet_header_list()
        self.sheet_data = self._set_sheet_data()

    def __repr__(self):
        """Human readable print"""
        return f"{self.file_name}.xlsx with {len(self.sheet_names)} sheets"

    def __getitem__(self, item):
        """Extract the data """
        if isinstance(item, int):
            return self.sheet_data[item]
        else:
            raise TypeError(f"Getting sheet data via __getitem__ requires an item yet was passed {type(item)}")

    def _set_sheet_names(self):
        """
        This extracts the sheets titles from the xlsx workbook

        :return: The sheet names for each given sheet in the form of a list
        :rtype: list
        """

        return [sheet.title for sheet in self._workbook.worksheets]

    def _count_sheet_rows(self):
        """
        Iterator, that will work through the sheets and find the number of columns based on the first row and if it has
        any content within it or otherwise.

        :return: The column length for each given sheet, where each column length is an int
        :rtype: list
        """

        return [self._set_column_length(sheet) for sheet in self._workbook.worksheets]

    def _count_sheet_columns(self):
        """
        Iterator that will work through the sheets and find the number of rows based on the first column by checking to
        see if a row has any content within it.

        :return: The row length for each given sheet, where each row length is an int
        :rtype: list
        """

        return [self._set_row_length(sheet) for sheet in self._workbook.worksheets]

    def _set_sheet_header_list(self):
        """
        This creates headers for our sheet information depending on if the file has headers or not

        :return: Sheet headers
        :rtype: list
        """

        if self._file_headers:
            sheet_headers = [[sheet[f"{get_column_letter(i)}{1}"].value for i in range(1, sheet_length + 1)]
                             for sheet_length, sheet in zip(self.sheet_col_count, self._workbook.worksheets)]

        else:
            sheet_headers = [[f"Var{i}" for i in range(1, sheet_length)] for sheet_length in self.sheet_col_count]
        return sheet_headers

    def _set_sheet_data(self):
        """
        Iterator that will work through the sheets and, by using the column and row lengths, isolate all the content
        within a given sheet. This means that the end result is a nested list of sheet-column-row.

        :return: The sheet data for each given sheet
        :rtype: list[SheetData]
        """

        return [self._set_data(sheet, sheet_index) for sheet_index, sheet in enumerate(self._workbook.worksheets)]

    @staticmethod
    def _set_column_length(sheet, column_index=1):
        """
        This takes the first row and returns its length so we know how many columns of data we are working with.

        :param sheet: The current openypyxl worksheet class object
        :type sheet: openpyxl.worksheet.worksheet.Worksheet

        :param column_index: Starting value, xlsx uses base 1 rather than base zero for columns
        :type column_index: int

        :return: Length of the number of columns
        :rtype: int
        """

        while True:
            if sheet[f"{get_column_letter(column_index)}1"].value is None:
                return column_index - 1
            else:
                column_index += 1

    def _set_row_length(self, sheet):
        """
        This takes the first column and returns its length so we know how many rows of data we are working with. If the
        file has headers, then we need to skip counting the first row

        :param sheet: The current openypyxl worksheet class object
        :type sheet: openpyxl.worksheet.worksheet.Worksheet

        :return: The row length for this given sheet
        :rtype: int
        """

        if self._file_headers:
            row_index = 2
        else:
            row_index = 1

        while True:
            if sheet[f"A{row_index}"].value is None:
                return row_index - 1
            else:
                row_index += 1

    def _set_data(self, sheet, sheet_index):
        """
        This sets the data for a given sheet by taking the row and column lengths and then iterating through the sheets
        columns and rows by using range indexing.

        NOTE
        ----
        openpyxl requires base 1 not base 0 hence range

        :param sheet: The current openypyxl worksheet class object
        :type sheet: openpyxl.worksheet.worksheet.Worksheet

        :param sheet_index: The current sheets index
        :type sheet_index: int

        :return: A column-row list set of all the content within the sheet
        :rtype: SheetData
        """

        # Set row count based on if headers are include so that headers are not within data rows
        if self._file_headers:
            row_start = 2
        else:
            row_start = 1
        row_end = self.sheet_row_count[sheet_index] + 1

        # Extract the data from the sheet
        sheet_data = [[sheet[f"{get_column_letter(col_i)}{row_i}"].value for row_i in range(row_start, row_end)]
                      for col_i in range(1, self.sheet_col_count[sheet_index] + 1)]

        # Return the sheet data type SheetData
        return SheetData(self.sheet_names[sheet_index], self.sheet_headers[sheet_index], sheet_data)

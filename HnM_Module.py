from RFID_Lab import RFID_Dataframe, RFID_Analysis
import pandas as pd
import enum
import xlrd


class File_Type(enum.Enum):
    Measured_Zebra = 0
    Measured_Bluebird = 1
    Expected_SalesFloor = 2
    Expected_StockRoom = 3


class HnM_Dataframe(RFID_Dataframe):

    columns = ["EPC"]

    Column_Table = {
        File_Type.Measured_Zebra: ["epcHex"],
        File_Type.Measured_Bluebird: [""],
        File_Type.Expected_SalesFloor: ["Salesfloor"],
        File_Type.Expected_StockRoom: ["BackRoom"]
    }

    def __init__(self, title, path, file_type):
        super().__init__(title, path, file_type)
        self.columns = HnM_Dataframe.Column_Table[file_type]

    def parse(self):
        data_frame = pd.DataFrame()
        if self.file_type == File_Type.Measured_Zebra:
            data_frame = self.parseZebraCSV()
        elif self.file_type == File_Type.Measured_Bluebird:
            data_frame = self.parseBlueBirdCSV()
        else:
            data_frame = self.parseExcel()
        data_frame.columns = HnM_Dataframe.columns
        return data_frame

    def parseZebraCSV(self):
        return pd.DataFrame(pd.read_csv(self.path), columns=HnM_Dataframe.Column_Table[self.file_type])

    def parseBlueBirdCSV(self):
        return pd.DataFrame(pd.read_csv(self.path, header=None, usecols=[0], skip_blank_lines=True))

    def parseExcel(self):
        return pd.DataFrame(pd.read_excel(self.path, header=None, index_col=None,
                                          sheet_name=HnM_Dataframe.Column_Table[self.file_type][0]))

    def filterData(self):
        pass


class HnM_Analysis(RFID_Analysis):

    def __init__(self, title, primary_csv, secondary_csv, column=0):
        super().__init__(self, title, primary_csv, secondary_csv, column)


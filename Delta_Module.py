from RFID_Lab import RFID_Dataframe, RFID_Analysis
import pandas as pd
import enum
import xlrd


class File_Type(enum.Enum):
    DELTA = 0
    ATT = 1


class Delta_Dataframe(RFID_Dataframe):
    columns = ["Commodity_ID", "Timestamp"]

    Column_Table = {
        File_Type.DELTA: ["CMDTY_ID", "SCN_UTC_TMS"],
        File_Type.ATT: ["CMDTY ID", "TIMESTAMP"]
    }

    DateFilter_Table = {
        File_Type.DELTA: "%d-%b-%y %I.%M.%S.%f000 %p",
        File_Type.ATT: "%m/%d/%Y %I:%M:%S %p"
    }

    def __init__(self, title, path, file_type):
        super().__init__(title, path, file_type)
        self.columns = self.Column_Table[file_type]

    def parse(self):
        data_frame = pd.DataFrame(pd.read_csv(self.path), columns=self.columns)
        data_frame.columns = self.columns

        return data_frame

    def filterToDateTime(self, column):
        self.data_frame[column] = pd.to_datetime(self.data_frame[column],
                                                 errors="coerce",
                                                 format=self.DateFilter_Table[self.csv_type])
        self.data_frame.dropna(subset=[column], inplace=True)

    def filterData(self):
        self.dropDuplicates()
        self.filterWithPrefix(self.columns[0], [[], ["0"], ["0"], ["6"]])
        self.filterToDateTime(self.columns[1])
        self.filterToInts(self.columns[0])
        self.data_frame.reset_index(drop=True, inplace=True)


class Delta_Analysis(RFID_Analysis):

    def __init__(self, title, primary_csv, secondary_csv, column=0):
        super().__init__(self, title, primary_csv, secondary_csv, column)

from RFID_Lab import RFID_Dataframe, RFID_Analysis
import pandas as pd
import enum
import xlrd
import openpyxl


class File_Type(enum.Enum):
    DELTA = 0
    ATT = 1


class Delta_Dataframe(RFID_Dataframe):
    column_labels = ["Commodity_ID", "Timestamp"]

    Column_Table = {
        File_Type.DELTA: ["CMDTY_ID", "SCN_UTC_TMS"],
        File_Type.ATT: ["CMDTY ID", "TIMESTAMP"]
    }

    DateFilter_Table = {
        File_Type.DELTA: "%d-%b-%y %I.%M.%S.%f000 %p",
        File_Type.ATT: "%m/%d/%Y %I:%M:%S %p"
    }

    def __init__(self, title, path, file_type):
        self.columns = self.Column_Table[file_type]
        super().__init__(title, path, file_type)

    def parse(self):
        data_frame = pd.DataFrame(pd.read_csv(self.path), columns=self.columns)
        data_frame.columns = self.column_labels
        return data_frame

    def filterToDateTime(self, column):
        self.data_frame[column] = pd.to_datetime(self.data_frame[column],
                                                 errors="coerce",
                                                 format=self.DateFilter_Table[self.file_type])
        self.data_frame.dropna(subset=[column], inplace=True)

    def filterData(self):
        self.dropDuplicates(self.column_labels[0])
        self.filterWithPrefix(self.column_labels[0], [[], ["0"], ["0"], ["6"]])
        self.filterToDateTime(self.column_labels[1])
        self.filterToInts(self.column_labels[0])
        self.data_frame.reset_index(drop=True, inplace=True)


class Delta_Analysis(RFID_Analysis):

    def __init__(self, title, primary_dataframe, secondary_dataframe, column=0):
        super().__init__(title, primary_dataframe, secondary_dataframe, column)

    def exportStatistics(self, path):
        stats = self.calcStatistics()
        indexes = ["Total Primary", "Total Secondary", "Accurate", "Underread", "Overread"]
        df1 = pd.DataFrame({"Count": [stats[0], stats[1], stats[2], stats[4], stats[6]],
                            "Percentage":
                                [None, None, stats[3], stats[5], stats[7]]},
                           indexes)

        df2 = self.primary_dataframe.parse()

        df3 = self.secondary_dataframe.parse()
        df5 = self.primary_dataframe.data_frame.copy()
        df5.columns = ["Expected", "Timestamp"]
        df4 = pd.concat([df5, self.secondary_dataframe.data_frame], axis=1)

        with pd.ExcelWriter(path) as writer:
            df1.to_excel(writer, sheet_name="Analysis")
            df2.to_excel(writer, sheet_name="Expected_RAW")
            df3.to_excel(writer, sheet_name="Read_RAW")
            df4.to_excel(writer, sheet_name="Filtered Data")

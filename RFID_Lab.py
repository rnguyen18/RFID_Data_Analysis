import abc


class RFID_Dataframe:
    column_table = {}

    csv_columns = []

    def __init__(self, title, path, file_type):
        self.title = title
        self.path = path
        self.file_type = file_type
        self.data_frame = self.parse()
        self.filterData()

    def print(self):
        print(self.data_frame)

    def printCount(self):
        print(self.data_frame.count())

    def printValues(self):
        for i, v in self.data_frame.iterrows():
            print(v.values[0])

    def dropDuplicates(self):
        return self.data_frame.drop_duplicates(keep='first', inplace=True)

    def writeCSV(self, path=""):
        Path = path if path != "" else "../files/HnM/write/{0}.csv".format(self.title)
        self.data_frame.to_csv(Path)

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError

    @abc.abstractmethod
    def filterData(self):
        raise NotImplementedError

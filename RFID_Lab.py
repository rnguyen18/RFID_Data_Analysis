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


class RFID_Analysis:

    def __init__(self, title, primary_csv, secondary_csv, column=0):
        self.title = title

        self.primary_csv = primary_csv
        self.primary_total = len(primary_csv.data_frame.index)

        self.secondary_csv = secondary_csv
        self.secondary_total = len(secondary_csv.data_frame.index)

        self.primary_ids = self.primary_csv.data_frame[self.primary_csv.data_frame.columns[column]]
        self.secondary_ids = self.secondary_csv.data_frame[self.secondary_csv.data_frame.columns[column]]

    def calc_Accurate(self):
        accurate_count = 0
        for _, v in self.primary_ids.iteritems():
            if v in set(self.secondary_ids):
                accurate_count = accurate_count + 1

        return accurate_count

    def calc_Underread(self):
        underread_count = 0
        for _, v in self.primary_ids.iteritems():
            if not (v in set(self.secondary_ids)):
                underread_count = underread_count + 1

        return underread_count

    def calc_Overread(self):
        overread_count = 0
        for _, v in self.secondary_ids.iteritems():
            if not (v in set(self.primary_ids)):
                overread_count = overread_count + 1

        return overread_count

    def calcStatistics(self):
        accurate = self.calc_Accurate()
        underread = self.calc_Underread()
        overread = self.calc_Overread()

        accurate_percentage = round(100*accurate/self.primary_total)
        underread_percentage = round(100*underread/self.primary_total)
        overread_percentage = round(100*overread/self.primary_total)

        return [self.primary_total, self.secondary_total, accurate, accurate_percentage, underread, underread_percentage, overread, overread_percentage]

    @abc.abstractmethod
    def exportStatistics(self):
        raise NotImplementedError


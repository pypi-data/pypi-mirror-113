from fload.stream import Source
import csv

class CSVSource(Source):
    csv_file = None
    encoding = 'utf8'

    def add_arguments(self, parser):
        parser.add_argument('csvfile')
        parser.add_argument('--encoding')

    def init(self, ops):
        self.csv_file = ops.csvfile
        self.encoding = ops.encoding or 'UTF8'

    def start(self):
        f = open(self.csv_file, encoding=self.encoding)
        input_file = csv.DictReader(f)
        for row in input_file:
            yield row
        f.close()

import datetime
import xlrd
from collections import OrderedDict

__all__ = ["Reader", "DictReader"]


class Reader:
    line_num = 0
    rows = []

    def __init__(self, f):
        wk = xlrd.open_workbook(file_contents=f.read())
        assert wk.nsheets == 1, "file sheet shoulb be one"
        sh = wk.sheet_by_index(0)
        assert sh.nrows >= 1, "data row must be more than one"

        for i in range(sh.nrows):
            row_data = []
            for j in range(sh.ncols):
                # ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                ctype = sh.cell(i, j).ctype
                v = sh.cell_value(rowx=i, colx=j)
                if ctype == 2 and v % 1 == 0:
                    v = int(v)
                elif ctype == 3:
                    date_touple = xlrd.xldate_as_tuple(v, wk.datemode)
                    v = datetime.datetime(*date_touple)
                    pass
                elif ctype == 4:
                    v = True if v else False

                row_data.append(v)

            self.rows.append(row_data)

    def __iter__(self):
        return self

    def __next__(self):
        self.line_num += 1
        try:
            return self.rows[self.line_num - 1]
        except IndexError:
            raise StopIteration


class DictReader:

    def __init__(self, f, fieldnames=None, restkey=None, restval=None):
        self._fieldnames = fieldnames   # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = Reader(f)
        self.line_num = 0

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def __next__(self):
        if self.line_num == 0:
            # Used only for its side effect.
            _fieldnames = self.fieldnames
        row = next(self.reader)
        self.line_num = self.reader.line_num
        while not row:
            row = next(self.reader)
        d = OrderedDict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d

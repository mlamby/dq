import re
from dq import ast


class QueryParseException(Exception):
    """ Exception raised when a query string can not be fully parsed.
    """
    pass


grammar = re.compile(r"""(
    (?P<select>\.[^.\[\]]+) |
    (?P<find>\.\.[^.\[\]]+) |
    (?P<index>\[-?\d+\]) |
    (?P<star>\[\*\]) |
    (?P<range>\[(?:-?\d+)?:(?:-?\d+)?(?:\:\d+)?\])
)""", re.VERBOSE)

class Parser(object):
    def __init__(self, query_str):
        self.query_str = query_str
        self.query_chunk = query_str

    def parse(self, lhs = ast.Root()):
        cls = ast.Selector
        m = self.next_match()
        if not m:
            return lhs

        if m.group('select'):
            field_name = m.group('select')[1:]
            rhs = ast.Field(field_name)
        if m.group('find'):
            field_name = m.group('find')[2:]
            rhs = ast.Field(field_name)
            cls = ast.Finder
        elif m.group('index'):
            field_index = int(m.group('index')[1:-1])
            rhs = ast.Index(field_index)
        elif m.group('star'):
            rhs = ast.Slice()
        elif m.group('range'):
            r = m.group('range')[1:-1].split(':')
            if len(r) == 2:
                r.append('')
            rhs = ast.Slice(
                self._int_or_none(r[0]), 
                self._int_or_none(r[1]), 
                self._int_or_none(r[2]))

        return self.parse(cls(lhs, rhs))

    def next_match(self):
        if not self.query_chunk:
            return None

        m = grammar.match(self.query_chunk)
        if m:
            self.query_chunk = self.query_chunk[len(m.group(0)):]
        else:
            raise QueryParseException(
                    "Unmatched String Portion '%s'" % self.query_chunk)

        return m

    def _int_or_none(self, value):
        return int(value) if value else None


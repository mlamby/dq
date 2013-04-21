from dq import parser

def query(query_str, source):
    """ Run a query over the given source data structure.

        query_str is the query to be executed and is compiled each time this
        function is called.

        source is the object to be queried.

        raises QueryParseException if query_str is not valid.

        returns the results of the query.
    """
    return compile(query_str)(source)


def compile(query_str):
    """ Compile the given query string into a compiled query
    """
    return CompiledQuery(query_str)


class CompiledQuery(object):
    """ The compiled query object.
        Calling the instance with the data to be queried will run the query
        and return the results.
    """
    def __init__(self, query_str):
        self._root = parser.Parser(query_str).parse() 

    def __call__(self, source):
        result = self._root(source)
        if len(result) == 1:
            return result[0]
        return result

    def __str__(self):
        return str(self._root)

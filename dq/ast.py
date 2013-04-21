from itertools import chain
import logging

logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Private query AST Nodes
# ----------------------------------------------------------
class Root(object):
    """ Node used to represent the root of the input data. """
    def __call__(self, source):
        logger.debug("$ = %s" % source)
        return [source]

    def __str__(self):
        return "$"


class Field(object):
    """ Node used to select a named item from a dictionary. """
    def __init__(self, name):
        self._name = name

    def __call__(self, source):
        try:
            logger.debug("Field[%s] in %s" % (self._name, source))
            return [source[self._name]]
        except:
            pass
        return []

    def __str__(self):
        return "'%s'" % (self._name)


class Index(object):
    """ Node used to select a number item from a list. """
    def __init__(self, index):
        self._index = index

    def __call__(self, source):
        try:
            logger.debug("Index[%s] in %s" % (self._index, source))
            return [source[self._index]]
        except:
            pass
        return []

    def __str__(self):
        return "[%s]" % (self._index)


class Slice(object):
    """ Node used to handle the array slicing specified [::]. """
    def __init__(self, start=None, stop=None, step=None):
        self._slice = slice(start, stop, step)

    def __call__(self, source):
        logger.debug("Slice[%s] in %s" % (self._slice, source))
        return source[self._slice]

    def __str__(self):
        return "[%s]" % (self._slice)


class Selector(object):
    """ Node used to handle '.' specifier. """
    def __init__(self, lhs, rhs):
        self._lhs, self._rhs = lhs, rhs

    def __call__(self, source):
        logger.debug("Select LHS=%s, RHS=%s" % (self._lhs, self._rhs))
        return list(chain(*[self._rhs(l) for l in self._lhs(source)]))

    def __str__(self):
        return "%s.%s" % (self._lhs, self._rhs)


class Finder(object):
    """ Node used to handle the '..' specifier. """
    def __init__(self, lhs, rhs):
        self._lhs, self._rhs = lhs, rhs

    def __call__(self, source):

        def matches(data):
            rhs = self._rhs(data)
            if isinstance(data, list):
                rhs.extend(list(chain(*[matches(child) for child in data])))
            elif isinstance(data, dict):
                rhs.extend(
                    list(chain(*[matches(child) for child in data.values()])))
            return rhs
            
        logger.debug("Find LHS=%s, RHS=%s" % (self._lhs, self._rhs))
        return list(chain(*[matches(l) for l in self._lhs(source)]))
    
    def __str__(self):
        return "%s..%s" % (self._lhs, self._rhs)


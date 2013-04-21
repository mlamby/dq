dq.py - Python DataQuery
=========================
Provides the ability to query a data source made up of any combination
of lists and dicts.

To use from within Python:
```python
>>> from dq import query
>>> dq.query('[0].name', [{'name': 'michael'}, {'name': 'jane'}])
'michael' 

>>> dq.query('..name', [{'name': 'michael'}, {'name': 'jane'}])
['michael', 'jane']
```
Installation
------------
To install dq:
```
pip install dq
```
dq does not depend on any non-standard libraries

Query Language
--------------
The query language is a much simplified version of [json path][1]. The subset
is selected to allow for simple structural querying of data - no filters or 
expressions. This keeps the parser nice and simple, and since its a Python
library you have the full power of Python to perform complex filters.

The query language supports the following path syntax:
```
.key - Returns the given key from the dict
..key - Returns the given key from any descendant dictionary 
[index] - Returns an item from a list at the specified index
[*] - Returns all items in a list
[start:stop:step] - Performs a python slice operation on a list
```

Query Examples
--------------
These syntax items can be combined to build complex queries.
```python
>>> from dq import query
>>> d = {}
>>> d['one'] = 1
>>> d['two'] = [1,2,3,4,5,6,7,8,9,10]
>>> d['three'] = [{'name': 'john'}, {'name': 'mary'}, {'one': 'guy'}]

>>> query('.one', d)
1

>>> query('.two', d)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

>>> query('.two[1]', d)
2

>>> query('.two[*]', d)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

>>> query('.two[2:-2]', d)
[3, 4, 5, 6, 7, 8]

>>> query('.two[1:6:2]', d)
[2, 4, 6]

>>> query('.three[1].name', d)
'mary'

>>> query('.three[*].name', d)
['john', 'mary']

>>> query('..name', d)
['john', 'mary']

>>> query('..one', d)
[1, 'guy']
```

Compiled Queries
----------------
When using the same query string repeatedly a CompiledQuery can be constructed
to prevent parsing the query string multiple times:
```python
>>> from dq import compiled
>>> query = compiled('[1]')
>>> query([1,2,3,4])
2
>>> query([5,6,7,8])
6
```

Thanks
-------
This library is based on the ideas and code from [python-jsonpath-rw][2].

[1]: http://goessner.net/articles/JsonPath/ "Json Path"
[2]: https://github.com/kennknowles/python-jsonpath-rw "python-jsonpath-rw"

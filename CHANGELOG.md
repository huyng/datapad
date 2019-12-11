
2019-12-11
==========

* Added the new `datapad.fields` module which provides functions for operating on lists and dicts, as if they were "columns" in a sequence of rows. The following functions were added:
    * `fields.apply` - apply functions to columns of rows
    * `fields.add` - add columns to each row by apply functions on the row
    * `fields.select` - limit the columns returned in each row
    * `fields.asdict` - converts lists to dicts

* Make `seq.groupby` eagerly collect groups by default 

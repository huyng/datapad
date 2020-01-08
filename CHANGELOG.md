<!--
Copyright 2019 Huy Nguyen

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Software distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-->

2020-01-01
==========

Version: 0.6.6

* New Features: We added `Sequence.window` and `Sequence.batch` to enable sliding window aggregations and batch aggregations.

2020-01-01
==========

Version: 0.6.5

* BUGFIX: Fixed bug where `Sequence.count` was throwing error when elements were non-hashable.


2019-12-31
==========

Version: 0.6.4

* added `sequence.peek` to allow you to examine a sequence without consuming it.

2019-12-26
==========

Version: 0.6.3

* added `sequnce.distinct` function to get unique values from a sequence.
* Added `Sequence.count(distinct=True)` function in order to count distinct elements in a sequence.

2019-12-11
==========

Version: 0.6.1

* Added the new `datapad.fields` module which provides functions for operating on lists and dicts, as if they were "columns" in a sequence of rows. The following functions were added:
    * `fields.apply` - apply functions to columns of rows
    * `fields.add` - add columns to each row by apply functions on the row
    * `fields.select` - limit the columns returned in each row
    * `fields.asdict` - converts lists to dicts

* Make `seq.groupby` eagerly collect groups by default

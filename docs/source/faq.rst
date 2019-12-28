==========================
Frequently Asked Questions
==========================

* **What was the motivation for developing Datapad?**

    Datapad stemmed from my desire to create a "humans" friendly data processing library with an API designed first and foremost focused on "developer happiness" as opposed to performance, distributed execution, or other concerns.

    This meant that the library would be easy to install, worked locally, and had a minimal yet intuitive API.


* **What other related projects are there?**

    Datapad is influenced heavily by the following projects. For the most part, many concepts from Python's `itertools` library have been repackaged into Datapad as fluent interfaces.

    * `LINQ <https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/standard-query-operators-overview>`_
    * `Spark <https://spark.apache.org/>`_
    * `Python itertools <https://docs.python.org/3/library/itertools.html>`_
    * `Pandas <https://pandas.pydata.org/>`_
    * `Tensorflow tf.data.Datasets <https://www.tensorflow.org/api_docs/python/tf/data/Dataset>`_

* **How does this project compare to Spark**?

    Spark is a fantastic library, and many of the concepts in Datapad such as lazy evaluation are similar to Spark's design. However, because Spark is written for a JVM based system, using Spark for simple, local data processing can be overkill.

    Datapad is written in pure python and can be used with minimal dependencies.

* **How does this project compare to Pandas**?

    The Pandas library is a popular framework for adhoc data processing. Many of the concepts in the Pandas framework revovle around the "Dataframe" object which is well suited for indexed tabular data.

    In contrast Datapad focuses on  `Sequences` or `streams` of data which may or may not fit into the tabular data paradigm. While subtle, this fact enables us to design an powerful & composable API that focuses more on the simple primitives of mapping functions over potentially infinite streams data.

    In our opinion, this central design pattern requires less mental overhead for interacting with your data (although it can be slower in some instances).












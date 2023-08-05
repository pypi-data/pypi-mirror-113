.. role:: raw-html-m2r(raw)
   :format: html


Streamlit-tags
==============

|pypi Version| |conda Version| |PyPi downloads| |Conda downloads|

A custom component to add Tags in Streamlit.

.. image:: https://user-images.githubusercontent.com/49101362/114277814-83cb1200-9a35-11eb-8761-9d8bb81ffadc.gif
   :alt: ezgif com-gif-maker (1)


Please star⭐ the repo and share the usage if you liked it.

Try out a demo here: |Streamlit App|

Check out docs here: https://streamlit-tags.readthedocs.io/en/latest/

Install
-------

PyPi

.. code-block::


   ::

      pip install streamlit-tags

   The installation can also be found on `PyPi`_

   Anaconda
   ~~~~



   conda install -c gagan3012 streamlit-tags

The installation can also be found on `Anaconda`_

Usage
-----

This library has two main functions to display and use tags:


* ``st_tags`` to display the tags feature
* ``st_tags_sidebar`` to display the tags in the sidebar

Check the ``examples/``\ _ folder of the project a quick start.

Check out demo here:
https://share.streamlit.io/gagan3012/streamlit-tags/examples/app.py

Definition
----------

.. code:: python

   def st_tags(label: str,
               text: str,
               value: list,
               suggestions: list,
               key=None) -> list:
       '''

       :param suggestions: (List) List of possible suggestions (optional)
       :param label: (Str) Label of the Function
       :param text: (Str) Instructions for entry
       :param value: (List) Initial Value (optional)
       :param key: (Str)
           An optional string to use as the unique key for the widget.
           Assign a key so the component is not remount every time the script is rerun.
       :return: (List) Tags

       Note: usage also supports keywords = st_tags()

       '''


Note:
^^^^^


* The suggestion and value fields are optional
* Usage also supports ``keywords = st_tags()``

We also have a function now to embed the tags function to the sidebar:
:raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`\ :raw-html-m2r:`<del>~</del>`

.. _PyPi: https://pypi.org/project/streamlit-tags/

.. _Anaconda: https://anaconda.org/gagan3012/streamlit-tags

.. _``examples/``: https://github.com/gagan3012/streamlit-tags/tree/master/examples


.. |pypi Version| image:: https://img.shields.io/pypi/v/streamlit-tags.svg?style=flat-square&logo=pypi&logoColor=white
   :target: https://pypi.org/project/streamlit-tags/

.. |conda Version| image:: https://img.shields.io/conda/vn/gagan3012/streamlit-tags.svg?style=flat-square&logo=conda-forge&logoColor=white
   :target: https://anaconda.org/gagan3012/streamlit-tags

.. |PyPi downloads| image:: https://static.pepy.tech/personalized-badge/streamlit-tags?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads
   :target: https://pypi.org/project/streamlit-tags/

.. |Conda downloads| image:: https://img.shields.io/conda/dn/gagan3012/streamlit-tags?label=conda%20downloads
   :target: https://anaconda.orggagan3012/streamlit-tags

.. |Streamlit App| image:: https://static.streamlit.io/badges/streamlit_badge_black_white.svg

   :target: https://share.streamlit.io/gagan3012/streamlit-tags/examples/app.py

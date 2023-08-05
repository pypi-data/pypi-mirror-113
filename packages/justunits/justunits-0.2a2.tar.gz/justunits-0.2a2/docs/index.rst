=============================================================================
Welcome to 'Just SI Units' documentation!
=============================================================================

**justunits** handles (SI-) units within string occurrences. The module's *justunits*
tasks are limited to the interchangeability of different unit formatting styles.
This module focus **just** on **units**, it does not provide unit conversion or
anything related to such a topic. It's purpose is to provide an entry point for a
future unit conversion within another module.

.. image:: ../justunits-icon.svg
   :height: 196px
   :width: 196px
   :alt: A trash panda.
   :align: center

**justunits** major purpose can be shown with 2 graphs. It's first purpose is to
provide a support for different value/attribute and unit separation styles, which
can occur within text files.


.. note::

    **The current development state of this project is `alpha`. It's published for a
    first stress test of 2 major functions.**

    Towards the beta

    - naming of modules, classes and methods will change, since the final wording is not
      done.
    - Code inspections are not finished.
    - The documentation is broad or incomplete.
    - Testing is not complete, as it is added during the first test phase. At this
      state mostly doctests are applied at class or function level.

.. _figure 1:


.. graphviz::

    digraph separators {
      layout=twopi;
      ranksep=1.5;
      node [shape=plaintext fontsize=11] {
       a [label="'length in mm'"];
       b [label="'length_in_mm'"];
       c [label="'length [mm]'"];
       d [label="'length_[mm]'"];
       e [label="'length#mm'"];
       f [label="'length mm'"];
       g [label="'length_mm'"];
       }

      justunits [shape=circle];

      justunits -> a, b, c, d, e, f, g [dir="both"];

    }

**Figure 1: Supported separations between an attribute/value and a unit.**

The second purpose is to detect SI-units and support 4 major layouts emphasising utf8
with superscripts using a dot as a separator.

.. _figure 2:

.. graphviz::

    graph grid {
      node [shape=plaintext width=1.8 fontsize=11] {
        a [label="kg/(s²⋅K)⋅m²"];
        b [label="kg⋅s⁻²⋅K⁻¹⋅m²"];
        c [label="kg/(s^2*K)*m^2"];
        d [label="kg*s^-2*K^-1*m^2"];
      }

      node [shape=boxed width=1.5] {
         slashed; power [label="by power"];
      }

      node [shape=boxed width=1] {
         utf8; ascii
      }

        a -- d
        c -- b

        slashed -- a -- c
        power -- b -- d

        rank=same {slashed power}
        rank=same {utf8 -- a -- b}
        rank=same {ascii -- c -- d}
    }

**Figure 2: Unit representations supported by justunits.**

|

Installation
============

Install the latest release from pip.

.. code-block:: shell

   $ pip install justunits

.. toctree::
   :maxdepth: 3

   basic_usage
   unit_styles
   api_reference/index


Indices and tables
==================

* :ref:`genindex`
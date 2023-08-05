=========================
Unit styles of justunits
=========================

The formatting of units is sectioned into the separation of attribute/value-unit pairs
and the styling of the units themself.

Defaults
========


*justunits* formats by these default definitions.

.. autodata:: justunits.DEFAULT_ATTRIBUTE_UNIT_SEPARATOR
   :noindex:
.. autodata:: justunits.DEFAULT_ALLOWED_SEPARATORS
   :noindex:
.. autodata:: justunits.DEFAULT_POWER_STYLE
   :noindex:
.. autodata:: justunits.DEFAULT_DIVIDING_STYLE
   :noindex:
.. autodata:: justunits.DEFAULT_SEPARATION_STYLE
   :noindex:
.. autodata:: justunits.DEFAULT_UNIT_STYLE
   :noindex:

Seperation of attribute/value and unit
======================================

.. autoattribute:: justunits.AttributeUnitSeparators.WHITESPACE_BOXED
.. autoattribute:: justunits.AttributeUnitSeparators.UNDERLINE_BOXED
.. autoattribute:: justunits.AttributeUnitSeparators.WHITESPACE_IN
.. autoattribute:: justunits.AttributeUnitSeparators.UNDERLINED_IN
.. autoattribute:: justunits.AttributeUnitSeparators.HASH_SIGN
.. autoattribute:: justunits.AttributeUnitSeparators.SINGLE_UNDERLINE
.. autoattribute:: justunits.AttributeUnitSeparators.SINGLE_WHITESPACE


Styling of just units
=====================

Unit power style
----------------

.. autoattribute:: justunits.UnitPowerStyle.SUPERSCRIPT
.. autoattribute:: justunits.UnitPowerStyle.CARET


Style of divisions
------------------

.. autoattribute:: justunits.UnitDividingStyle.SLASHED
.. autoattribute:: justunits.UnitDividingStyle.BY_POWER

Seperation in between units
---------------------------

.. autoattribute:: justunits.UnitSeparationStyle.DOT
.. autoattribute:: justunits.UnitSeparationStyle.ASTERISK


Complete unit styles
--------------------

.. autoattribute:: justunits.UnitStyle.SIMPLE_ASCII
.. autoattribute:: justunits.UnitStyle.TOTAL_POWER_ASCII
.. autoattribute:: justunits.UnitStyle.FINE_SLASHED_SUPERSCRIPT
.. autoattribute:: justunits.UnitStyle.FINE_POWERED_SUPERSCRIPT
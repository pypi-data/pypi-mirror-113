===========
Basic Usage
===========

Styling
=======
You might want to set your desired attribute unit and unit style flavor first or
just keep the preset defaults. See all `supported unit styles`_.


.. _supported unit styles: ./unit_styles.html

    >>> import justunits
    >>> from justunits import AttributeUnitSeparators, UnitStyle
    >>> justunits.set_default_attribute_unit_separator(AttributeUnitSeparators.WHITESPACE_BOXED)
    >>> justunits.set_default_unit_style(UnitStyle.FINE_SLASHED_SUPERSCRIPT)


Reformatting
============

Attribute/value-unit pairs come in many different, justifiable forms. Either they are
demanded by preexisting file format definitions or depend on the context of information
transfer. Transferring different formats depicted in figure 1.


.. doctest::

    >>> import justunits
    >>> from justunits import AttributeUnitSeparators, UnitStyle, UnitDividingStyle
    >>> justunits.reformat_unit("pressure#kg*m^-1*s^-2")
    'pressure [kg/(m⋅s²)]'

Change just the separator in between attribute and unit.

.. doctest::

    >>> justunits.reformat_unit(
    ...     "pressure#kg*m^-1*s^-2",
    ...     target_format=AttributeUnitSeparators.WHITESPACE_IN
    ... )
    'pressure in kg/(m⋅s²)'

Or make custom combinations. Missing definitions will be replaced by defaults.

.. doctest::

    >>> boxed_fine_powered = (
    ...     AttributeUnitSeparators.WHITESPACE_BOXED | UnitDividingStyle.BY_POWER
    ... )
    >>> justunits.reformat_unit(
    ...     "pressure#kg*m^-1*s^-2",
    ...     target_format=boxed_fine_powered
    ... )
    'pressure [kg⋅m⁻¹⋅s⁻²]'

Splitting
=========

You may come across one of these exemplary formats and want to split attributes/values
from units from further processing.

Header of a csv file::

    time[s],energy[J],torque[Nm]
    0.0,0.0,0.0
    ...

Attributes with units in text files::

    ...
    height_mm = 1.0
    width_mm = 2.0
    ...

Or values with units in text files::

    ...
    height = 1.0 mm
    width = 2.0 mm
    ...

split_unit_text
---------------

Splitting attributes/values from units preserving text. The function
:func:`justunits.split_unit_text` provides a splitting whenever a unit detection is
not desired.

.. doctest::

    >>> justunits.split_unit_text("heat capacity[kg/(s^−2*K^-1)*m^2]")
    ('heat capacity', 'kg/(s^−2*K^-1)*m^2')

    >>> justunits.split_unit_text("1.23 apples")
    ('1.23', 'apples')

split_unit
----------

:func:`justunits.split_unit` provides the main feature of detecting units in the
process of splitting.

.. doctest::

    >>> attribute_name, any_units = justunits.split_unit("pressure#kg*m^-1*s^-2")
    >>> attribute_name
    'pressure'

    The unit text is converted into an iterable DerivedUnit-Object containing all detected
    (and unknown units).

    >>> any_units
    (AUnit(kg 'kilogram' mass, 1e+03g), AUnit(m 'meter' length; power=-1), AUnit(s 'second' time; power=-2))

    >>> [str(unit) for unit in any_units]
    ['kg', 'm^-1.0', 's^-2.0']

split_unit converting attribute/value
-------------------------------------

It is also possible to convert the split values by converting them with a
`Callable[[str], Any]``.

.. doctest::

    >>> justunits.split_unit("1.23 apples", converter=float)
    (1.23, (UnknownUnit('apples'),))

Be aware that using a *conversion* function any exception will not be caught.

    >>> justunits.split_unit("1.23 apples", converter=int)
    Traceback (most recent call last):
    ...
    ValueError: invalid literal for int() with base 10: '1.23'

This is intentional as the purpose of the converters result depends on your choice.
Either catch a related exception or take different solutions.

    >>> justunits.split_unit("1.23 apples", converter=lambda x: int(float(x)))
    (1, (UnknownUnit('apples'),))


Joining
=======

:func:`justunits.join` The counterpart of splitting attributes/values-unit pairs joins

.. doctest::

    >>> pressure = justunits.from_string("kg/(m*s^2)")
    >>> justunits.join_unit("pressure", pressure)
    'pressure [kg/(m⋅s²)]'

    >>> from justunits import AttributeUnitSeparators
    >>> justunits.join_unit(
    ...     "pressure", pressure, target_format=AttributeUnitSeparators.WHITESPACE_IN
    ... )
    'pressure in kg/(m⋅s²)'
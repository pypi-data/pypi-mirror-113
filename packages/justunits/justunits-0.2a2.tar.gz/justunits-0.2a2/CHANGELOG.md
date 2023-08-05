# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2a2] - not released
### Changed
- The default attribute unit seperator is now set to 
  *justunits.AttributeUnitSeparators.WHITESPACE_IN* leading to the default result of
  *'pressure in Pa'*.
- The class *BaseUnit* is renamed into *BareUnit* to avoid a name clash with the
  definition of the SI-Base unit. The class *BareUnit* is the definition of any
  custom unit (like *apples*) within the modules runtime-unit-library.
  
### Deprecated
- The class *AnyUnit* is renamed to *DerivedUnit*. *AnyUnit* will be removed within
  the next minor release.
  
### Fixed
- Fixed issue #1 in which the any word starting with lower or uppercase 'e' would
  result into a split like 'experiment' to ('e', 'xperiment').

### Added
- Minor additions; makefile & additional tests.

## [0.2a1] - 21-04-19
### Fixed
- Failed tests in python version 3.6 due to different inheritance behavior of 
  enum.IntFlag.
- A single AUnit now is being processed by *justunits.to_string*.

## Removed
- The concept of *DerivedUnit* and *AUnit* carrying their own style definition and the
  *StyledDetection* is removed before releasing the first alpha release on *pipy.org*.

## [0.2a0] - unreleased
### Added
- A huge chunk of code for unit detection, definition and formatting into different
  styles.
  
## [0.1a0] - unreleased
### Changed
- renamed *encode_text* with *join_unit*
- *join_unit* does not enforce unit separator if `None` or empty unit is supplied. This
  behavior reflects for entities, which doesn't need a unit.

## [0.0a1] - unreleased
Start of justunits.
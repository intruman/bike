# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Fixed
- 5464564

## [0.3.6]
### Added
- Bike model decorator can be used just with model instead of model().
### Fixed
- Fix error on try set an empty string on required field. 

## [0.3.5] - 2023-07-07
### Fixed
- Fixed an error when a model was instantiated by unpacked dict with extra values.


## [0.3.4] - 2023-07-06
### Fixed
- Fixed error when a model object was passed as value.


## [0.3.3] - 2023-07-06
### Fixed
- Fixed error when a model has optionals bike models attributes.


## [0.3.2] - 2023-06-02
### Fixed
- Fixed an error that allow models accept different field types.


## [0.3.1] - 2023-05-26
### Fixed
- Fixed an error on pip install process.


## [0.3.0] - 2023-05-21
### Add
- Model class features.
- Validators.
- Field class to manager fields model.
- A model dict method.
- A model json method.
- __init__ method of Model class created dynamically by Field instance list.
- Nested models.


## [0.2.0] - 2022-03-11


## [0.1.0] - 2022-03-11
### Added
- Created basic project structure.


[Unreleased]: https://github.com/manasseslima/bike/compare/v0.2.0...HEAD
[0.1.0]: https://github.com/manasseslima/bike/releases/tag/v0.1.0
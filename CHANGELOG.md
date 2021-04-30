# Changelog

## [Unreleased]

### Changed

- Timecard settings file now supports line comments. Line must start with `#` to be a comment.
- Deprecate `.timecardrc` in favor of user folders (e.g. `.config/timecard/settings.conf`).
  - If new default settings file doesn't exist, will check for `.timecardrc` before creating new default.
  - If loading from `.timecardrc`, will migrate settings to new location and add migration comments to old location.
- Default location for time logs is now the user data directory (e.g. `.local/share/timecard/`).

## [2.0.7] - 2021-03-24

### Changed

- Make metadata compliant with org.freedesktop expectations

## [2.0.6] - 2021-03-23

### Changed

- Made ready for PySide6 (Qt 6) migration. Only imports and one marked change
  will need to be made to complete the transition. Program is already tested
  against PySide6 v6.0.2.

### Development

- Move `/app/share` to `/share`
- Bring Flatpak up to Flathub standards and expectations.

## [2.0.5] - 2021-03-19

### Added

- Flatpak distribution.

### Fixed

- Logged duration is wrong when stopping paused timer.

## [2.0.4] - 2019-12-29

### Changed

- Renamed executable to `timecard-app` regardless of distribution method.

### Fixed

- Removed 3.8-only debug print line.

## [2.0.3] - 2019-12-29

### Fixed

- Address time doubling behind-the-scenes when stopping timer.
- Add text labels to app buttons, for when icons are not available (e.g. macOS)

## [2.0.0] - 2020-12-19

Initial release.

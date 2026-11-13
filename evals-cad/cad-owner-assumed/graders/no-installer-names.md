---
type: regex
pattern: 'AppImage|flatpak|Homebrew|\.deb\b'
flags: i
match: not_contains
target: last_message
---

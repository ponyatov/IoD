# Package

version       = "0.0.1"
author        = "Dmitry Ponyatov"
description   = "IoD implementation for Android NDK"
license       = "MIT"
srcDir        = "src"
installExt    = @["nim"]
bin           = @["droid"]

backend       = "cpp"

# Dependencies

requires "nim >= 0.20.2"

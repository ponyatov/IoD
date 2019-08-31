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
requires "https://github.com/yglukhov/android"

# Build automation

const cwd = getCurrentDir()

task droid, "generate source code for Android SDK project":
    # configure compiler for code generation
    switch("os","android")  # target os
    switch("cpu","arm")     # most mobiles has ARM
    switch("compileOnly")   # don't run compiler, _translation_ only
    switch("nimcache",cwd & "/nimcache")
    # switch to next nimble command
    setCommand "build"

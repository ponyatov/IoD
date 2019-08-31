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

const home = getEnv("HOME")
const cwd = getCurrentDir()
const cpp = cwd & "/app/src/main/cpp" # project /cpp

# const nimbase = "https://raw.githubusercontent.com/nim-lang/csources/master/c_code/nimbase.h"
const nimbase = home & "/.choosenim/toolchains/nim-" & NimVersion & "/c_code/nimbase.h"

task droid, "generate source code for Android SDK project":
    # configure compiler for code generation
    switch("os","android")    # target os
    switch("cpu","arm")       # most mobiles has ARM
    # switch("t","-m32")
    # switch("l","-m32")
    switch("compileOnly")     # don't run compiler, _translation_ only
    switch("noMain")
    switch("nimcache",cpp)    # add files to app /cpp
    # # prepare .h files
    const h = cpp & "/nimbase.h"
    if not existsFile(h): discard
    writeFile h,"#include " & '"' & nimbase & '"'
    # switch to next nimble command
    # setCommand "build"

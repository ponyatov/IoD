# This is just an example to get you started. A typical hybrid package
# uses this file as the main entry point of the application.

import droidpkg/submodule

when isMainModule:
  echo(getWelcomeMessage())

const ver   = "branch: " & staticExec("git rev-parse --short HEAD")
const os    = system.hostOS
const about = "IoD/" & os & " " & ver

echo about

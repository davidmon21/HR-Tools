include openbox.local

include firefox.local
# Persistent global definitions
include globals.local

noblacklist ${HOME}/.cache/mozilla
noblacklist ${HOME}/.mozilla

mkdir ${HOME}/.cache/mozilla/firefox
mkdir ${HOME}/Pictures
mkdir ${HOME}/Downloads
mkdir ${HOME}/Videos
mkdir ${HOME}/.mozilla

noblacklist ${HOME}/.config/openbox
include disable-common.inc
caps.drop all
netfilter
noroot
protocol unix,inet,inet6
seccomp

whitelist ${HOME}/.config/openbox
whitelist ${HOME}/.cache/mozilla/firefox
whitelist ${HOME}/.mozilla
whitelist ${HOME}/Pictures
whitelist ${HOME}/Videos
whitelist ${HOME}/Downloads
whitelist ${HOME}/.config/tint2
whitelist /usr/bin


noblacklist ${HOME}/.config/discord
noblacklist ${HOME}/HR-Tools/LinuxED/EnhancedDiscord
noblacklist ${HOME}/.config/openbox

mkdir ${HOME}/.config/discord
mkdir ${HOME}/HR-Tools/LinuxED/EnhancedDiscord
whitelist ${HOME}/.config/discord
whitelist ${HOME}/HR-Tools/LinuxED/EnhancedDiscord
include whitelist-common.inc

# Redirect
include electron.profile
include firefox-common.profile

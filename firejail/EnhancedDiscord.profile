
# Firejail profile for riot-web
# Description: A glossy Matrix collaboration client for the web
# This file is overwritten after every install/update
# Persistent local customizations
#include riot-web.local
# Persistent global definitions
include globals.local

noblacklist ${HOME}/.config/discord
noblacklist ${HOME}/HR-Tools/LinuxED/EnhancedDiscord

mkdir ${HOME}/.config/discord
mkdir ${HOME}/HR-Tools/LinuxED/EnhancedDiscord
whitelist ${HOME}/.config/discord
whitelist ${HOME}/HR-Tools/LinuxED/EnhancedDiscord
include whitelist-common.inc

# Redirect
include electron.profile
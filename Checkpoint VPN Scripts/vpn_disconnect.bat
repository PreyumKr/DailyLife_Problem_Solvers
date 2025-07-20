@echo off
echo Disconnecting from VPN...
"Path\To\Your\VPN\CLI\trac.exe" disconnect
if %errorlevel% == 0 (
    echo VPN disconnected successfully!
) else (
    echo Failed to disconnect from VPN. Error code: %errorlevel%
)
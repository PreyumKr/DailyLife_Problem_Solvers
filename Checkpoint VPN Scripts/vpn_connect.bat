@echo off
echo Starting VPN GUI service...
start /min "" "Path\To\Your\VPN\GUI\Service.exe"
echo Connecting to VPN...
"Path\To\Your\VPN\CLI\trac.exe" connect -s <ServerName> -u <UserName> -p <Password>
if %errorlevel% == 0 (
    echo VPN connected successfully!
) else (
    echo Failed to connect to VPN. Error code: %errorlevel%
)
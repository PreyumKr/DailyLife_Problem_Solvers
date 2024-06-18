Clear-Host

Echo "Keep-Alive With Scroll Lock!!!"
$paused = $false

$WShell = New-Object -com "Wscript.shell"

while($true)
{
	if ($paused){
		Echo "Paused! Press Space to resume."
		while($paused){
			$key = [System.Console]::ReadKey($true)
			if($key.key -eq 'Spacebar'){
				$paused = $false
				Echo "Resumed!!!"
			}
		}
	}
	$WShell.sendkeys("{SCROLLLOCK}")
	Start-Sleep -Milliseconds 100
	$WShell.sendkeys("{SCROLLLOCK}")
	Start-Sleep -Milliseconds 240

	$pshost = Get-Host              
	$pswindow = $pshost.UI.RawUI

	$newsize = $pswindow.windowsize 
	$newsize.width = 60    
	$newsize.height = 5           
	$pswindow.windowsize = $newsize
	
	if ([System.Console]::KeyAvailable){
		$key = [System.Console]::ReadKey($true)
		if ($key.key -eq 'Spacebar'){
			$paused = $true
		} 
	}
}
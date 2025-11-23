$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TehNadzor.lnk")
$Shortcut.TargetPath = "C:\Users\PC\StroiNadzor\start_all.bat"
$Shortcut.WorkingDirectory = "C:\Users\PC\StroiNadzor"
$Shortcut.WindowStyle = 7
$Shortcut.Save()

Write-Host "✅ Ярлык создан успешно!" -ForegroundColor Green
Write-Host "Местоположение: $env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TehNadzor.lnk" -ForegroundColor Cyan

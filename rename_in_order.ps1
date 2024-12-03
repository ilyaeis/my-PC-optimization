if ($args.Count -lt 1) {
    Write-Host "Usage: PowerShell -File 'script_name.ps1' <FolderPath>" -ForegroundColor Yellow
    exit
}

$folderPath = $args[0]

# Validate folder path
if (-Not $folderPath -or -Not (Test-Path $folderPath)) {
    Write-Host "Error: Folder does not exist or path is null. Please check the input." -ForegroundColor Red
    exit
}

$files = Get-ChildItem -Path $folderPath -Recurse -File

if ($files.Count -eq 0) {
    Write-Host "No files found in the specified folder." -ForegroundColor Yellow
    exit
}

$count = 1
foreach ($file in $files) {
    # Debugging: Check file information
    Write-Host "Processing file: $($file.FullName)" -ForegroundColor Cyan

    # Generate new name and path
    $newName = "{0}{1}" -f $count, $file.Extension
    $newPath = Join-Path -Path $folderPath -ChildPath $newName

    # Debugging: Check new path
    Write-Host "Renaming to: $newPath" -ForegroundColor Cyan

    # Rename the file
    if ($newPath -and $file.FullName) {
        Rename-Item -Path $file.FullName -NewName $newPath -Force
        $count++
    } else {
        Write-Host "Skipping file: $($file.FullName) due to invalid new path." -ForegroundColor Yellow
    }
}

Write-Host "Files renamed successfully in numeric order." -ForegroundColor Green
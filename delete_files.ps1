if ($args.Count -lt 2) {
    Write-Host "Usage: powershell -File script.ps1 <FolderPath> <SearchString>" -ForegroundColor Yellow
    exit
}

$folderPath = $args[0]
$searchString = $args[1]

if (-Not (Test-Path $folderPath)) {
    Write-Host "Folder does not exist. Please check the path." -ForegroundColor Red
    exit
}

# Get all files in the folder and subfolders
$files = Get-ChildItem -Path $folderPath -Recurse -File

foreach ($file in $files) {
    if ($file.Name -like "*$searchString*") {
        try {
            Remove-Item -Path $file.FullName -Force
            Write-Host "Deleted: $($file.FullName)" -ForegroundColor Green
        } catch {
            Write-Host "Failed to delete: $($file.FullName). Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host "Script completed." -ForegroundColor Cyan
# Simple PowerShell HTTP Server for AutoQI Dashboard
# Port: 3000
# Access at: http://localhost:3000/autoqi_dashboard.html

$port = 3000
$root = $PSScriptRoot

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  AutoQI Dashboard - Local Web Server" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Server running at:" -ForegroundColor Yellow
Write-Host "  http://localhost:$port/autoqi_dashboard.html" -ForegroundColor Green
Write-Host ""
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Server started successfully!" -ForegroundColor Green

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Get requested file path
        $requestedFile = $request.Url.LocalPath.TrimStart('/')
        if ($requestedFile -eq '' -or $requestedFile -eq '/') {
            $requestedFile = 'autoqi_dashboard.html'
        }
        
        $filePath = Join-Path $root $requestedFile
        
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $($request.HttpMethod) $($request.Url.LocalPath)" -ForegroundColor Cyan
        
        if (Test-Path $filePath -PathType Leaf) {
            # Determine content type
            $contentType = "text/html"
            $extension = [System.IO.Path]::GetExtension($filePath)
            switch ($extension) {
                ".html" { $contentType = "text/html; charset=utf-8" }
                ".css"  { $contentType = "text/css; charset=utf-8" }
                ".js"   { $contentType = "application/javascript; charset=utf-8" }
                ".json" { $contentType = "application/json; charset=utf-8" }
                ".png"  { $contentType = "image/png" }
                ".jpg"  { $contentType = "image/jpeg" }
                ".jpeg" { $contentType = "image/jpeg" }
                ".gif"  { $contentType = "image/gif" }
                ".svg"  { $contentType = "image/svg+xml" }
                ".ico"  { $contentType = "image/x-icon" }
                default { $contentType = "application/octet-stream" }
            }
            
            # Read file and send response
            $content = [System.IO.File]::ReadAllBytes($filePath)
            $response.ContentType = $contentType
            $response.ContentLength64 = $content.Length
            $response.StatusCode = 200
            $response.OutputStream.Write($content, 0, $content.Length)
            
            Write-Host "  -> 200 OK ($([math]::Round($content.Length/1KB, 2)) KB)" -ForegroundColor Green
        }
        else {
            # File not found
            $response.StatusCode = 404
            $errorMessage = "404 - File Not Found: $requestedFile"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorMessage)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            
            Write-Host "  -> 404 NOT FOUND" -ForegroundColor Red
        }
        
        $response.Close()
    }
}
catch {
    Write-Host ""
    Write-Host "Server stopped." -ForegroundColor Yellow
}
finally {
    $listener.Stop()
    $listener.Close()
}

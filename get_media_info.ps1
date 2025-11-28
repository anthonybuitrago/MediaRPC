
try {
    # Set output encoding to UTF-8 to avoid UnicodeDecodeError in Python
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

    # Load required assemblies
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    
    # Get the AsTask extension method to convert IAsyncOperation<T> to Task<T>
    $asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | 
        Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.IsGenericMethod } | 
        Select-Object -First 1

    # Load the SMTC Manager Type
    $managerType = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager, Windows.Media.Control, ContentType=WindowsRuntime]
    
    # Call RequestAsync()
    $asyncOp = $managerType::RequestAsync()
    
    # Convert to Task
    $asTask = $asTaskGeneric.MakeGenericMethod([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager])
    $task = $asTask.Invoke($null, @($asyncOp))
    
    # Await the task synchronously
    $manager = $task.GetAwaiter().GetResult()
    
    # Get Current Session
    $session = $manager.GetCurrentSession()

    if ($null -ne $session) {
        # Get Media Properties (Async)
        $asyncOpProps = $session.TryGetMediaPropertiesAsync()
        $asTaskProps = $asTaskGeneric.MakeGenericMethod([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties])
        $taskProps = $asTaskProps.Invoke($null, @($asyncOpProps))
        $props = $taskProps.GetAwaiter().GetResult()

        # Get Playback Info
        $playbackInfo = $session.GetPlaybackInfo()
        $status = $playbackInfo.PlaybackStatus # Enum: Closed, Opened, Changing, Stopped, Playing, Paused

        $output = @{
            title = $props.Title
            artist = $props.Artist
            status = "$status"
            source = $session.SourceAppUserModelId
            thumbnail = "" # Thumbnail is complex (IRandomAccessStreamReference), skipping for now
        }
        
        Write-Output ($output | ConvertTo-Json -Compress)
    } else {
        Write-Output "{}"
    }
} catch {
    $err = $_.Exception.Message
    Write-Output "{ ""error"": ""$err"" }"
}

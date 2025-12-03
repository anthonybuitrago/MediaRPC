try {
    # Load Assembly
    $path = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll"
    [System.Reflection.Assembly]::LoadFrom($path) | Out-Null
    
    # Load WinRT Type
    [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager,Windows.Media,ContentType=WindowsRuntime] | Out-Null
    
    # Get AsTask methods
    $methods = [System.WindowsRuntimeSystemExtensions].GetMethods()
    
    # Find the correct AsTask<T>(IAsyncOperation<T>)
    $asTask = $null
    foreach ($m in $methods) {
        if ($m.Name -eq "AsTask" -and $m.IsGenericMethodDefinition -and $m.GetParameters().Count -eq 1) {
            $paramType = $m.GetParameters()[0].ParameterType
            if ($paramType.Name -match "IAsyncOperation") {
                $asTask = $m
                break
            }
        }
    }

    if (-not $asTask) {
        throw "AsTask method not found"
    }

    # 1. Request Manager
    $async = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]::RequestAsync()
    
    # Make Generic AsTask for Manager
    $tManager = [Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]
    $task = $asTask.MakeGenericMethod($tManager).Invoke($null, @($async))
    
    $task.Wait()
    $manager = $task.Result

    if (-not $manager) {
        throw "Manager is null"
    }

    $session = $manager.GetCurrentSession()
    
    if ($session) {
        $info = $session.GetPlaybackInfo()
        
        # 2. Get Properties
        $asyncProps = $session.TryGetMediaPropertiesAsync()
        
        # We need the type for MediaProperties to make the generic method
        # It is: Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties
        # We can get it from the asyncProps object? No, it's COM.
        # We can get it from the return type of the method?
        $methodInfo = $session.GetType().GetMethod("TryGetMediaPropertiesAsync")
        # The return type is IAsyncOperation<T>, we need T.
        # But $session is a COM object (System.__ComObject) in PS?
        # If so, GetMethod might fail or return null.
        
        # Let's try to load the type by name.
        $tPropsName = "Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties"
        # It's in Windows.Media.winmd.
        # Since we loaded the Manager type, the assembly should be loaded?
        # Manager is in Windows.Media.Control namespace.
        
        # Let's try to get it from the assembly of the Manager type
        $tProps = $tManager.Assembly.GetType($tPropsName)
        
        if (-not $tProps) {
            # Try to find it in the exported types
            $tProps = $tManager.Assembly.GetExportedTypes() | Where-Object { $_.FullName -eq $tPropsName } | Select-Object -First 1
        }

        if ($tProps) {
            $taskProps = $asTask.MakeGenericMethod($tProps).Invoke($null, @($asyncProps))
            $taskProps.Wait()
            $props = $taskProps.Result
            
            $result = @{
                title = $props.Title
                artist = $props.Artist
                status = $info.PlaybackStatus.ToString()
                source = $session.SourceAppUserModelId
            }
            [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
            $result | ConvertTo-Json -Compress
        } else {
            # Fallback if we can't find the type (shouldn't happen)
            Write-Error "Could not find MediaProperties type"
        }
    } else {
        # No active session
        Write-Host "{}"
    }

} catch {
    Write-Error $_
}

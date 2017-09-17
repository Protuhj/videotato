; Toggles the script on and off
f12::
Suspend,Toggle
return

; Switch Chrome tab
f7::
    SendToChrome("^{PgUp}")
return


; Skip to next in playlist
Media_next::
    SendToChrome("+n")
return

; Toggle play
Media_Play_Pause::
    SendToChrome("k")
return

; Play random video
Launch_Mail::
    RunWait, python randomLine.py,,HIDE
    FileRead, vidya, result.txt

    prefixStr = ""
    if ( InStr( vidya, "http", true ) ) {
        ; If the result has a complete URL, use it verbatim
        prefixStr := vidya
    } else {
        ; Otherwise, assume it's a YouTube video ID.
        prefixStr := "https://www.youtube.com/watch?v=" . vidya
    }

    ; Cache clipboard contents
    temp := clipboardall

    ; Put the URL onto the clipboard
    clipboard := prefixStr

    ; Focus address bar then paste the clipboard to the URL box
    SendToChrome("^l^v{Enter}")

    ; Restore the cached clipboard contents
    clipboard := temp
return

; Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT alt + LEFT shift + delete (more difficult since it's destructive)
<!<+Del::
    RunWait, python removeLastVideo.py,,HIDE
return

; Helper function to send keys directly to Chrome if it's focused,
; otherwise use ControlFocus and ControlSend to do the work.
SendToChrome(controlSet) {
    if (IsChromeActive() = False) {
        SetTitleMatchMode, 2

        ControlGet, OutputVar, Hwnd,,Chrome_RenderWidgetHostHWND1, Google Chrome

        ControlFocus,,ahk_id %outputvar%
        ControlSend, , %controlSet% , Google Chrome
    } else {
        Send, %controlSet%
    }
}

; Helper function to see if the user already has Chrome focused.
; ControlSend doesn't seem to work well when the window is already focused.
IsChromeActive() {
    WinGetClass, class, A
    if (class = "Chrome_WidgetWin_1") {
        return True
    } else {
        return False
    }
}

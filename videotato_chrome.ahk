; Toggles the script on and off
f12::
Suspend,Toggle
return

; Switch Chrome tab
f7::
    SetTitleMatchMode, 2

    ControlGet, OutputVar, Hwnd,,Chrome_RenderWidgetHostHWND1, Google Chrome

    ControlFocus,,ahk_id %outputvar%

    ControlSend, , ^{PgUp} , Google Chrome
return


; Skip to next in playlist
Media_next::
    SetTitleMatchMode, 2

    ControlGet, OutputVar, Hwnd,,Chrome_RenderWidgetHostHWND1, Google Chrome

    ControlFocus,,ahk_id %outputvar%

    ControlSend, , +n , Google Chrome
return

; Toggle play
Media_Play_Pause::
    SetTitleMatchMode, 2

    ControlGet, OutputVar, Hwnd,,Chrome_RenderWidgetHostHWND1, Google Chrome

    ControlFocus,,ahk_id %outputvar%

    ControlSend, , k , Google Chrome
return

; Play random video
Launch_Mail::
    RunWait, python randomLine.py,,HIDE
    FileRead, vidya, result.txt
    SetTitleMatchMode, 2

    ControlGet, OutputVar, Hwnd,,Chrome_RenderWidgetHostHWND1, Google Chrome

    ControlFocus,,ahk_id %outputvar%

    ; Select the address bar (ctrl+l)
    ControlSend, , ^l , Google Chrome
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
    ; Paste the clipboard to the URL box
    ControlSend, , ^v{Enter} , Google Chrome
    ; Restore the cached clipboard contents
    clipboard := temp
return

; Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT alt + LEFT shift + delete (more difficult since it's destructive)
<!<+Del::
    RunWait, python removeLastVideo.py,,HIDE
return

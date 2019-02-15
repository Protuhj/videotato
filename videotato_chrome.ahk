; F12                                       - toggle script on/off
; F7                                        - switch Chrome tabs
; Media_next                                - Skip to next in playlist
; Media_play_pause                          - Play/pause video (sends space to tab)
; LEFT alt + LEFT shift + LEFT ctrl + F5    - refresh current tab (sends F5 to tab)
; Launch_Mail                               - Play random video
; Browser_Home                              - Play previous random video
; LEFT alt + LEFT shift + delete            - Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT ctrl + left arrow                    - Go back 10 seconds in a video (sends 'J' to tab)
; LEFT ctrl + right arrow                   - Go forward 10 seconds in a video (sends 'L' to tab)

; Toggles the script on and off
f12::
Suspend,Toggle
return

; Switch Chrome tab
f7::
    SendToChrome("^{PgUp}")
    ;SoundBeep
return


; Skip to next in playlist
Media_next::
    SendToChrome("+n")
return

; Toggle play
Media_Play_Pause::
    ; SendToChrome("k")
    ; It's a space character, not a dot
    SendToChrome(" ")
return

; LEFT alt + LEFT shift + LEFT ctrl + F5
; Refresh the active tab in case some kind of error occurs
<!<+<^f5::
    SendToChrome("{f5}")
return

; Play random video
Launch_Mail::
    RunWait, python randomLine.py,,HIDE
    FileRead, vidya, result.txt

    GoToUrl(vidya)
return

; Play last video
Browser_Home::
    FileRead, vidya, result.txt

    GoToUrl(vidya)
return

; Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT alt + LEFT shift + delete (more difficult since it's destructive)
<!<+Del::
    RunWait, python removeLastVideo.py,,HIDE
return

; Go Back 10 seconds
; LEFT ctrl+ left arrow
<^Left::
    SendToChrome("J")
return

; Go Forward 10 seconds
; LEFT ctrl+ right arrow
<^Right::
    SendToChrome("L")
return

; Scroll down a page
; LEFT CTRL + PAGE DOWN
<^PgDn::
    SendToChrome("{PgDn}")
return

; Scroll up a page
; LEFT CTRL + PAGE UP
<^PgUp::
    SendToChrome("{PgUp}")
return

; Scroll down a little
; LEFT CTRL + LEFT SHIFT + PAGE DOWN
<^<+PgDn::
    SendToChrome("{Down}")
return

; Scroll down a little
; LEFT CTRL + LEFT SHIFT + PAGE UP
<^<+PgUp::
    SendToChrome("{Up}")
return

GoToUrl(videoIDOrFullURL) {
    prefixStr = ""
    if ( InStr( videoIDOrFullURL, "http", true ) ) {
        ; If the result has a complete URL, use it verbatim
        prefixStr := videoIDOrFullURL
    } else {
        ; Otherwise, assume it's a YouTube video ID.
        prefixStr := "https://www.youtube.com/watch?v=" . videoIDOrFullURL
    }

    ; Cache clipboard contents
    temp := clipboardall

    ; Put the URL onto the clipboard
    clipboard := prefixStr

    ; Focus address bar then paste the clipboard to the URL box
    SendToChrome("^l^v{Enter}")

    ; Restore the cached clipboard contents
    clipboard := temp
}

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

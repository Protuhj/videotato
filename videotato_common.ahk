;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
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
; LEFT CTRL + PAGE DOWN                     - Scroll down using Page Down
; LEFT CTRL + PAGE UP                       - Scroll up using Page Up
; LEFT CTRL + LEFT SHIFT + PAGE DOWN        - Scroll down using the down arrow key
; LEFT CTRL + LEFT SHIFT + PAGE UP-         - Scroll down using the up arrow key
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#SingleInstance Force
; ##############################################################################################################################################
; Common functions for Chrome and Firefox
; "SendToBrowser" must be implemented in the including scripts, this one cannot stand alone.
; ##############################################################################################################################################

; Toggles the script on and off
f12::
Suspend,Toggle
return

; Switch tab
f7::
    SendToBrowser("^{PgUp}")
    ;SoundBeep
return

; Skip to next in playlist
Media_next::
    SendToBrowser("+n")
return

; Toggle play
Media_Play_Pause::
    SendToBrowser("k")
    ; It's a space character, not a dot
    ; SendToBrowser(" ")
return

; LEFT alt + LEFT shift + LEFT ctrl + F5
; Refresh the active tab in case some kind of error occurs
<!<+<^f5::
    SendToBrowser("{f5}")
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
    SendToBrowser("J")
return

; Go Forward 10 seconds
; LEFT ctrl+ right arrow
<^Right::
    SendToBrowser("L")
return

; Scroll down a page
; LEFT CTRL + PAGE DOWN
<^PgDn::
    SendToBrowser("{PgDn}")
return

; Scroll up a page
; LEFT CTRL + PAGE UP
<^PgUp::
    SendToBrowser("{PgUp}")
return

; Scroll down a little
; LEFT CTRL + LEFT SHIFT + PAGE DOWN
<^<+PgDn::
    SendToBrowser("{Down}")
return

; Scroll down a little
; LEFT CTRL + LEFT SHIFT + PAGE UP
<^<+PgUp::
    SendToBrowser("{Up}")
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
    ; SendToBrowser("^l^v{Enter}")
    ; Give these time to take effect, so sleep a little between each call
    SendToBrowser("^l")
    Sleep, 20
    SendToBrowser("^v")
    Sleep, 20
    SendToBrowser("{Enter}")

    ; Restore the cached clipboard contents
    clipboard := temp
}


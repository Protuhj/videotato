;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; F12                                       - Toggle script on/off
; F7                                        - Switch tabs Left
; Shift + F7                                - Switch tabs Right
; Ctrl + Alt + T                            - Open a new tab
; Ctrl + Alt + W                            - Close the current tab
; Media_next                                - Skip to next in playlist
; Media_play_pause                          - Play/pause video (sends space to tab)
; LEFT alt + LEFT shift + LEFT ctrl + F5    - refresh current tab (sends F5 to tab)
; Launch_Mail                               - Play random video
; Browser_Home                              - Play previous random video
; LEFT alt + LEFT shift + delete            - Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT ctrl + left arrow                    - Go back 10 seconds in a video (sends 'J' to tab)
; LEFT ctrl + right arrow                   - Go forward 10 seconds in a video (sends 'L' to tab)
; LEFT ctrl + ALT + PAGE DOWN               - Scroll down using Page Down
; LEFT ctrl + ALT + PAGE UP                 - Scroll up using Page Up
; LEFT ctrl + LEFT SHIFT + PAGE DOWN        - Scroll down using the down arrow key
; LEFT ctrl + LEFT SHIFT + PAGE UP-         - Scroll down using the up arrow key
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#SingleInstance Force
; ##############################################################################################################################################
; Common functions for Chrome and Firefox
; Functions to be implemented in the including scripts, this one cannot stand alone:
;   SendToBrowser(command string) - specific logic needed to send the commands to the specific browser/sink
;   GoToUrl(youtube ID or full URL) - default behavior is to just call GoToUrl_Base(..), you can change the behavior as needed for a sink I haven't added
; ##############################################################################################################################################

; Toggles the script on and off
f12::
Suspend,Toggle
return

; Switch tab Left
f7::
    SendToBrowser("^{PgUp}")
    ;SoundBeep
return

; Switch tab right
+f7::
    SendToBrowser("^{PgDn}")
    ;SoundBeep
return

; Ctrl + Alt + t
; Open a new tab
^!t::
    SendToBrowser("^t")
    ;SoundBeep
return

; Ctrl + Alt + w
; Close the current tab
^!w::
    SendToBrowser("^w")
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
    ;SendToBrowser("J")
    SendToBrowser("{Left}")
return

; Go Forward 10 seconds
; LEFT ctrl+ right arrow
<^Right::
    ;SendToBrowser("L")
    SendToBrowser("{Right}")
return

; Scroll down a page
; LEFT CTRL + ALT + PAGE DOWN
<^!PgDn::
    SendToBrowser("{PgDn}")
return

; Scroll up a page
; LEFT CTRL + ALT + PAGE UP
<^!PgUp::
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

GoToUrl_Base(videoIDOrFullURL) {
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
    clipboard := ""
    ; Put the URL onto the clipboard
    clipboard := prefixStr
    ClipWait, 2
    ; Focus address bar then paste the clipboard to the URL box
    ; SendToBrowser("^l^v{Enter}")
    ; Give these time to take effect, so sleep a little between each call
    SendToBrowser("^l")
    Sleep, 25
    SendToBrowser("^v")
    Sleep, 25
    SendToBrowser("{Enter}")
    Sleep, 25
    ; Restore the cached clipboard contents
    clipboard := temp
}


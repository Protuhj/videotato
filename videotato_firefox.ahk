;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; F12                                       - toggle script on/off
; F7                                        - switch Firefox tabs
; Media_next                                - Skip to next in playlist
; Media_play_pause                          - Play/pause video (sends space to tab)
; LEFT alt + LEFT shift + LEFT ctrl + F5    - refresh current tab (sends F5 to tab)
; Launch_Mail                               - Play random video
; Browser_Home                              - Play previous random video
; LEFT alt + LEFT shift + delete            - Remove the last result's text from all output files (for videos you don't want to play again)
; LEFT ctrl + left arrow                    - Go back 10 seconds in a video (sends 'J' to tab)
; LEFT ctrl + right arrow                   - Go forward 10 seconds in a video (sends 'L' to tab)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#include videotato_common.ahk

; ##############################################################################################################################################
; Videotato implementation for Firefox
; ##############################################################################################################################################

; Overridden function from videotato_common
SendToBrowser(controlSet) {
    SendToFirefox(controlSet)
}

; Overridden function from videotato_common
GoToUrl(videoIDOrFullURL) {
    GoToUrl_Base(videoIDOrFullURL)
}

; Helper function to send keys directly to Firefox if it's focused,
; otherwise use ControlFocus and ControlSend to do the work.
SendToFirefox(controlSet) {

    if (IsFirefoxActive() = False) {
        SetTitleMatchMode, 2

        ;ControlGet, OutputVar, Hwnd,,MozillaWindowClass,Mozilla Firefox
        ;ControlGet, OutputVar, Hwnd,,MozillaWindowClass
        ;MsgBox %OutputVar%
        ;ControlFocus,,ahk_id %OutputVar%
        ;ControlFocus,,ahk_class MozillaWindowClass
        ;ControlSend, , %controlSet% , Mozilla Firefox
        ControlSend, ahk_parent, %controlSet% , ahk_class MozillaWindowClass
    } else {
        Send, %controlSet%
    }
}

; Helper function to see if the user already has Firefox focused.
; ControlSend doesn't seem to work well when the window is already focused.
IsFirefoxActive() {
    WinGetClass, class, A
    if (class = "MozillaWindowClass") {
        return True
    } else {
        return False
    }
}

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Launch_Mail                               - Play random video
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#include videotato_common.ahk

; ##############################################################################################################################################
; Videotato implementation for using the ytcast program
; ##############################################################################################################################################

; Overridden function from videotato_common
SendToBrowser(controlSet) {
    ; Do nothing, since we can't send control commands via ytcast
}

; Overridden function from videotato_common
GoToUrl(videoIDOrFullURL) {
    prefixStr = ""
    if ( InStr( videoIDOrFullURL, "http", true ) ) {
        ; If the result has a complete URL, use it verbatim
        prefixStr := videoIDOrFullURL
    } else {
        ; Otherwise, assume it's a YouTube video ID.
        prefixStr := "https://www.youtube.com/watch?v=" . videoIDOrFullURL
    }

    RunWait, C:\extended_path\ytcast\ytcast.exe -p %prefixStr%,,HIDE 
}
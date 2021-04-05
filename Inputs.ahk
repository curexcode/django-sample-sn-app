; py .\manage.py makemigrations
; py .\manage.py migrate 
; py .\manage.py createsuperuser

; phone +919999999999
; name admin2
; gen male
; city delmasca
; Password somethingsomething
; Password2 somethingsomething

Numpad0::fill_superuser_form()
; Numpad1::git_push()
; Numpad2::ns()
; Numpad3::move_mouse()
; Numpad4::type_sen()
; Numpad5::login_burger()
; Numpad6::fill_form_burger()

fill_superuser_form(){
	Send py .\manage.py makemigrations  
	Send {Enter}
	Send py .\manage.py migrate 
	Send {Enter}
    Send py .\manage.py createsuperuser
	Send {Enter}
    Sleep 8000
    Send {NumpadAdd}919999999999
	Send {Enter}
    Send Admin
	Send {Enter}
    Send male 
    Send {Enter}
    Send Delmasca
    Send {Enter}
    Send somethingsomething
    Send {Enter}
    Send somethingsomething
    Send {Enter}
}


; login_burger(){
;     SendRaw hello@g.com
;     Send %A_Tab%
;     Send hello123
;     Send %A_Tab%
;     Send {Enter}
; }

; ns(){
;     Send npm start
;     Return
; }

; git_commit(){
;     Send git add . {Enter}
;     Send git commit -m ""
;     return
; }


; git_push(){
;     Send git push -u{Space} origin master {Enter}
;     return
; }
; move_mouse(){
;     MouseMove, 1300, 500, 0, 
; }

; type_sen(){
;     Send are we ask why eat no know mom family very Indian not you American some very
; }
.model small
.stack 100h

.data
; ----------------
; data section
; ----------------
msg_insert      db 13,10,'insert your card (press enter)...$'
msg_pin         db 13,10,'enteryour account pin: $'
msg_wrong_pin   db 13,10,'incorrect pin. try again.',13,10,'$'
msg_blocked     db 13,10,'too many incorrect attempts. card blocked.$'
msg_menu        db 13,10,'1. deposit',13,10,'2. withdraw',13,10,'3. exit',13,10,'4. change pin',13,10,'5. check balance',13,10,'choice: $'  ; updated
msg_deposit     db 13,10,'enter amount to deposit: $'
msg_withdraw    db 13,10,'enter amount to withdraw: $'
msg_insuff      db 13,10,'insufficient funds.$'
msg_balance     db 13,10,'current balance: $'
msg_exit        db 13,10,'thank you. goodbye.$'
msg_change_pin  db 13,10,'enter the new pin: $'
msg_pin_changed db 13,10,'pin changed successfully!$'

correct_pin     db '1234'      ; pin
entered_pin     db 4 dup(0)    ; buffer pin to enter
attempts        db 3           ; 3 attemps to ck 
balance         dw 0000        ; int  balance
temp_amount     dw 0           ; temp amount storage
temp_digit      dw 0           ; multi digit handle

.code
main proc
; ----------------
; init segment
; ----------------
mov ax, @data
mov ds, ax

; ----------------
; insert card (press enter)
; ----------------
mov dx, offset msg_insert
mov ah, 09h
int 21h

.wait_enter:
mov ah, 01h
int 21h
cmp al, 13      ; check for enter key
jne .wait_enter

; ----------------
; pin authentication
; ----------------
auth:
cmp attempts, 0
je blocked

mov dx, offset msg_pin
mov ah, 09h
int 21h

; read 4-digit pin
mov si, 0
read_pin:
mov ah, 01h
int 21h
mov entered_pin[si], al
inc si
cmp si, 4
jne read_pin

; compare with correct pin
mov si, 0
mov di, 0
mov cx, 4
check_pin:
mov al, entered_pin[si]
cmp al, correct_pin[di]
jne wrong_pin
inc si
inc di
loop check_pin
jmp menu        ; authentication successful

wrong_pin:
dec attempts
mov dx, offset msg_wrong_pin
mov ah, 09h
int 21h
jmp auth

blocked:
mov dx, offset msg_blocked
mov ah, 09h
int 21h
jmp exit

; ----------------
; main menu
; ----------------
menu:
mov dx, offset msg_menu
mov ah, 09h
int 21h

; get user choice
mov ah, 01h
int 21h

cmp al, '1'
je deposit
cmp al, '2'
je withdraw
cmp al, '3'
je exit
cmp al, '4'
je change_pin
cmp al, '5'     ; new option for check balance
je show_bal
jmp menu        ; invalid choice, show menu again

; ----------------
; deposit
; ----------------
deposit:
mov dx, offset msg_deposit
mov ah, 09h
int 21h

mov temp_amount, 0

read_deposit:
mov ah, 01h
int 21h
cmp al, 13      ; enter key pressed
je add_deposit

sub al, '0'
mov ah, 0
mov temp_digit, ax

mov ax, temp_amount
mov cx, 10
mul cx
add ax, temp_digit
mov temp_amount, ax

jmp read_deposit

add_deposit:
mov ax, balance
add ax, temp_amount
mov balance, ax
jmp show_bal

; ----------------
; withdraw
; ----------------
withdraw:
mov dx, offset msg_withdraw
mov ah, 09h
int 21h

mov temp_amount, 0

read_withdraw:
mov ah, 01h
int 21h
cmp al, 13      ; enter key pressed
je check_funds

sub al, '0'
mov ah, 0
mov temp_digit, ax

mov ax, temp_amount
mov cx, 10
mul cx
add ax, temp_digit
mov temp_amount, ax

jmp read_withdraw

check_funds:
mov ax, balance
cmp ax, temp_amount
jl insufficient

sub ax, temp_amount
mov balance, ax
jmp show_bal

insufficient:
mov dx, offset msg_insuff
mov ah, 09h
int 21h
jmp menu

; ----------------
; show balance
; ----------------
show_bal:
mov dx, offset msg_balance
mov ah, 09h
int 21h

; convert balance to ascii and display
mov ax, balance
mov cx, 0
mov bx, 10

push_digits:
mov dx, 0
div bx
push dx
inc cx
cmp ax, 0
jne push_digits

pop_digits:
pop dx
add dl, '0'
mov ah, 02h
int 21h
loop pop_digits

jmp menu

; ----------------
; change pin
; ----------------
change_pin:
mov dx, offset msg_change_pin
mov ah, 09h
int 21h

mov si, 0
new_pin:
mov ah, 01h
int 21h
mov correct_pin[si], al
inc si
cmp si, 4
jne new_pin

mov dx, offset msg_pin_changed
mov ah, 09h
int 21h

mov attempts, 3
jmp auth

; ----------------
; exit
; ----------------
exit:
mov dx, offset msg_exit
mov ah, 09h
int 21h

mov ax, 4c00h
int 21h

main endp
end main
.MODEL SMALL
.STACK 100H

.DATA
; ----------------
; Data Section
; ----------------
msg_insert     db 13,10,'Insert your card (press ENTER)...$'
msg_pin        db 13,10,'Enter 4-digit PIN: $'
msg_wrong_pin  db 13,10,'Incorrect PIN. Try again.',13,10,'$'
msg_blocked    db 13,10,'Too many incorrect attempts. Card blocked.$'
msg_menu       db 13,10,'1. Deposit',13,10,'2. Withdraw',13,10,'3. Exit',13,10,'4. Change PIN',13,10,'Choice: $'
msg_deposit    db 13,10,'Enter amount to deposit: $'
msg_withdraw   db 13,10,'Enter amount to withdraw: $'
msg_insuff     db 13,10,'Insufficient funds.$'
msg_balance    db 13,10,'Current balance: $'
msg_exit       db 13,10,'Thank you. Goodbye.$'
msg_change_pin db 13,10,'Enter new 4-digit PIN: $'
msg_pin_changed db 13,10,'PIN changed successfully!$'

correct_pin    db '1234'
entered_pin    db 4 dup(0)
attempts       db 3
balance        dw 1000
temp_amount    dw 0

.CODE
MAIN PROC
; ----------------
; Init segment
; ----------------
MOV AX, @DATA
MOV DS, AX

; ----------------
; Step 1: Insert Card
; ----------------
MOV DX, OFFSET msg_insert
MOV AH, 09H
INT 21H

.wait_enter:
MOV AH, 01H
INT 21H
CMP AL, 13
JNE .wait_enter

; ----------------
; Step 2: PIN Authentication
; ----------------
AUTH:
CMP attempts, 0
JE BLOCKED

MOV DX, OFFSET msg_pin
MOV AH, 09H
INT 21H

MOV SI, 0
READ_PIN:
MOV AH, 01H
INT 21H
MOV entered_pin[SI], AL
INC SI
CMP SI, 4
JNE READ_PIN

; Compare PIN
MOV SI, 0
MOV DI, 0
MOV CX, 4
CHECK_PIN:
MOV AL, entered_pin[SI]
CMP AL, correct_pin[DI]
JNE WRONG
INC SI
INC DI
LOOP CHECK_PIN
JMP MENU

WRONG:
DEC attempts
MOV DX, OFFSET msg_wrong_pin
MOV AH, 09H
INT 21H
JMP AUTH

BLOCKED:
MOV DX, OFFSET msg_blocked
MOV AH, 09H
INT 21H
JMP EXIT

; ----------------
; Step 3: Main Menu
; ----------------
MENU:
MOV DX, OFFSET msg_menu
MOV AH, 09H
INT 21H

MOV AH, 01H
INT 21H
CMP AL, '1'
JE DEPOSIT
CMP AL, '2'
JE WITHDRAW
CMP AL, '3'
JE EXIT
CMP AL, '4'
JE CHANGE_PIN
JMP MENU

; ----------------
; Step 4: Deposit
; ----------------
DEPOSIT:
    ; Display deposit prompt
    MOV DX, OFFSET msg_deposit
    MOV AH, 09H
    INT 21H

    ; Initialize variables
    XOR BX, BX        ; BX will hold our running total (temp_amount)
    
READ_DIGIT:
    ; Read one character
    MOV AH, 01H
    INT 21H
    
    ; Check for ENTER key (end input)
    CMP AL, 13
    JE .ADD_TO_BALANCE
    
    ; Convert ASCII to digit (0-9)
    SUB AL, '0'
    XOR AH, AH        ; AX = digit (0-9)
    
    ; temp_amount = temp_amount * 10 + new_digit
    MOV CX, 10
    MOV DX, BX        ; Save current amount
    MOV BX, AX        ; Save new digit
    MOV AX, DX        ; AX = current amount
    MUL CX            ; AX = AX * 10
    ADD AX, BX        ; Add the new digit
    MOV BX, AX        ; Store back in BX
    
    JMP READ_DIGIT

.ADD_TO_BALANCE:
    ; Add to balance
    MOV AX, balance
    ADD AX, BX
    MOV balance, AX
    
    ; Show new balance
    JMP SHOW_BAL

; ----------------
; Step 5: Withdraw
; ----------------
WITHDRAW:
    ; Display withdraw prompt
    MOV DX, OFFSET msg_withdraw
    MOV AH, 09H
    INT 21H

    ; Initialize BX to 0 without XOR
    MOV BX, 0        ; BX will hold our running total (temp_amount)
    
READ_WITHDRAW_DIGIT:
    ; Read one character
    MOV AH, 01H
    INT 21H
    
    ; Check for ENTER key (end input)
    CMP AL, 13
    JE .CHECK_WITHDRAWAL
    
    ; Convert ASCII to digit (0-9)
    SUB AL, '0'
    MOV AH, 0        ; Clear AH (alternative to XOR AH,AH)
    MOV [temp_digit], AX ; Store digit temporarily
    
    ; temp_amount = temp_amount * 10 + new_digit
    MOV AX, BX       ; Move current amount to AX
    MOV CX, 10
    MUL CX           ; AX = AX * 10
    ADD AX, [temp_digit] ; Add the new digit
    MOV BX, AX       ; Store back in BX
    
    JMP READ_WITHDRAW_DIGIT

.CHECK_WITHDRAWAL:
    ; Check if sufficient funds
    MOV AX, balance
    CMP AX, BX
    JL .INSUFFICIENT_FUNDS
    
    ; Subtract from balance
    SUB AX, BX
    MOV balance, AX
    
    ; Show new balance
    JMP SHOW_BAL

.INSUFFICIENT_FUNDS:
    MOV DX, OFFSET msg_insuff
    MOV AH, 09H
    INT 21H
    JMP MENU

; Add to your data section:
temp_digit dw 0      ; Temporary storage for digit
; ----------------
; Step 6: Show Balance
; ----------------
SHOW_BAL:
MOV DX, OFFSET msg_balance
MOV AH, 09H
INT 21H

MOV AX, balance
MOV CX, 0
MOV BX, 10
PUSH_LOOP:
MOV DX, 0
DIV BX
PUSH DX
INC CX
CMP AX, 0
JNE PUSH_LOOP

POP_LOOP:
POP DX
ADD DL, '0'
MOV AH, 02H
INT 21H
LOOP POP_LOOP

JMP MENU

; ----------------
; Step 7: Change PIN
; ----------------
CHANGE_PIN:
MOV DX, OFFSET msg_change_pin
MOV AH, 09H
INT 21H

MOV SI, 0
NEW_PIN_INPUT:
MOV AH, 01H
INT 21H
MOV correct_pin[SI], AL
INC SI
CMP SI, 4
JNE NEW_PIN_INPUT

MOV DX, OFFSET msg_pin_changed
MOV AH, 09H
INT 21H

JMP MENU

; ----------------
; Step 8: Exit
; ----------------
EXIT:
MOV DX, OFFSET msg_exit
MOV AH, 09H
INT 21H

MOV AX, 4C00H
INT 21H
MAIN ENDP
END MAIN

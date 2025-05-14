.model small
.stack 100h

.data 
    welcome db "Welcome to banking system!$"
    menu db 13,10, '[1] Create Account', 13,10, '[2] Login', 13,10, '[3] Exit', 13,10, 'Choice: $'
    newlinee db 13,10, '$'
    ask_user db 'Enter username: $'
    ask_pass db 'Enter password: $'
    acc_created db 'Account created successfully!',13,10,'$'
    login_success db 'Login successful!',13,10,'$'
    login_failed db 'Login failed! Incorrect password!',13,10,'$'
    user_full db 'User limit reached!',13,10,'$'
    deposit_msg db 'Enter amount to deposit (Max 65,536): $'
    withdraw_msg db 'Enter amount to withdraw (Max 65,536): $'
    balance_msg db 'Your current balance is: $'
    not_enough_msg db 10,13, 'Insufficient funds!',13,10,'$'
    update_success db 10,13, 'Transaction completed!',13,10,'$'
    history_msg db 'Transaction history:',13,10,'$'
    interest_msg db 10,13, 'Simple interest is: $'
    enter_years db 'Enter number of years: $'
    not_enough db "Not enough balance to withdraw!", 13, 10, "$" 
    usernotfound db 10,13, "Username not found.$"
    
    
    msg_deposit db 'Deposit: $'
    msg_withdraw db 'Withdraw: $'
    no_txn_msg db 'No transaction history found.', '$'

    

    usernames db 90 dup('$')
    passwords db 90 dup('$')
    balances dw 3 dup(0)
    transactions dw 200 dup(?)
    user_count dw 0
    logged_in dw -1 

    temp_input db 30 dup('$')
    temp_input_pass db 30 dup('$') 
      
    transaction_ptrs dw 0,0,0     ; current index for each user's transaction list
    cx_limit dw 90

    dash_menu db '[1] Deposit',13,10,'[2] Withdraw',13,10,'[3] Balance',13,10,'[4] History',13,10,'[5] Interest',13,10,'[6] Logout',13,10,'Choice: $'

.code  
main: 
    
    mov ax, @data
    mov ds, ax    
    LEA DX, welcome
    call print_str
main_menu:
    lea dx, menu
    call print_str

    mov ah, 01h
    int 21h
    mov bl, al
flush:
    mov ah, 01h
    int 21h
    cmp al, 13
    jne flush    
    
    cmp bl, '1'
    je create_account
    cmp bl, '2'
    je login_user
    cmp bl, '3'
    je exit_program
    jmp main_menu

create_account:
    mov ax, user_count
    cmp ax, 3
    jae max_users

    call newline
    lea dx, ask_user
    call print_str

    ; Calculate username index
    mov ax, user_count
    mov bx, 30
    mul bx
    lea si, usernames
    add si, ax
    call input_user

    call newline
    lea dx, ask_pass
    call print_str

    mov ax, user_count
    mov bx, 30
    mul bx
    lea si, passwords
    add si, ax
    call input_pass

    inc user_count
    lea dx, acc_created
    call print_str
    jmp main_menu

max_users:
    call newline
    lea dx, user_full
    call print_str
    jmp main_menu

login_user:
    call newline
    lea dx, ask_user
    call print_str
    lea di, temp_input
    call get_input

    xor si, si             ; si = offset to usernames
    xor bx, bx             ; bx = index
login_loop:
    mov ax, bx
    mov cx, 30
    mul cx
    lea si, usernames
    add si, ax
    lea di, temp_input
    call compare_strings
    cmp al, 1
    je username_found
    inc bx
    cmp bx, user_count
    jb login_loop

    call newline
    lea dx, usernotfound
    call print_str
    jmp main_menu

username_found:
    call newline
    lea dx, ask_pass
    call print_str
    lea di, temp_input_pass
    call get_input

    ; passwords + bx * 30
    mov ax, bx
    mov cx, 30
    mul cx
    lea si, passwords
    add si, ax
    lea di, temp_input_pass
    call compare_strings
    cmp al, 1
    je login_ok
    call newline
    lea dx, login_failed
    call print_str
    jmp main_menu

login_ok:
    mov logged_in, bx
    call newline
    lea dx, login_success
    call print_str
    jmp user_dashboard

user_dashboard:
    ; ... (same as before, just use proper indexing as below)

    call newline
    lea dx, newlinee
    call print_str
    lea dx, dash_menu
    call print_str

    mov ah, 01h
    int 21h
    mov bl, al
dash_flush:
    mov ah, 01h
    int 21h
    cmp al, 13
    jne dash_flush

    cmp bl, '1'
    je deposit
    cmp bl, '2'
    je withdraw
    cmp bl, '3'
    je show_balance
    cmp bl, '4'
    je show_history
    cmp bl, '5'
    je calc_interest
    cmp bl, '6'
    je main_menu
    jmp user_dashboard

deposit:
    call newline
    lea dx, deposit_msg
    call print_str
    call read_number             ; DX = deposit amount

    ; Add deposit to current balance
    mov ax, logged_in
    shl ax, 1                    ; word offset (2 bytes per balance)
    mov bx, ax
    mov cx, [balances + bx]
    add cx, dx
    mov [balances + bx], cx     ; updated balance

     

    ; Log transaction
    ; Get transaction index for this user
; Simplified Transaction Logging
    ; Get current user's transaction pointer
    mov ax, logged_in
    shl ax, 1
    lea si, transaction_ptrs
    add si, ax
    mov cx, [si]              ; cx = current transaction index (word offset)

    ; Compute offset into transactions array
    shl cx, 1                 ; convert word index to byte offset (2 bytes per word)
    lea di, transactions
    add di, cx

    ; Store transaction type (1 = deposit)
    mov word ptr [di], 1

    ; Store transaction amount just after
    add di, 2
    mov word ptr [di], dx

    ; Update transaction_ptrs[logged_in] += 2 (since 2 entries added)
    mov cx, [si]
    add cx, 2
    mov [si], cx

    lea dx, update_success
    call print_str

    jmp user_dashboard


withdraw:
    call newline
    lea dx, withdraw_msg
    call print_str
    call read_number           ; user input in DX

    push dx                    ; save withdrawal amount

    mov ax, logged_in
    shl ax, 1
    mov bx, ax
    mov cx, [balances + bx]    ; CX = current balance

    pop dx                     ; restore withdrawal amount

    call check_within_90_percent
    ja withdraw_too_much       ; CF = 1 means too much

    cmp cx, dx                 ; balance vs withdrawal
    jb not_enough_funds

    sub cx, dx
    mov [balances + bx], cx     
 
   
    ; 2 = deposit 
    ; Log withdrawal as negative amount
; Simplified Transaction Logging
    ; Get current user's transaction pointer
    mov ax, logged_in
    shl ax, 1
    lea si, transaction_ptrs
    add si, ax
    mov cx, [si]              ; cx = current transaction index (word offset)

    ; Compute offset into transactions array
    shl cx, 1                 ; convert word index to byte offset (2 bytes per word)
    lea di, transactions
    add di, cx

    ; Store transaction type (2 = withdraw)
    mov word ptr [di], 2

    ; Store transaction amount just after
    add di, 2
    mov word ptr [di], dx

    ; Update transaction_ptrs[logged_in] += 2 (since 2 entries added)
    mov cx, [si]
    add cx, 2
    mov [si], cx
    lea dx, update_success
    call print_str

    jmp user_dashboard

withdraw_too_much:
    call newline
    lea dx, not_enough
    call print_str
    jmp user_dashboard


show_balance:
    call newline
    lea dx, balance_msg
    call print_str

    mov ax, logged_in
    shl ax, 1
    mov bx, ax
    mov ax, [balances + bx]
    call print_number

    call newline
    jmp user_dashboard

calc_interest:
    call newline
    lea dx, enter_years
    call print_str
    call read_number         ; DX = number of years
    mov cx, dx               ; CX = number of years (loop counter)

    lea dx, interest_msg
    call print_str

    ; Get principal from balances[]
    mov ax, logged_in        ; Get user index
    shl ax, 1                ; Multiply by 2 (word offset)
    mov bx, ax
    mov ax, [balances + bx]  ; AX = principal
    mov si, ax               ; SI = original principal (for interest calculation)

.loop3:
    ; AX = balance
    mov dx, 0
    mov bx, 110              ; Multiply by 110 (to add 10%)
    mul bx                   ; DX:AX = AX * 110

    mov bx, 100
    div bx                   ; AX = (balance * 110) / 100 (rounded compound)

    loop .loop3               ; Repeat for CX times (years)

    ; Now AX = final balance after compound interest
    sub ax, si               ; AX = interest = final - principal

    call print_number
    call newline
    jmp user_dashboard



not_enough_funds:
    call newline
    lea dx, not_enough
    call print_str
    jmp user_dashboard 

show_history:
    call newline
    lea dx, history_msg
    call print_str

    ; Get transaction pointer for current user
    mov ax, logged_in
    shl ax, 1
    lea si, transaction_ptrs
    add si, ax
    mov cx, [si]       ; total entries for user (each transaction = 2 words)

    cmp cx, 0
    je no_transactions

    xor bx, bx         ; index into transaction entries

print_next_transaction:
    cmp bx, cx
    jae end_history

    ; calculate offset in transactions: 2 bytes per entry
    mov ax, bx
    shl ax, 1
    lea di, transactions
    add di, ax

    ; Get transaction type (1 = deposit, 2 = withdraw)
    mov dx, [di]
    cmp dx, 1
    je show_deposit
    cmp dx, 2
    je show_withdraw
    jmp skip

show_deposit:
    call newline
    lea dx, msg_deposit
    call print_str
    jmp show_amount

show_withdraw:
    call newline
    lea dx, msg_withdraw
    call print_str

show_amount:
    add di, 2         ; move to amount word
    mov ax, [di]
    call print_number
    jmp skip

skip:
    add bx, 2
    jmp print_next_transaction

end_history:
    call newline
    jmp user_dashboard

no_transactions:
    call newline
    lea dx, no_txn_msg
    call print_str
    jmp user_dashboard

   


; ------------------- UTILITIES ---------------------

get_input:
    xor cx, cx
.get_loop:
    mov ah, 01h
    int 21h
    cmp al, 13
    je .done
    mov [di], al
    inc di
    inc cx
    cmp cx, 30
    jl .get_loop
.done:
    mov byte ptr [di], '$'
    ret

read_number:
    xor dx, dx        ; Clear DX (result)
    xor cx, cx
.rloop:
    mov ah, 01h
    int 21h           ; Read character into AL
    cmp al, 13
    je .rend          ; Enter key pressed ? finish input

    cmp al, '0'
    jb .rloop         ; If below '0', ignore and repeat
    cmp al, '9'
    ja .rloop         ; If above '9', ignore and repeat

    sub al, '0'       ; Convert ASCII to number
    mov cl, al
    mov ax, dx
    mov bx, 10
    mul bx            ; AX = DX * 10
    add ax, cx
    mov dx, ax        ; DX = result
    jmp .rloop

.rend:
    ret


compare_strings:
    push cx
    mov cx, 30
    mov al, 1
cmp_loop:
    mov dl, [si]
    mov dh, [di]
    cmp dl, dh
    jne no_match
    cmp dl, '$'
    je match
    inc si
    inc di
    loop cmp_loop
match:
    pop cx
    ret
no_match:
    mov al, 0
    pop cx
    ret

print_str:
    mov ah, 09h
    int 21h
    ret

newline:
    lea dx, newlinee
    call print_str
    ret

input_user:
    mov cx, 0
read_loop:
    mov ah, 1
    int 21h
    cmp al, 13
    je end_inputu
    mov bx, si
    add bx, cx
    mov [bx], al
    inc cx
    cmp cx, 29
    je end_inputu
    jmp read_loop
end_inputu:
    mov bx, si
    add bx, cx
    mov [bx], '$'
    ret

input_pass:
    mov cx, 0
read_loop2:
    mov ah, 1
    int 21h
    cmp al, 13
    je end_inputp
    mov bx, si
    add bx, cx
    mov [bx], al
    inc cx
    cmp cx, 30
    je end_inputp
    jmp read_loop2
end_inputp:
    mov bx, si
    add bx, cx
    mov [bx], '$'
    ret



print_number:
    push ax
    push bx
    push cx
    push dx

    mov cx, 0
    mov bx, 10
.pn_loop:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz .pn_loop

.print_digits:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop .print_digits

    pop dx
    pop cx
    pop bx
    pop ax
    ret


; Checks if dx <= 90% of cx
; Input:
;   CX = full balance
;   DX = withdrawal amount
; Output:
;   CF set if DX > 90% of CX
check_within_90_percent proc
    push ax
    push bx
    push dx     ; save withdrawal amount

    mov ax, cx  ; AX = full balance
    mov bx, 90
    mul bx      ; AX = balance * 90
    mov bx, 100
    div bx      ; AX = 90% of balance

    pop dx      ; get withdrawal amount back
    cmp dx, ax  ; is withdrawal > 90% ?
    ; CF=1 if dx > ax

    pop bx
    pop ax
    ret
check_within_90_percent endp

exit_program:
    mov ah, 4Ch
    int 21h

end main
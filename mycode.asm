.MODEL SMALL
.STACK 100H
.DATA 
msg1 db "Enter First Num:?$"
msg2 db "Enterr second Num:?$"
msgadd db 13,10, "Addition:?$"
msgsub db 13,10 ,"Subtraction:?$"
msgmul db 13,10 ," Multiplication:?$"
msgdiv db 13,10 ,"DIvision:?$"

.CODE
MAIN PROC
    Mov AX,@Data
    Mov DS ,AX
    
    ; first num
    lea DX,msg1
    mov AH, 9
    int 21h
    mov AH, 1
    int 21h
    sub AL ,48
    mov BL,AL 
    ; 2nd  num
    lea DX,msg2
    mov AH, 9
    int 21h
    mov AH, 1
    int 21h
    sub AL ,48
    mov CL,AL 
    
    ;addition
    mov AL,BL
    add AL,CL
    add AL,48 ;ascii convert
    lea DX, msgadd
    mov AH,9
    int 21h
    mov DL,AL   
    mov AH,2
    int 21h   
    ;substration
    
    mov AL,BL
    sub AL,CL
    add AL,48 ;ascii convert
    lea DX, msgsub
    mov AH,9
    int 21h
    mov DL,AL   
    mov AH,2
    int 21h  
        ;multipilcation
    mov AL,BL
    mul CL
    add AL,48 ;ascii convert
    lea DX, msgmul
    mov AH,9
    int 21h
    mov DL,AL   
    mov AH,2
    int 21h   
    
            ;division
    mov AL,BL  
    mov AH, 0
    div CL   ; quotient in AL 
    add AL,48 ;ascii convert
    lea DX, msgdiv
    mov AH,9
    int 21h
    mov DL,AL   
    mov AH,2
    int 21h  
    
    mov AH, 4CH
    int 21h
MAIN ENDP
END MAIN
 Task Title: Check If a Number Is Divisible by
Both 5 and 11     
.MODEL SMALL
.STACK 100H
.DATA 
A DB 13,10,"THIS IS NOT DIVISIBLE BY BOTH 5 AND 11$"
B DB   13 ,10 , " THIS IS DIVISIBLE BY BOTH 5 AND?11 $"
.CODE
MAIN PROC
    Mov AX,@Data
    Mov DS ,AX  
    
    MOV AX, 55
    MOV CX, AX
    
    MOV BL, 5
    DIV BL
    
    CMP AH, 0
    
    JNE Not_divisiable
    
    MOV AX,CX
    MOV BL ,12
    DIV BL
    CMP AH ,0  
    JNE Not_divisiable
    
    LEA DX, B
    MOV AH,9
    INT 21H
    JMP EXIT
Not_divisiable:
    LEA DX , A
    MOV AH , 9
    INT 21H
EXIT:
MOV AH, 4CH
INT 21H

    

MAIN ENDP
END MAIN
      

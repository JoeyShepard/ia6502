lda #$FE
clc
adc #1

ldx #2
jmp (table,X)
table:
.dw label1
.dw label2
label1:
lda #5
label2:
lda #7

sed
clc
lda #$67
adc #$34
cld

lda #$FF
sta 5
smb0 5
smb1 5
smb2 5
smb3 5
smb4 5
smb5 5
smb6 5
smb7 5


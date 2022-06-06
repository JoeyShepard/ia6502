lda #$FE
clc
adc #1

jmp (table)
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

lda #3
sta 5
dec 5

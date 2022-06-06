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

sec
lda #$63
sbc #$37

clc
lda #$63
sbc #$37

clc
lda #0
sbc #0

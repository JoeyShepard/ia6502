lda #5
jmp label
sec ;skipped!
label:
sbc #2
tay
jmp uninit

;Directives
.org $D000
.set foo, 5
.set bar,foo+2
.dw *

;Unknown symbols
jmp baz
.set jar,baz+5
lda jar

;Unknown mem
uninit:
lda 3
tax
adc 4

;Parentheses hilite
lda ((1+2)+(3+4))

;Errors
.set ,5
.set adc, 5
clc 5
lda (5,y)
lda #256
sta 5++2
ldz

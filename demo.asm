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
.db bar
.dw *

;Unknown symbols
jmp baz
.set jar,baz+5
lda jar

;Uninitialized mem
uninit:
lda 3
tax
adc 4

;Paren highlighting
lda ((1+2)+(3+4))

;Errors
.set ,5
.set adc, 5
sta 5++2
lda (5,y)
ldz
.org $D00E
.db 42
clc 5
lda #256
.org $FFFF
.rs 1

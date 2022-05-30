lda #3
sta 5
bbs0 5,foo
lda #5
foo:




jmp (table)
table:
.dw label1
.dw label2
label1:
lda #5
label2:
lda #7

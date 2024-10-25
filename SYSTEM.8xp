Disp "EQ 1"
Input "A:",A
Input "B:",B
Input "C:",C
Disp "EQ 2"
Input "A:",D
Input "B:",E
Input "C:",F
Listmatr({A,D},{B,E},[I])
Listmatr({C,F},[J])
([I][J])→[H]
[H](1,1)→X
[H](2,1)→Y
DelVar A
DelVar B
DelVar C
DelVar D
DelVar E
DelVar F
DelVar [H]
DelVar [I]
DelVar [J]
Disp "VALUES STORED: X, Y"
Disp "X:"
Disp XFrac
Disp "Y:"
Disp YFrac

Input "X COMP:",X
Input "Y COMP:",Y
If X>0
Then
tan(Y/X)→θ
Else
If X<0 and Y≥0
Then
tan(Y/X)+180→θ
Else
If X<0 and Y<0
Then
tan(Y/X)-180→θ
Else
If X=0 and Y>0
Then
90→θ
Else
If X=0 and Y<0
Then
-90→θ
End
End
End
End
End
√(X²+Y²)→M
Disp "MAGNITUDE, ANGLE: M, θ"
Disp toString(M)+" @ "+toString(θ)
DelVar X
DelVar Y

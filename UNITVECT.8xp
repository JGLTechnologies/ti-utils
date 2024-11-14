Input "MAGNITUDE:",M
Input "ANGLE:",θ
Mcos(θ)→I
Msin(θ)→J
Disp "VALUES STORED: [J]"
Listmatr({I,J},[J])
Disp toString(I)+"i + "+toString(J)+"j"
DelVar M
DelVar θ
DelVar I
DelVar J

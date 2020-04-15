\ Model qcp
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0.04 r + 0.01 o + 0.07 c
Subject To
 c0: r + o + c = 100
 c1: c >= 50
 c2: r >= 25
 c3: r <= 60
 qc0: 0.1 o + [ 0.001 o ^2 ] <= 0.5
 qc1: - 0.35 r + 0.04 o + [ 0.002 o ^2 ] <= 1
 qc2: 0.1 r + 0.06 o - 0.3 c + [ 0.002 r ^2 + 0.001 r * o + 0.005 o ^2
   + 0.001 c ^2 ] <= 1
Bounds
End

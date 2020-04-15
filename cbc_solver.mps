NAME          ClpDefau
ROWS
 N  OBJROW
 L  R_1_0
 L  R_1_1
 L  R_2_0
 L  R_2_1
COLUMNS
    x_0       OBJROW    1.             R_1_0     1.          
    x_0       R_1_1     1.             R_2_0     1.          
    x_1       OBJROW     -2.           R_1_0     2.          
    x_2       OBJROW    3.             R_1_1     1.          
    x_2       R_2_1     1.          
    y_0       OBJROW    2.             R_2_0     1.          
    y_1       OBJROW    2.             R_2_0     2.          
    y_1       R_2_1     1.          
RHS
    RHS       R_1_0     5.             R_1_1     2.5         
    RHS       R_2_0     4.2            R_2_1     3.          
RANGES
    RANGE     R_2_0     2.2            R_2_1     1.          
BOUNDS
 FR BOUND     x_0              1e+30
 LO BOUND     x_1       1.1         
 UP BOUND     x_1       2.          
 LO BOUND     x_2       1.1         
 UP BOUND     x_2       3.5         
ENDATA

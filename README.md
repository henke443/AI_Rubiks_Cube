# About


# AI

Decision Transformer
s a r s a r 
state action reward

random state -> random set of notation -> try notation, calculate score based on diff to 


# Short intro to notation:

```



                 ║ Top          ║
                 ┌──────────────┐
                 │ Y0 │ Y1 │ Y2 │
                 │ Y3 │ Y4 │ Y5 │
                 │ Y6 │ Y7 │ Y8 │
                 └──────────────┘
║ Left         ║ ║ Back         ║ ║ Right        ║ ║ Front        ║
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ O0 │ O1 │ O2 │ │ G0 │ G1 │ G2 │ │ R0 │ R1 │ R2 │ │ B0 │ B1 │ B2 │
│ O3 │ O4 │ O5 │ │ G3 │ G4 │ G5 │ │ R3 │ R4 │ R5 │ │ B3 │ B4 │ B5 │
│ O6 │ O7 │ O8 │ │ G6 │ G7 │ G8 │ │ R6 │ R7 │ R8 │ │ B6 │ B7 │ B8 │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                 ║ Down         ║
                 ┌──────────────┐
                 │ W0 │ W1 │ W2 │
                 │ W3 │ W4 │ W5 │
                 │ W6 │ W7 │ W8 │
                 └──────────────┘

A cubie face is for example O7, which has the sides [O7, W3], 
other examples are [G4] and [W4], or this one which has 3 sides: [B0, O2, Y6]

A cube face is for example D: [[W0, W1, W2], [W3, W4, W5], [W6, W7, W8]]

The other face of a 2 sided cubie is denoted by \*, so O7\* corresponds to W3
If the cubie is 3 faced, then the notation orientation is determined by the containing cube face, B0\*\* returns the left or right face (O2) and B0\* returns the top or bottom face (Y6) of the cubie.


y(W4)                     # cube face containing cubie face W4 (down)
W0* = B6                  # returns top or bottom adjacent cubie face to W0
W0** = O8                 # returns left or right adjacent cubie face to W0
y(07*)''                  # will perform D'
y(07*)'                   # will perform D
y(O7*)''2 = y(O7*)'2 = D2 # number after prim denotes number of repetitions
y^(x)                     # returns the opposite cube face to the cube face containing x

Just typing regular cube face rotation notation is also valid: R' D U' D2 for example
L1 ~ L2 true if L1 is adjacent to L2
x e L returns true if x is an element of cube face L, x is one cubie face
x == x1 true if x and x1 are equal, x and x1 are two cubie or cube faces
x != x1 true if x and x1 are not equal, x and x1 are two cubie or cube faces
x & x1 true if x and x1 are both true

i(x, f) if statement, perform y if x is true
i^(x, f) if not statement, perform y if x is not true
i(x, f1, f2) if else statement, perform f1 if x else f2
i^(x, f1, f2) if not else statement, perform f2 if x else f1

w(x, y) while statement, perform y while x is false
w^(x, y) while not statement, perform y while x is false

w(j, x, d, y) for statement with variable, example:
    w(j=0, j < 10, +1, y) # if j=0 is instead j, it will default to j=0
    equivalent to for(j=0; j<10; j+=1) { y }
    j can be named anything including things that would conflict with other names, if so those things will be overridden inside of this function and all functions within it. Not recommended to do the aforementioned thing though.

w(el, [W2, O2, Y2], y) for statement with array, el is an entry of the array

yH(x) returns the closest adjacent left or right (horizontal) cube face to the cubie face x.
If the left and right side are equally far apart from x, then it will return false.
Oriented by the cube face containing x.

yV(x) returns the closest adjacent top or bottom (vertical) cube face to the cubie face x.
If the top and bottom side are equally far apart from x, then it will return false.
Oriented by the cube face containing x.

yU(x) returns the top cube face, oriented by x if x is a cube face, or the cube face containing x if x is a cubie face
yD(x) ... 
yR(x) ... 
yL(x) ...

y*(x)z = i(yV(x), yV(x)z) 
         i(yH(x), yV(x)z)

y*(W3)'2 = i(yV(W3), yV(W3)'2) 
           i(yH(W3), yV(WH)'2)

Ln gets the nth item of a cube face.
Not to be confused with L'n or L''n
For example:
    y(W3*)4 == O4

c(x) gets the color of a cubie face or a cube face,
for example:
c(W3)4 = W4
c(W3*) = O7
c(W3*)4 = O4
c(0) = Y
c(1) = L


```




```






3d experimental note:
since 16 and 48 for example is the same piece, it feels like my layout has redundant information and that might make it less performant. How can I structure it in a way that retains the 3D information with as little space as possible?
Answer: Probably not, you would need to record the rotation of it anyways and 3D rotation typically requires 3 axis, 
so each block would still need 3 pieces of information sometimes, and sometimes 2
The first and last cube face would need: 4*3+4*2+1 pieces of info
The second cube face would need 8*2 so we could MAYBE get away with 37 pieces of info instead of 54, but I'm not sure...


                 ║ Top          ║
                 ┌──────────────┐
                 │ Y0 │ Y1 │ Y2 │
                 │ Y3 │ Y4 │ Y5 │
                 │ Y6 │ Y7 │ Y8 │
                 └──────────────┘
║ Left         ║ ║ Back         ║ ║ Right        ║ ║ Front        ║
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ O0 │ O1 │ O2 │ │ G0 │ G1 │ G2 │ │ R0 │ R1 │ R2 │ │ B0 │ B1 │ B2 │
│ O3 │ O4 │ O5 │ │ G3 │ G4 │ G5 │ │ R3 │ R4 │ R5 │ │ B3 │ B4 │ B5 │
│ O6 │ O7 │ O8 │ │ G6 │ G7 │ G8 │ │ R6 │ R7 │ R8 │ │ B6 │ B7 │ B8 │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                 ║ Down         ║
                 ┌──────────────┐
                 │ W0 │ W1 │ W2 │
                 │ W3 │ W4 │ W5 │
                 │ W6 │ W7 │ W8 │
                 └──────────────┘

                 ║ Top          ║
                 ┌──────────────┐
                 │ 0  │ 1  │ 2  │
                 │ 3  │ 4  │ 5  │
                 │ 6  │ 7  │ 8  │
                 └──────────────┘
║ Left         ║ ║ Back         ║ ║ Right        ║ ║ Front        ║
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 9  │ 10 │ 11 │ │ 18 │ 19 │ 20 │ │ 27 │ 28 │ 29 │ │ 36 │ 37 │ 38 │
│ 12 │ 13 │ 14 │ │ 21 │ 22 │ 23 │ │ 30 │ 31 │ 32 │ │ 39 │ 40 │ 41 │
│ 15 │ 16 │ 17 │ │ 24 │ 25 │ 26 │ │ 33 │ 34 │ 35 │ │ 42 │ 43 │ 44 │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                 ║ Down         ║
                 ┌──────────────┐
                 │ 45 │ 46 │ 47 │
                 │ 48 │ 49 │ 50 │
                 │ 51 │ 52 │ 53 │
                 └──────────────┘

```
# Section 1. (Somewhat) Formalizing CFOP 

# Motivation

# The cross

Rule notation:

A cubie face is for example O7, which has the sides [O7, W3], 
other examples are G4 or W4 which only has the sides: [G4] and [W4].
Or this one which has 3 sides: [B0, O2, Y6]

The other face(s) of a 2 sided cubie is denoted by \*, so O7\* corresponds to W3
If the cubie is 3 faced, then the notation orientation is determined by the containing cube face, B0\*\* returns the left or right face (O2) and B0\* returns the top or bottom face (Y6) of the cubie.

A containg cube face function ***y***, returns the cube face that currently contains the element passed in as an argument.
y(O7\*) will for example correspond to the DOWN cube face in an unscrambled cube.

If you put ' after a cube face then that will rotate that cube face clockwise, if you put '' it will rotate counter clockwise.
y(07\*)'' will perform D'
y(07\*)' will perform D

If you put a number after the rotation notation then it will be repeated that many times:
y(O7\*)''2 = y(O7\*)'2 = D2

Also, y(x), y(x)' and y(x)'' returns the cube face containg x as it looks after the operation. This is also true for all coming operations on cube faces.


y^(x) returns the opposite cube face to the cube face containing x

yH(x) returns the closest adjacent left or right (horizontal) cube face to the cubie face x.
If the left and right side are equally far apart from x, then it will return false.
Oriented by the cube face containing x.

yV(x) returns the closest adjacent top or bottom (vertical) cube face to the cubie face x.
If the top and bottom side are equally far apart from x, then it will return false.
Oriented by the cube face containing x.

yU(x) returns the top cube face, oriented by x if x is a layer, or the cube face containing x if x is a cubie face
yD(x) ... 
yR(x) ... 
yL(x) ...

y*(x)z = i(yV(x), yV(x)z) 
         i(yH(x), yV(x)z)

y*(W3)'2 = i(yV(W3), yV(W3)'2) 
           i(yH(W3), yV(WH)'2)

Ln gets the nth item of a cube face.
Not to be confused with L'n or L''n
For example:
    y(W4)4 == Y4

c(x) gets the color of a cubie face or a cube face,
for example:
c(W3)4 = W4
c(W3*) = O7
c(W3*)4 = O4
c(0) = Y
c(1) = L

L1 ~ L2 true if L1 is adjacent to L2
x e L returns true if x is an element of cube face L, x is one cubie face
x == x1 true if x and x1 are equal, x and x1 are two cubie or cube faces
x != x1 true if x and x1 are not equal, x and x1 are two cubie or cube faces
x & x1 true if x and x1 are both true

i(x, f) if statement, perform y if x is true
i^(x, f) if not statement, perform y if x is not true
i(x, f1, f2) if else statement, perform f1 if x else f2
i^(x, f1, f2) if not else statement, perform f2 if x else f1

w(x, y) while statement, perform y while x is false
w^(x, y) while not statement, perform y while x is false

w(j, x, d, y) for statement with variable, example:
    w(j=0, j < 10, +1, y) # if j=0 is instead j, it will default to j=0
    equivalent to for(j=0; j<10; j+=1) { y }
    j can be named anything including things that would conflict with other names, if so those things will be overridden inside of this function and all functions within it. Not recommended to do the aforementioned thing though.

w(el, [W2, O2, Y2], y) for statement with array, el is an entry of the array

1. Fix orange white center piece [W3, O7]
```


    
    # For each W1, W3, W5, W7, return the current cubie face as J
    w(J, [W1, W3, W5, W7],
        
        # While the J cubie face is 
        #     1. not contained within the cube face that contains the white center piece
        # and 2. the centerpiece of the layer the other cubie face is in does not match the other cubie faces color

        w^(J e y(W4) & y(J*)4 = c(J*)4, 
            i(
                # If the face is in the opposite cube face to the white middle piece
                J e y^(W4),

                # While other cubie face on the cubie (O7 if J is W3), is not aligned to the other cubie face's color (O if J is W3)
                w(y(J*)4 != c(J*)4,
                    y(J)' # Turn cube face containing J
                )
                
                # Turn adjacent cube face to J twice
                y(J*)'2
                
            , # Else, if the face is in an adjacent cube face

                # If the orange face is in the orange (middle piece) cube face
                i(J* e y( c(J*)4 ),
                    # If the white face is in the face that's adjacent to the left of the white middle piece's face
                    i(J e yL(W4),
                        y(J*)''
                    )
                    i(J e yR(W4),
                        y(J*)'
                    )

                # Else if the orange face is not in the orange (middle piece) cube face
                ,
                    
                    # If the other color of the cubie is in the opposite cube face to the white middle piece
                    i(J* e y^(W4),
                        # Turn the top cube face until the white orange piece is aligned with orange middle
                        w(y(J)4 != c(J*)4,
                            y(J*)'
                        )
                        # Move the orange cube face 90 deg
                        y(J)'
                    )

                    # If the other color of the cubie is in the adjacent to the left of the white middle pieces cube face
                    i(J* e yL(W4),
                        y(J*)' 
                    )

                    # If the other color of the cubie is in the adjacent to the right of the white middle pieces cube face
                    i(J* e yR(W4),
                        y(J*)''
                    )
                )

            )
        )
    )

    Or shorter:
        w(J,[W1,W3,W5,W7],w^(Jey(W4)&y(J*)4=c(J*)4,i(Jey^(W4),w(y(J*)4!=c(J*)4,y(J)')y(J*)'2,i(J*ey(c(J*)4),i(JeyL(W4),y(J*)'')i(JeyR(W4),y(J*)'),i(J*ey^(W4),w(y(J)4!=c(J*)4,y(J*)')y(J)')i(J*eyL(W4),y(J*)')i(J*eyR(W4),y(J*)'')))))
    Even shorter:
        wJ,[W1,W3,W5,W7],w^JeyW4&yJ*4=cJ*4,iJey^W4,wyJ*4!=cJ*4,yJ'yJ*'2,iJ*eycJ*4,iJeyLW4,yJ*''iJeyRW4,yJ*',iJ*ey^W4,wyJ4!=cJ*4,yJ*'yJ'iJ*eyLW4,yJ*'iJ*eyRW4,yJ*''

```
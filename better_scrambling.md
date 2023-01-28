Better scrambling by instead of using random moves figure out the rules for how things are put so that the cube is solveable:

https://www.quora.com/Is-it-possible-to-determine-whether-a-Rubiks-Cube-is-solvable-just-by-looking-at-its-scrambled-state

Yes.

There are three conditions necessary for a cube to be solvable:

The edges must have an even number of them “flipped”
The total twist of the corners must be a whole number (where twisting a corner 1/3 clockwise is 1/3 of a twist, and so on).
The parity of the permutation of the edges is the same as the parity of the permutation of the corners.
To determine the total twist of the corners, pick two opposite faces (like Up and Down), and examine each corner, recording the twist necessary to get all the up and down colors on the up and down faces (it doesn’t matter if twisting a corner would result in a up color on the down face, or vice versa). If the total twist is not a whole number, such as “twist these two corners 1/3 clockwise”, then the cube is not solvable.

To determine the total flip state, look at the edge colors on the top and down faces, as well as the edge colors on the front and back faces of the middle slice. Count how many are “right” — a top color on the bottom face, a front color on the top face, a back color on the back face (in those two spots), etc, compared to how many are “wrong” — a left color on the front face (in those two spots), a right color on top, etc. If there are an odd number “wrong” (or “right”), then the cube is not solvable.

There are 8 corner pieces. Pick one, and track the cycle it goes in: the one in the up-right-front spot belongs in the down-right-front spot, which should be in the down-left-back spot, which should be in the up-right-front spot. Write down the cycle like (urf,drf,dlb). Do that again for another corner not tracked, until all corners are tracked. You’ll get a cycle pattern like (urf,drf,dlb)(ulf,ulb)(ubf,dlf)(drb). Count the number of cycles of even length (in this case, 2).

There are 12 edge pieces. Do the same task with them as you did with the corner pieces: pick one, track its cycle, write it down, repeat for all twelve. You’ll get a cycle pattern like (uf,df,rf)(lf,ul,ur,br,bl)(ub,db)(dl,dr). Count the number of cycles of even length (in this case, 2)

If one of those two even-length-cycle counts is even and the other is odd, then the cube is not solvable.

None of these actions require making even one turn.

Of course, partially solving it can make it easier to do these counts. If you’ve solved two layers, for instance, it’s easy to see if there’s a flip or twist problem, and looking at the permutations is easier. But you don’t have to do so.


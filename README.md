# Dots, Boxes, and Shapes
## A strategic variation of Dots and Boxes
### Members: Veera Toram and Tali Zacks

For our version of the game Dots and Boxes, we will make an irregular grid pattern that has a multiplicity of repeating 
and non-repeating shapes with varying points {based on the size of the shape captured. Another unique aspect of this 
game would be that if a player captured the majority of a repeating shape they win all the equivalent shapes.

We are open to evaluating and testing various algorithms based on the final size of the puzzle, but we do think a 
minimax-based algorithm and alpha-beta pruning and/or localized gameplays based on the unique shape would be a good fit.
We intend to utilize the features of Network X for this project.

## References: 
<ul>
  <li>Traditional Dots and Boxes: https://gametable.org/games/dots-and-boxes/</li>
  <li>A project dealing with a traditional Dots and Boxes game: https://github.com/Armando8766/Dots-and-Boxes.git</li>
  <li>Pattern theory: https://www.youtube.com/watch?v=48sCx-wBs34</li>
</ul>

## Two Variations:
### [recommended] Only one chance per player:
This more improved version restricts players to one chance per turn even if you win a box. This variation allows players
to play in a more strategic give-and-take fashion.
To play this final version run main_alternative games.py

### Get another chance on winning:
The first version of this game is built to give you another chance everytime you capture a box, this however means that
the game will collapse rapidly after all no-win moves are played. 
To test this version play main.py.

## RULES OF THE GAME
Number of players = 2
### Instructions
1. You will first be asked if you want to play against the computer. If you do, type: C. Otherwise, type: H
2. If you typed 'C', continue to Human vs Computer section. If you typed 'H', continue to Human vs Human section.
-----
#### Human vs Computer:
3. When prompted, input the difficulty level of the computer opponent you wish to play against.
   - For easy, type: 0
   - For medium, type: 1
   - For hard, type: 2
---
#### Human vs Human:
3. You will take turns back and forth between players entering your desired edges.
---
4. Type the edge number (as seen in the figure) that you wish to play for your turn.
5. Depending on your opponent (computer or human) either wait for the computer to make its move 
or prompt your opponent to play, respectively.
6. If a player completes a box, they receive an additional turn.

### Goal
The winning player is that which has the most points. Points are awarded for completing a box.
To win a box, you must play the 4th edge of a box during your turn. Box values are not uniform. The awarded points are 
based on the shape within the box and are as follows:
- Circle = 5 points
- Triangle = 3 points
- Square = 2 points

If a player captures the majority of boxes containing a certain shape, they automatically retain all of the
boxes containing that shape. This includes the boxes which have already been won by the opponent. 
Here is an example:
- There are 5 total circles on the board.
- Blue has 2 circle boxes and 1 triangle box.
- Red has 2 circle boxes and 3 square boxes.
- The score is currently: 
  - Blue: 13
  - Red: 16
- Blue completes a box around another circle.
- Blue now has 5 circle boxes and 1 triangle box.
- Red now has 3 square boxes.
- The score is now:
  - Blue: 28
  - Red: 6

#### Targeted Algorithm Analysis: heuristic function evaluation
Our Heuristic evaluation function plays a list of moves whose length is constant for a given difficulty level. Thus
the time complexity is also constant for any given difficulty level. The increase in time complexity for increasing
complexity level is linearly proportional.
Profiler efficiency: 
complexity level is linearly proportional.

Easy

3: ~5.6 milliseconds per call count

4: ~4.3 milliseconds per call count [MacOS]

5: ~6.5  milliseconds per call count [MacOS]

6: ~18  milliseconds per call count


Medium

3: ~ 5.3 milliseconds per call count

4: ~ 4.5 milliseconds per call count [MacOS]

5: ~ 6.4 milliseconds per call count [MacOS]

6: ~ 13.3  milliseconds per call count

Hard

3: ~ 5.4 milliseconds per call count

4: ~ 4.5 milliseconds per call count [MacOS]

5: ~ 6.4 milliseconds per call count [MacOS]

6: ~ 14.8  milliseconds per call count


#### Targeted Algorithm Analysis: Legal Moves identification function
The time complexity of the legal moves identification function is proportional to the square of the size of the grid's side.
i.e., O(n^2), where n is the length of grid's side. 

3x3: 
- Easy  : 0.20 milliseconds per call count
- Medium: 0.20 milliseconds per call count
- Hard  : 0.19 milliseconds per call count

4x4:
- Easy  : 0.18 milliseconds per call count [MacOS]
- Medium: 0.18 milliseconds per call count [MacOS]
- Hard  : 0.17 milliseconds per call count [MacOS]

5x5:
- Easy  : 0.26 milliseconds per call count [MacOS]
- Medium: 0.27 milliseconds per call count [MacOS]
- Hard  : 0.25 milliseconds per call count [MacOS]

6x6:
- Easy  : 0.72 milliseconds per call count 
- Medium: 0.52 milliseconds per call count
- Medium: 0.53 milliseconds per call count

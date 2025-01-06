(define (problem doors-keys-gems-problem)
  (:domain doors-keys-gems)
  (:objects door1 door2 door3 - door
            key1 key2 - key
            gem1 gem2 gem3 gem4 - gem
            red yellow blue green - color
            robot - robot
            human - human)
  (:init (= (walls) (new-bit-matrix false 7 9))
         (= (xloc gem1) 1)
         (= (yloc gem1) 1)
         (= (walls) (set-index walls true 1 3))
         (= (walls) (set-index walls true 1 4))
         (= (walls) (set-index walls true 1 5))
         (= (walls) (set-index walls true 1 6))
         (= (walls) (set-index walls true 1 7))
         (= (walls) (set-index walls true 1 8))
         (= (walls) (set-index walls true 1 9))
         (= (xloc key1) 1)
         (= (yloc key1) 2)
         (iscolor key1 red)
         (= (xloc key2) 2)
         (= (yloc key2) 2)
         (iscolor key2 blue)
         (= (walls) (set-index walls true 2 3))
         (= (walls) (set-index walls true 2 4))
         (= (walls) (set-index walls true 2 5))
         (= (walls) (set-index walls true 2 6))
         (= (walls) (set-index walls true 2 7))
         (= (walls) (set-index walls true 2 8))
         (= (walls) (set-index walls true 2 9))
         (= (xloc gem2) 9)
         (= (yloc gem2) 3)
         (= (xloc door1) 1)
         (= (yloc door1) 4)
         (iscolor door1 red)
         (locked door1)
         (= (walls) (set-index walls true 4 2))
         (= (walls) (set-index walls true 4 3))
         (= (walls) (set-index walls true 4 4))
         (= (walls) (set-index walls true 4 5))
         (= (xloc door2) 6)
         (= (yloc door2) 4)
         (iscolor door2 blue)
         (locked door2)
         (= (walls) (set-index walls true 4 7))
         (= (walls) (set-index walls true 4 8))
         (= (xloc door3) 9)
         (= (yloc door3) 5)
         (iscolor door3 red)
         (locked door3)
         (= (walls) (set-index walls true 6 1))
         (= (walls) (set-index walls true 6 3))
         (= (walls) (set-index walls true 6 4))
         (= (walls) (set-index walls true 6 6))
         (= (walls) (set-index walls true 6 7))
         (= (walls) (set-index walls true 6 8))
         (= (walls) (set-index walls true 7 1))
         (= (xloc gem3) 2)
         (= (yloc gem3) 7)
         (= (walls) (set-index walls true 7 3))
         (= (walls) (set-index walls true 7 4))
         (= (walls) (set-index walls true 7 6))
         (= (walls) (set-index walls true 7 7))
         (= (walls) (set-index walls true 7 8))
         (= (xloc gem4) 9)
         (= (yloc gem4) 7)
         (= (xloc human) 5)
         (= (yloc human) 7)
         (= (xloc robot) 3)
         (= (yloc robot) 3)
         (iscolor gem1 red)
         (iscolor gem2 yellow)
         (iscolor gem3 blue)
         (iscolor gem4 green)
         (active human)
         (next-turn human robot)
         (next-turn robot human)
         (forbidden robot gem1)
         (forbidden robot gem2)
         (forbidden robot gem3)
         (forbidden robot gem4))
  (:goal (has human gem4))
)
import numpy as np
import random

#colours:
    #0 -> white
    #1 -> yellow
    #2 -> green
    #3 -> blue
    #4 -> orange
    #5 -> red

class Cube:
    def __init__(self):
        self.state = np.array([
            [0,0,0,0],  #bottom
            [1,1,1,1],  #top
            [2,2,2,2],  #front
            [3,3,3,3],  #back
            [4,4,4,4],  #right
            [5,5,5,5]   #left
        ])
        #[bottom_left, bottom_right, top_right, top_left]
    
    def print_cube(self):
        print("Bottom:", self.state[0])
        print("Top:", self.state[1])
        print("Front:", self.state[2])
        print("Back:", self.state[3])
        print("Right:", self.state[4])
        print("Left", self.state[5])
        print("\n\n")
    
    def display_flat(self):
        color_map = {0: 'W', 1: 'Y', 2: 'G', 3: 'B', 4: 'O', 5: 'R'}
        
        top = self.state[1]
        bottom = self.state[0]
        front = self.state[2]
        back = self.state[3]
        right = self.state[4]
        left = self.state[5]
        
        # Display in cross pattern
        print("        ", color_map[top[3]], color_map[top[2]])
        print("        ", color_map[top[0]], color_map[top[1]])
        print()
        print(color_map[left[3]], color_map[left[2]], " ", 
              color_map[front[3]], color_map[front[2]], " ",
              color_map[right[3]], color_map[right[2]], " ",
              color_map[back[3]], color_map[back[2]])
        print(color_map[left[0]], color_map[left[1]], " ", 
              color_map[front[0]], color_map[front[1]], " ",
              color_map[right[0]], color_map[right[1]], " ",
              color_map[back[0]], color_map[back[1]])
        print()
        print("        ", color_map[bottom[3]], color_map[bottom[2]])
        print("        ", color_map[bottom[0]], color_map[bottom[1]])
        print("\n")
    
    def U(self):
        #top face rotate clockwise
        temp = self.state[1][0]
        for i in range(3):
            self.state[1][i] = self.state[1][i+1]
        self.state[1][3] = temp

        temp2 = self.state[2][2]
        temp3 = self.state[2][3]

        #front
        self.state[2][2] = self.state[4][2]
        self.state[2][3] = self.state[4][3]

        #right
        self.state[4][2] = self.state[3][2]
        self.state[4][3] = self.state[3][3]

        #back
        self.state[3][2] = self.state[5][2]
        self.state[3][3] = self.state[5][3]

        #left
        self.state[5][2] = temp2
        self.state[5][3] = temp3

    def U_prime(self):
        for i in range(3):
            self.U()

    def U2(self):
        for i in range(2):
            self.U()

    def D(self):
        #bottom face rotate clockwise
        temp = self.state[0][0]
        for i in range(3):
            self.state[0][i] = self.state[0][i+1]
        self.state[0][3] = temp

        temp2 = self.state[2][0]
        temp3 = self.state[2][1]

        #front
        self.state[2][0] = self.state[4][0]
        self.state[2][1] = self.state[4][1]

        #right
        self.state[4][0] = self.state[3][0]
        self.state[4][1] = self.state[3][1]

        #back
        self.state[3][0] = self.state[5][0]
        self.state[3][1] = self.state[5][1]

        #left
        self.state[5][0] = temp2
        self.state[5][1] = temp3

    def D_prime(self):
        for i in range(3):
            self.D()

    def D2(self):
        for i in range(2):
            self.D()
    
    def F(self):
        #front face rotate clockwise
        temp = self.state[2][0]
        for i in range(3):
            self.state[2][i] = self.state[2][i+1]
        self.state[2][3] = temp

        temp2 = self.state[1][0]
        temp3 = self.state[1][1]

        #top
        self.state[1][0] = self.state[5][1]
        self.state[1][1] = self.state[5][2]

        #left
        self.state[5][1] = self.state[0][2]
        self.state[5][2] = self.state[0][3]

        #bottom
        self.state[0][2] = self.state[4][3]
        self.state[0][3] = self.state[4][0]

        #left
        self.state[4][3] = temp2
        self.state[4][0] = temp3
    
    def F_prime(self):
        for i in range(3):
            self.F()
    
    def F2(self):
        for i in range(2):
            self.F()

    def B(self):
        #back face rotate clockwise
        temp = self.state[3][0]
        for i in range(3):
            self.state[3][i] = self.state[3][i+1]
        self.state[3][3] = temp

        temp2 = self.state[1][2]
        temp3 = self.state[1][3]

        #top
        self.state[1][2] = self.state[4][1]
        self.state[1][3] = self.state[4][2]

        #right
        self.state[4][1] = self.state[0][0]
        self.state[4][2] = self.state[0][1]

        #bottom
        self.state[0][0] = self.state[5][3]
        self.state[0][1] = self.state[5][0]

        #left
        self.state[5][3] = temp2
        self.state[5][0] = temp3

    def B_prime(self):
        for i in range(3):
            self.B()
    
    def B2(self):
        for i in range(2):
            self.B()

    def R(self):
        #right face rotate clockwise
        temp = self.state[4][0]
        for i in range(3):
            self.state[4][i] = self.state[4][i+1]
        self.state[4][3] = temp

        temp2 = self.state[1][1]
        temp3 = self.state[1][2]

        #top
        self.state[1][1] = self.state[2][1]
        self.state[1][2] = self.state[2][2]

        #front
        self.state[2][1] = self.state[0][1]
        self.state[2][2] = self.state[0][2]

        #bottom
        self.state[0][1] = self.state[3][3]
        self.state[0][2] = self.state[3][0]

        #left
        self.state[3][3] = temp2
        self.state[3][0] = temp3
    
    def R_prime(self):
        for i in range(3):
            self.R()
    
    def R2(self):
        for i in range(2):
            self.R()

    def L(self):
        #left face rotate clockwise
        temp = self.state[5][0]
        for i in range(3):
            self.state[5][i] = self.state[5][i+1]
        self.state[5][3] = temp

        temp2 = self.state[1][3]
        temp3 = self.state[1][0]

        #top
        self.state[1][3] = self.state[3][1]
        self.state[1][0] = self.state[3][2]

        #back
        self.state[3][1] = self.state[0][3]
        self.state[3][2] = self.state[0][0]

        #bottom
        self.state[0][3] = self.state[2][3]
        self.state[0][0] = self.state[2][0]

        #front
        self.state[2][3] = temp2
        self.state[2][0] = temp3

    def L_prime(self):
        for i in range(3):
            self.L()

    def L2(self):
        for i in range(2):
            self.L()
    
    def turn(self, move):
        match move:
            case "U":
                self.U()
            case "U\'":
                self.U_prime()
            case "U2":
                self.U2()
            case "D":
                self.D()
            case "D\'":
                self.D_prime()
            case "D2":
                self.D2()
            case "F":
                self.F()
            case "F\'":
                self.F_prime()
            case "F2":
                self.F2()
            case "B":
                self.B()
            case "B\'":
                self.B_prime()
            case "B2":
                self.B2()
            case "R":
                self.R()
            case "R\'":
                self.R_prime()
            case "R2":
                self.R2()
            case "L":
                self.L()
            case "L\'":
                self.L_prime()
            case "L2":
                self.L2()

    def reset(self):
        self.state = np.array([
            [0,0,0,0],  #bottom
            [1,1,1,1],  #top
            [2,2,2,2],  #front
            [3,3,3,3],  #back
            [4,4,4,4],  #right
            [5,5,5,5]   #left
        ])
        
        last = None
        moves = ["R", "U", "F"]
        modifiers = ["", "\'", "2"]

        print("Scramble:\n")
        for i in range(10):
            move = moves[random.randint(0, 2)]

            while(last == move):
                move = moves[random.randint(0, 2)]

            last = move

            modifier = modifiers[random.randint(0, 2)]
            move = move + modifier
            print(move)
            self.turn(move)
        
        print()

    def scramble_n_moves(self, n):
        self.state = np.array([
            [0,0,0,0],  #bottom
            [1,1,1,1],  #top
            [2,2,2,2],  #front
            [3,3,3,3],  #back
            [4,4,4,4],  #right
            [5,5,5,5]   #left
        ])
        
        last = None
        moves = ["R", "U", "F"]
        modifiers = ["", "\'", "2"]

        print("Scramble:\n")
        for i in range(n):
            move = moves[random.randint(0, 2)]

            while(last == move):
                move = moves[random.randint(0, 2)]

            last = move

            modifier = modifiers[random.randint(0, 2)]
            move = move + modifier
            print(move)
            self.turn(move)
        
        print()

    def is_solved(self):
        for i in range(6):
            face = self.state[i]
            if not np.all(face == face[0]):
                return False
        return True
    
    def get_action_space(self):
        """
        Returns list of all possible moves for the 2x2 Rubik's cube.
        Moves occur in the following order in the action array:
        0 -> U,   1 -> U',  2 -> U2
        3 -> D,   4 -> D',  5 -> D2
        6 -> F,   7 -> F',  8 -> F2
        9 -> B,  10 -> B', 11 -> B2
        12 -> R, 13 -> R', 14 -> R2
        15 -> L, 16 -> L', 17 -> L2
        """
        return ["U", "U'", "U2", 
                "D", "D'", "D2", 
                "F", "F'", "F2", 
                "B", "B'", "B2", 
                "R", "R'", "R2", 
                "L", "L'", "L2"]
    
    def action_to_move(self, action_idx):
        """Convert action index (0-17) to move string"""
        action_space = self.get_action_space()
        if 0 <= action_idx < len(action_space):
            return action_space[action_idx]
        return None
    
    def move_to_action(self, move_str):
        """Convert move string to action index (0-17)"""
        action_space = self.get_action_space()
        try:
            return action_space.index(move_str)
        except ValueError:
            return None
    
    
#main program
if __name__ == "__main__":
    cube = Cube()
    cube.display_flat()

    cube.reset()

    while(True):
        move = input("Input your next move: ")

        if(move == "X"):
            break
        elif(move == "S"):
            cube.reset()
        elif(move == "C"):
            print(cube.is_solved)

        else:
            cube.turn(move)

        cube.display_flat()
"""
State is represnetated as (𝑟𝑜𝑤,𝑐𝑜𝑙,𝑓𝑜𝑟𝑤,ℎ𝑒𝑎𝑙𝑡ℎ,𝑚𝑠𝑡𝑒𝑝,𝑓1,𝑓2,…,𝑓𝐾)

row, col is for agent location
forw represents agent orientation ('north', 'south' etc)
health is hp
mstep is the monster timestep for their positions to be tracked (1, 2, 3, 4)
f1, f2, fk is a boolean for each food item to show if it has been collected

"""


class FoodCollectorProblem():
    def __init__(self, initial_agent_info, N, food_chords, monster_chords):
        self.initial_agent_info = initial_agent_info # row, col, forw, hp
        self.N = N #size of grid N X N grid
        self.food_chords = food_chords #list of food chords
        self.monster_chords = monster_chords #list of monster chords
        self.mstep = 0
        self.food_bools = (False,) * len(food_chords)

        self.initial_state = self.initial_agent_info + (self.mstep, ) + self.food_bools 
        self.state = self.initial_state
    
    def move_monsters(self, timestep):
        monster_chords = list(self.monster_chords)

        if (timestep == 0):
            # monsters move to the right if possible
            for monster_chord in monster_chords:
                monster_chord = (monster_chord[0], min(monster_chord[1] + 1, self.N - 1))

        elif (timestep == 1):
            for monster_chord in monster_chords:
                monster_chord = (monster_chord[1], min(monster_chord[0] + 1, self.N - 1))
        
        elif (timestep == 2):
            for monster_chord in monster_chords:
                monster_chord = (monster_chords[0], max(monster_chord[1] - 1, 0))
        elif (timestep == 3):
            for monster_chord in monster_chords:
                monster_chord[0] = (monster_chords[1], max(monster_chord[0] - 1, 0))
        
        return tuple(monster_chords)

    def actions(self, state):
        actions = ['move-forward', 'turn-left', 'turn-right', 'collect', 'stay']

        row = state[0]
        col = state[1]
        forw = state[2]
        hp = state[3]

        if hp <= 0:
            return []
        
        if (forw == 'north' and row <= 0):
            actions.remove('move-forward')
            return actions

        elif (forw == 'east' and col >= self.N - 1):
            actions.remove('move-forward')
            return actions
        
        elif (forw == 'south' and row >= self.N - 1):
            actions.remove('move-forward')
            return actions

        elif (forw == 'west' and col <= 0):
            actions.remove('move-forward')
            return actions
        
        else:
            return actions
        
    def result(self, state, action):

        row = state[0]
        col = state[1]
        direction = state[2]
        hp = state[3]
        mstep = state[4] + 1
        food_bools = list(state[5:])
        print(food_bools)

        new_monster_cords = self.move_monsters(mstep)

        if action == 'move-forward':
            if direction == 'north':
                row -= 1
            
            elif direction == 'east':
                col += 1

            elif direction == 'south':
                row += 1
            
            elif direction == 'west':
                col -= 1

        elif action == 'turn-left':
            if direction == 'north':
                direction = 'west'
            
            elif direction == 'east':
                direction = 'north'
            
            elif direction == 'south':
                direction = 'east'
            
            elif direction == 'west':
                direction = 'south'
        
        elif action == 'turn-right':
            if direction == 'north':
                direction = 'east'
            
            elif direction == 'east':
                direction = 'south'
            
            elif direction == 'south':
                direction = 'west'
            
            elif direction == 'west':
                direction = 'north'
        
        elif action == 'collect':
            for food_index in range(len(food_bools)):
                if row == self.food_chords[food_index][0] and col == self.food_chords[food_index][1]:
                    food_bools[food_index] = True

        for monster_cord in new_monster_cords:
            if monster_cord[0] == row and monster_cord[1] == col:
                hp -= 1

        return (row, col, direction, hp, mstep) + tuple(food_bools)
    

    def action_cost(self, state1, action, state2):
        return 1    
    
    def is_goal(self, state):
        food_bools = state[5:]
        hp = state[3]

        for food_bool in food_bools:
            if not food_bool:
                return False
        
        if hp <= 0:
            return False

        return True

    def h(self, node):
        print(node)
        
def main():

    prob = FoodCollectorProblem(
        initial_agent_info=(1,1,'north', 3),
        N = 5,
        food_chords=[(1,1), (2,2)],
        monster_chords=[(2,2)]
        )

    print(prob.initial_state)
    print(prob.monster_chords)
    print(prob.food_chords)
    print(prob.food_bools)
    print(prob.result(prob.initial_state, 'collect')[5:])

if __name__ == "__main__":
    main()
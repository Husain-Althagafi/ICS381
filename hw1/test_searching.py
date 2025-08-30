from search_problem import *
from search_algorithms import *
from collections import Counter

"""
    We will use cProfile to get some function call stats. 
    Particularly, we want to count the number of times a node is popped from frontier and is generated. 
    To count the number of times a node is popped, we just need to count number of times pop() is called.
    To count number of times a node is generated, notice that we call p.result.
    So, we just need to count number of times result is called for a Problem object.
"""
import cProfile, pstats, io
from pstats import SortKey   
def run_profiler_searches(problem, searchers_list, searcher_names_list):
    problem_name = str(problem)[:28]
    total_gen_node, total_pop_node = 0, 0
    print('\nProfiler for problem: {}\n'.format(problem_name))
    for search_algo, search_algo_name in zip(searchers_list, searcher_names_list):
        pr = cProfile.Profile()
        pr.enable()
        goal_node = search_algo(problem)
        pr.disable()
        
        io_stream = io.StringIO()
        ps = pstats.Stats(pr, stream=io_stream).sort_stats(SortKey.CALLS).strip_dirs()
        ps.print_stats("pop*|result*")
        profiler_string = io_stream.getvalue()
        
        gen_node_count, pop_node_count = profiler_splitter(profiler_string)
        total_gen_node += gen_node_count
        total_pop_node += pop_node_count
        
    
        print('{:15s} {:9,d} generated nodes |{:9,d} popped |{:5.0f} solution cost |{:8,d} solution depth|'.format(
              search_algo_name, gen_node_count, pop_node_count, goal_node.path_cost, goal_node.depth))
    
    
    print('{:15s} {:9,d} generated nodes |{:9,d} popped'.format('TOTAL', total_gen_node, total_pop_node))
    print('________________________________________________________________________')

def profiler_splitter(profiler_data):
    profiler_data = profiler_data.split("\n")
    result_line = [l for l in profiler_data if 'result' in l][1]
    pop_line = [l for l in profiler_data if 'pop' in l][1]
    
    splitter = (lambda s: int(s.split()[0].split("/")[0]) )
    result_calls = splitter(result_line)
    pop_calls = splitter(pop_line)
    
    return result_calls, pop_calls 
    
if __name__ == "__main__":
    # be sure to clip monster locations to not go out of bounds.
    # you can clip using max and min
    clipped_monsters_example = FoodCollectorProblem(initial_agent_info=(0, 4, 'west', 10),
                                                    N=5, food_coords=[(1,1), (1,4)],
                                                    monster_coords=[(2,2), (4,4), (0,4), (4,2)])
    example_state = (4, 2, 'north', 11, 2, False, False)
    print(f'For FoodCollectorProblem. With N=5, and monster_coords=[(2,2), (4,4), (0,4), (4,2)].')
    print(f'Monsters at mstep=0, is {clipped_monsters_example.move_monsters(0)}')
    print(f'Monsters at mstep=1, is {clipped_monsters_example.move_monsters(1)}')
    print(f'Monsters at mstep=2, is {clipped_monsters_example.move_monsters(2)}')
    print(f'Monsters at mstep=3, is {clipped_monsters_example.move_monsters(3)}')
    print('________________________________________________________________________')
    
    example_fhproblem = FoodCollectorProblem(initial_agent_info=(0, 4, 'west', 10),
                                             N=5, food_coords=[(1,1), (1,4)],
                                             monster_coords=[(0,1), (2,2)] )
    
    example_state = (4, 4, 'north', 10, 0, True, True)
    print(f'For FoodCollectorProblem. From state: {example_state}. we have the following actions available:')
    actions_available = example_fhproblem.actions(state=example_state)
    print(actions_available)
    print("All actions should be available")
    print('________________________________________________________________________')
    
    example_state = (4, 4, 'south', 10, 0, True, True)
    print(f'For FoodCollectorProblem. From state: {example_state}. we have the following actions available:')
    actions_available = example_fhproblem.actions(state=example_state)
    print(actions_available)
    print("move-forward should be removed.")
    print('________________________________________________________________________')
    
    example_state = (3, 3, 'south', 0, 0, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. we have the following actions available:')
    actions_available = example_fhproblem.actions(state=example_state)
    print(actions_available)
    print("No actions should be available.")
    print('________________________________________________________________________')
    
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"move-forward"}')
    next_state = example_fhproblem.result(state=example_state, action='move-forward')
    print(next_state)
    print("agent location should be updated to (4, 3).")
    print('________________________________________________________________________')
    
    example_state = (1, 4, 'west', 10, 3, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"collect"}')
    next_state = example_fhproblem.result(state=example_state, action='collect')
    print(next_state)
    print("agent should have collected food item at (1,4). So second boolean should be True.")
    print('________________________________________________________________________')
    
    example_state = (1, 1, 'south', 10, 2, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"collect"}')
    next_state = example_fhproblem.result(state=example_state, action='collect')
    print(next_state)
    print("agent should have collected food item at (1, 1). So first boolean should be True.")
    print("also agent contacts monster and takes damage, so health is 9.")
    print('________________________________________________________________________')
    
    example_state = (4, 0, 'east', 10, 0, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"turn-left"}')
    next_state = example_fhproblem.result(state=example_state, action='turn-left')
    print(next_state)
    print("agent turned left, orientation should now be north.")
    next_state = example_fhproblem.result(state=example_state, action='turn-right')
    print(next_state)
    print("agent turned right, orientation should now be south.")
    print('________________________________________________________________________')
    
    example_state = (0, 3, 'west', 8, 0, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"move-forward"}')
    next_state = example_fhproblem.result(state=example_state, action='move-forward')
    print(next_state)
    print("agent walked into location with monster. health should be 7.")
    example_state = (1, 3, 'west', 33, 1, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"move-forward"}')
    next_state = example_fhproblem.result(state=example_state, action='move-forward')
    print(next_state)
    print("agent walked into location with monster. health should be 32.")
    example_state = (4, 2, 'north', 11, 2, False, False)
    print(f'For FoodCollectorProblem. From state: {example_state}. Taking action: {"move-forward"}')
    next_state = example_fhproblem.result(state=example_state, action='move-forward')
    print(next_state)
    print("agent walked into location with monster. health should be 10.")
    print('________________________________________________________________________')
    
    # add your own problems and try printing report. 
    example_fhproblem = FoodCollectorProblem(initial_agent_info=(0, 4, 'west', 10),
                                             N=5, food_coords=[(1,1), (1,4)],
                                             monster_coords=[(0,1), (2,2)] )
    goal_node = uniform_cost_search(example_fhproblem)
    print('printing solution path')
    print(get_path_states(goal_node))
    print('printing solution-actions-path')
    print(get_path_actions(goal_node))
    print('________________________________________________________________________')
    print('________________________________________________________________________')
    
    ######## #######
    
    # get some statistics on generated nodes, popped nodes, solution
    searchers = [(lambda p: breadth_first_search(p, treelike=False)), 
                 (lambda p: uniform_cost_search(p, treelike=False)),  
                 (lambda p: astar_search(p, h=p.h, treelike=False))]
    searcher_names= ['Graph-like BFS',  
                     'Graph-like UCS', 
                     'Graph-like A*']
    run_profiler_searches(example_fhproblem, searchers, searcher_names)

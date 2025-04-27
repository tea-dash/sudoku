from sudoku.grid import SudokuGrid
import random
import time

def solve(grid: SudokuGrid, record_steps=False) -> bool:
    """
    Solve the Sudoku puzzle using backtracking.
    Returns True if a solution is found, False otherwise.
    The grid is modified in place.
    
    If record_steps is True, returns (success, steps) where steps is a list of
    board states and positions filled during solving.
    """
    steps = [] if record_steps else None
    solution_path = [] if record_steps else None
    
    # Helper function to capture solving process
    def solve_with_steps(grid, current_path=None):
        if current_path is None and record_steps:
            current_path = []
            
        # Find next empty cell with the minimum number of possible values
        best = None  # (r, c, possible_values)
        for r in range(9):
            for c in range(9):
                if grid.board[r][c] == 0:
                    candidates = [v for v in range(1, 10) if grid.is_valid(r, c, v)]
                    if not candidates:
                        return False  # Dead end, no valid value for this cell
                    if best is None or len(candidates) < len(best[2]):
                        best = (r, c, candidates)
        
        # If no empty cell found, puzzle is solved
        if best is None:
            if record_steps and current_path:
                # We've found a solution, save the path
                solution_path.extend(current_path)
            return True
        
        # Try each candidate value
        r, c, candidates = best
        # Shuffle the candidates for randomization
        random.shuffle(candidates)
        for val in candidates:
            grid.place(r, c, val)
            
            # Create a step record but don't save it yet - only if it leads to a solution
            if record_steps:
                board_copy = [row[:] for row in grid.board]
                step = {
                    'board': board_copy,
                    'position': (r, c),
                    'value': val
                }
                current_path.append(step)
                
            if solve_with_steps(grid, current_path):
                return True
                
            # Backtrack if solution not found
            grid.remove(r, c, val)
            
            # Remove this step from the current path if it didn't lead to a solution
            if record_steps and current_path:
                current_path.pop()
        
        return False
    
    # Call the helper function
    result = solve_with_steps(grid)
    
    # Return appropriate result based on whether steps were requested
    if record_steps:
        # Now we have only the steps that led to the solution
        return result, solution_path
    else:
        return result

def count_solutions(grid: SudokuGrid, limit=2) -> int:
    """
    Count the number of solutions up to a limit.
    Used to check if a puzzle has a unique solution.
    """
    # Create a copy of the grid to avoid modifying the original
    copy_grid = grid.copy()
    solutions = [0]  # Use a list so we can modify from inner function
    
    def backtrack():
        # Find an empty cell
        for r in range(9):
            for c in range(9):
                if copy_grid.board[r][c] == 0:
                    candidates = [v for v in range(1, 10) if copy_grid.is_valid(r, c, v)]
                    for val in candidates:
                        copy_grid.place(r, c, val)
                        if copy_grid.is_complete():
                            solutions[0] += 1
                            if solutions[0] >= limit:
                                return
                        else:
                            backtrack()
                        copy_grid.remove(r, c, val)
                    return  # No valid value for this cell
        
    backtrack()
    return solutions[0]

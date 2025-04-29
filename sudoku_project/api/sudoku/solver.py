from sudoku.grid import SudokuGrid
import random
import time

def solve(grid: SudokuGrid, record_steps=False) -> bool:
    """
    Solve the Sudoku puzzle using backtracking.
    Returns True if a solution is found, False otherwise.
    The grid is modified in place.
    
    If record_steps is True, returns (success, steps) where steps is a list of
    moves that lead to the solution.
    """
    steps = [] if record_steps else None
    solution_path = [] if record_steps else None
    empty_cells = [(r, c) for r in range(9) for c in range(9) if grid.board[r][c] == 0]
    total_empty = len(empty_cells)
    cells_filled = [0]  # Use list to allow modification in inner function
    
    def get_explanation(r: int, c: int, val: int, candidates: list) -> str:
        """Generate a clear explanation for the current solving step"""
        row_num = r + 1
        col_num = c + 1
        
        if len(candidates) == 1:
            return f"Cell at row {row_num}, column {col_num} can only be {val}. This is the only valid number that doesn't conflict with other cells in the same row, column, or 3x3 box."
        else:
            candidates_str = ', '.join(map(str, sorted(candidates)))
            return f"Placing {val} in cell at row {row_num}, column {col_num}. This cell could be any of these numbers: {candidates_str}. Trying {val} first and will backtrack if it doesn't lead to a solution."
    
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
            cells_filled[0] += 1
            
            # Create a step record but don't save it yet - only if it leads to a solution
            if record_steps:
                step = {
                    'position': (r, c),
                    'value': val,
                    'progress': round(cells_filled[0] / total_empty * 100, 1),
                    'explanation': get_explanation(r, c, val, candidates)
                }
                current_path.append(step)
                
            if solve_with_steps(grid, current_path):
                return True
                
            # Backtrack if solution not found
            grid.remove(r, c, val)
            cells_filled[0] -= 1
            
            # Remove this step from the current path if it didn't lead to a solution
            if record_steps and current_path:
                current_path.pop()
        
        return False
    
    # Call the helper function
    result = solve_with_steps(grid)
    
    if record_steps and solution_path:
        # Reconstruct the board states for the solution path
        board_states = []
        current_board = [row[:] for row in grid.board]  # Start with the solved board
        # Work backwards to create the sequence of board states
        for i in range(len(solution_path) - 1, -1, -1):
            step = solution_path[i]
            r, c = step['position']
            current_board[r][c] = 0  # Remove the number to get the previous state
            # Add the board state to the beginning of our list
            board_states.insert(0, [row[:] for row in current_board])
        
        # Update the solution path with board states
        for i, step in enumerate(solution_path):
            step['board'] = board_states[i]
    
    # Return appropriate result based on whether steps were requested
    if record_steps:
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

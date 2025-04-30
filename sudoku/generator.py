import random
import time
from sudoku.grid import SudokuGrid
from sudoku.solver import solve, count_solutions

def generate(clues=30, min_clues=17, timeout=10):
    """
    Generate a Sudoku puzzle with the specified number of clues.
    The puzzle is guaranteed to have a unique solution.
    
    Args:
        clues: Target number of clues to keep (default: 30)
        min_clues: Minimum number of clues (default: 17, theoretical minimum)
        timeout: Maximum time in seconds to spend generating (default: 10)
    
    Returns:
        tuple: (puzzle_grid, solution_grid)
    """
    # Ensure clues is within valid range
    clues = max(min_clues, min(clues, 81))
    
    start_time = time.time()
    
    # Start with an empty grid
    grid = SudokuGrid()
    
    # Add a few random values to create a different starting point each time
    # This creates a random seed that leads to different solutions
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    
    # Place 5-10 random initial values
    num_initial = random.randint(5, 10)
    for i in range(num_initial):
        r, c = positions[i]
        # Try random values until finding a valid one
        values = list(range(1, 10))
        random.shuffle(values)
        for val in values:
            if grid.is_valid(r, c, val):
                grid.place(r, c, val)
                break
    
    # Fill the grid completely
    solve(grid)
    
    # Save the solution
    solution = SudokuGrid([row[:] for row in grid.board])
    
    # Randomly remove cells while ensuring uniqueness
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    
    for r, c in cells:
        # Check timeout - if we're taking too long, return what we have
        if time.time() - start_time > timeout:
            # We've exceeded our timeout, return current state
            print(f"Generation timed out after {timeout} seconds. Returning puzzle with {sum(1 for i in range(9) for j in range(9) if grid.board[i][j] != 0)} clues.")
            return grid, solution
            
        # Skip if we've reached the target number of clues
        if sum(1 for i in range(9) for j in range(9) if grid.board[i][j] != 0) <= clues:
            break
            
        # Remember the value before removing
        val = grid.board[r][c]
        grid.remove(r, c, val)
        
        # Check if the puzzle still has a unique solution
        if count_solutions(grid) != 1:
            # If not, restore the value
            grid.place(r, c, val)
    
    return grid, solution

def generate_easy(clues=40):
    """Generate an easy puzzle with more clues."""
    return generate(clues=clues)

def generate_medium(clues=30):
    """Generate a medium difficulty puzzle."""
    return generate(clues=clues)

def generate_hard(clues=25):
    """Generate a hard puzzle with fewer clues."""
    return generate(clues=clues)

def generate_expert(clues=22):
    """Generate an expert level puzzle with minimal clues.
    Note: Uses 22 clues instead of 20 to ensure faster generation."""
    return generate(clues=clues, timeout=15)

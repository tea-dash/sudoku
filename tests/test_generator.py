import pytest
from sudoku.generator import generate, generate_easy, generate_medium, generate_hard, generate_expert
from sudoku.solver import count_solutions

def test_generate_default():
    """Test generating a puzzle with default settings."""
    grid, solution = generate()
    
    # Count how many clues (non-zero values) in the puzzle
    clues = sum(1 for r in range(9) for c in range(9) if grid.board[r][c] != 0)
    
    # Default should be around 30 clues
    assert 28 <= clues <= 32  # Allow for some variation
    
    # Puzzle should have exactly one solution
    assert count_solutions(grid) == 1
    
    # Solution should be valid (all positions filled)
    assert all(solution.board[r][c] != 0 for r in range(9) for c in range(9))

def test_generate_with_clues():
    """Test generating puzzles with different number of clues."""
    # Test with minimum allowed clues (17)
    min_grid, _ = generate(clues=17)
    min_clues = sum(1 for r in range(9) for c in range(9) if min_grid.board[r][c] != 0)
    assert 17 <= min_clues <= 22  # Allow for some variation
    assert count_solutions(min_grid) == 1
    
    # Test with maximum clues (81 - completely filled)
    max_grid, _ = generate(clues=81)
    max_clues = sum(1 for r in range(9) for c in range(9) if max_grid.board[r][c] != 0)
    assert max_clues == 81
    assert count_solutions(max_grid) == 1

def test_generate_difficulty_levels():
    """Test generating puzzles with different difficulty levels."""
    # Easy (should have more clues)
    easy_grid, _ = generate_easy()
    easy_clues = sum(1 for r in range(9) for c in range(9) if easy_grid.board[r][c] != 0)
    assert 35 <= easy_clues <= 45
    assert count_solutions(easy_grid) == 1
    
    # Medium
    medium_grid, _ = generate_medium()
    medium_clues = sum(1 for r in range(9) for c in range(9) if medium_grid.board[r][c] != 0)
    assert 28 <= medium_clues <= 35
    assert count_solutions(medium_grid) == 1
    
    # Hard
    hard_grid, _ = generate_hard()
    hard_clues = sum(1 for r in range(9) for c in range(9) if hard_grid.board[r][c] != 0)
    assert 23 <= hard_clues <= 28
    assert count_solutions(hard_grid) == 1
    
    # Expert
    expert_grid, _ = generate_expert()
    expert_clues = sum(1 for r in range(9) for c in range(9) if expert_grid.board[r][c] != 0)
    assert 17 <= expert_clues <= 23
    assert count_solutions(expert_grid) == 1

def test_solution_matches_puzzle():
    """Test that solution matches the puzzle (all clues are preserved)."""
    grid, solution = generate(clues=35)
    
    # Every non-zero value in the grid should match the solution
    for r in range(9):
        for c in range(9):
            if grid.board[r][c] != 0:
                assert grid.board[r][c] == solution.board[r][c]

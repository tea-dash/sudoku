document.addEventListener('DOMContentLoaded', function() {
    const board = document.getElementById('sudoku-board');
    const generateBtn = document.getElementById('generate-btn');
    const solveBtn = document.getElementById('solve-btn');
    const resetBtn = document.getElementById('reset-btn');
    const difficultySelect = document.getElementById('difficulty');
    const bearSpinner = document.getElementById('bear-spinner');
    
    // Step navigation controls
    const stepControls = document.getElementById('step-controls');
    const prevStepBtn = document.getElementById('prev-step-btn');
    const nextStepBtn = document.getElementById('next-step-btn');
    const stepCounter = document.getElementById('step-counter');
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    
    let currentPuzzle = null;
    let currentSolution = null;
    let originalState = null;
    let isSolving = false;
    let lastSteps = null;
    let currentStepIndex = 0;
    let animationInterval = null;
    let isPlaying = false;
    
    // Initialize empty board
    function initializeBoard() {
        board.innerHTML = '';
        
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.addEventListener('click', handleCellClick);
                board.appendChild(cell);
            }
        }
    }
    
    // Handle cell click for manual input
    function handleCellClick(e) {
        const cell = e.target;
        if (cell.classList.contains('prefilled') || isSolving) return;
        
        let value = parseInt(cell.textContent) || 0;
        value = (value + 1) % 10;
        
        cell.textContent = value === 0 ? '' : value;
    }
    
    // Update board with puzzle data
    function updateBoard(puzzleData, isPrefilled = true) {
        const cells = board.querySelectorAll('.cell');
        
        cells.forEach(cell => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            const value = puzzleData[row][col];
            
            cell.textContent = value === 0 ? '' : value;
            cell.classList.toggle('prefilled', value !== 0 && isPrefilled);
        });
        
        // Save original state if this is the initial puzzle
        if (isPrefilled) {
            originalState = JSON.parse(JSON.stringify(puzzleData));
        }
    }
    
    // Highlight a cell to show solving progress
    function highlightCell(row, col, value, isBacktrack = false) {
        const cells = board.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.classList.remove('highlight', 'backtrack');
        });
        
        const targetCell = [...cells].find(
            cell => parseInt(cell.dataset.row) === row && parseInt(cell.dataset.col) === col
        );
        
        if (targetCell) {
            targetCell.textContent = value === 0 ? '' : value;
            if (isBacktrack) {
                targetCell.classList.add('backtrack');
            } else {
                targetCell.classList.add('highlight');
            }
        }
    }
    
    // Reset step navigation controls
    function resetStepNavigation() {
        currentStepIndex = 0;
        updateStepCounter();
        prevStepBtn.disabled = true;
        nextStepBtn.disabled = lastSteps === null || lastSteps.length === 0;
        
        // Hide controls if no steps
        stepControls.style.display = lastSteps && lastSteps.length > 0 ? 'block' : 'none';
        
        // Make sure play is shown, pause is hidden
        playBtn.style.display = 'inline-block';
        pauseBtn.style.display = 'none';
        isPlaying = false;
        
        // Clear any existing animation
        if (animationInterval) {
            clearInterval(animationInterval);
            animationInterval = null;
        }
    }
    
    // Update step counter text
    function updateStepCounter() {
        if (!lastSteps) {
            stepCounter.textContent = 'Step 0 of 0';
            return;
        }
        stepCounter.textContent = `Step ${currentStepIndex + 1} of ${lastSteps.length}`;
    }
    
    // Show a specific step
    function showStep(index) {
        if (!lastSteps || lastSteps.length === 0) return;
        
        // Validate index
        index = Math.max(0, Math.min(index, lastSteps.length - 1));
        currentStepIndex = index;
        
        // Update buttons
        prevStepBtn.disabled = currentStepIndex === 0;
        nextStepBtn.disabled = currentStepIndex === lastSteps.length - 1;
        
        // Update counter
        updateStepCounter();
        
        // Show the step
        const step = lastSteps[currentStepIndex];
        console.log('Current step:', step); // Debug log
        updateBoard(step.board, false);
        
        const [row, col] = step.position;
        highlightCell(row, col, step.value);
        
        // Update explanation with more debug logging
        const explanationContainer = document.getElementById('step-explanation');
        const explanationText = document.getElementById('current-explanation');
        console.log('Explanation container:', explanationContainer); // Debug log
        console.log('Explanation element:', explanationText); // Debug log
        console.log('Step explanation:', step.explanation); // Debug log
        
        if (explanationContainer) {
            console.log('Explanation container style:', window.getComputedStyle(explanationContainer)); // Debug log
            explanationContainer.style.display = 'block';
            explanationContainer.style.visibility = 'visible';
            explanationContainer.style.opacity = '1';
        }
        
        if (explanationText && step.explanation) {
            explanationText.textContent = step.explanation;
            console.log('Updated explanation text to:', explanationText.textContent); // Debug log
            console.log('Explanation text style:', window.getComputedStyle(explanationText)); // Debug log
        }
    }
    
    // Previous step button
    prevStepBtn.addEventListener('click', function() {
        showStep(currentStepIndex - 1);
    });
    
    // Next step button
    nextStepBtn.addEventListener('click', function() {
        showStep(currentStepIndex + 1);
    });
    
    // Play button - start automatic animation
    playBtn.addEventListener('click', function() {
        if (!lastSteps || lastSteps.length === 0 || isPlaying) return;
        
        isPlaying = true;
        playBtn.style.display = 'none';
        pauseBtn.style.display = 'inline-block';
        
        // If we're at the end, go back to start
        if (currentStepIndex >= lastSteps.length - 1) {
            currentStepIndex = 0;
        }
        
        // Start animation interval
        animationInterval = setInterval(() => {
            showStep(currentStepIndex + 1);
            
            // If we reached the end, stop
            if (currentStepIndex >= lastSteps.length - 1) {
                pauseAnimation();
            }
        }, 150);
    });
    
    // Pause button - stop automatic animation
    pauseBtn.addEventListener('click', function() {
        pauseAnimation();
    });
    
    function pauseAnimation() {
        if (!isPlaying) return;
        
        isPlaying = false;
        playBtn.style.display = 'inline-block';
        pauseBtn.style.display = 'none';
        
        if (animationInterval) {
            clearInterval(animationInterval);
            animationInterval = null;
        }
    }
    
    // Animate solving steps
    function animateSolvingSteps(steps) {
        if (!steps || steps.length === 0) {
            alert('No steps to visualize');
            return;
        }
        
        // Save the steps for navigation
        lastSteps = steps;
        
        // Reset and show step controls
        resetStepNavigation();
        
        // Start at step 0
        showStep(0);
        
        // Start auto-play
        playBtn.click();
    }
    
    // Get current board state
    function getBoardState() {
        const boardState = Array(9).fill().map(() => Array(9).fill(0));
        const cells = board.querySelectorAll('.cell');
        
        cells.forEach(cell => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            const value = cell.textContent === '' ? 0 : parseInt(cell.textContent);
            
            boardState[row][col] = value;
        });
        
        return boardState;
    }
    
    // Generate a new puzzle
    generateBtn.addEventListener('click', function() {
        const difficulty = difficultySelect.value;
        
        // Hide step controls when generating new puzzle
        stepControls.style.display = 'none';
        lastSteps = null;
        
        // Show bear spinner
        bearSpinner.style.display = 'flex';
        
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ difficulty: difficulty })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data.puzzle) {
                throw new Error('Invalid response format');
            }
            currentPuzzle = data.puzzle;
            currentSolution = data.solution;
            updateBoard(currentPuzzle, true);
            
            // Hide bear spinner
            bearSpinner.style.display = 'none';
        })
        .catch(error => {
            console.error('Error generating puzzle:', error);
            alert('Error generating puzzle. Please try again.');
            
            // Hide bear spinner on error
            bearSpinner.style.display = 'none';
        });
    });
    
    // Solve the current puzzle
    solveBtn.addEventListener('click', function() {
        if (isSolving) return;
        
        // Always use visualization regardless of whether we have a solution
        const boardState = currentPuzzle || getBoardState();
        
        fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                board: boardState,
                show_steps: true
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.solved) {
                if (data.steps && data.steps.length > 0) {
                    // Animate the solution steps
                    animateSolvingSteps(data.steps);
                } else {
                    // Just show the final solution
                    updateBoard(data.board, false);
                    alert('Solution found but no steps to visualize');
                }
            } else {
                alert('No solution found for this puzzle!');
            }
        })
        .catch(error => {
            console.error('Error solving puzzle:', error);
            alert('Error solving puzzle. Please try again.');
        });
    });
    
    // Reset to original puzzle or empty board
    resetBtn.addEventListener('click', function() {
        if (originalState) {
            updateBoard(originalState, true);
            
            // Hide step controls
            stepControls.style.display = 'none';
            
            // Stop any ongoing animation
            pauseAnimation();
        } else {
            initializeBoard();
        }
    });
    
    // Initialize empty board on page load
    initializeBoard();
    
    // Generate a medium puzzle on load for demonstration
    generateBtn.click();
}); 
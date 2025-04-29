// Debug script to validate explanation display
console.log('Debug script loaded');

document.addEventListener('DOMContentLoaded', function() {
    // Check for explanation container
    const explanationContainer = document.getElementById('step-explanation');
    const explanationText = document.getElementById('current-explanation');
    
    console.log('Explanation container exists:', !!explanationContainer);
    console.log('Explanation text element exists:', !!explanationText);
    
    if (explanationContainer) {
        console.log('Explanation container display:', getComputedStyle(explanationContainer).display);
        console.log('Explanation container visibility:', getComputedStyle(explanationContainer).visibility);
        console.log('Explanation container opacity:', getComputedStyle(explanationContainer).opacity);
    }
    
    if (explanationText) {
        console.log('Current explanation text:', explanationText.textContent);
    }
    
    // Override the fetch API to log responses
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        const result = originalFetch.apply(this, arguments);
        
        if (url === '/solve') {
            console.log('Intercepted /solve request');
            result.then(response => {
                const clonedResponse = response.clone();
                clonedResponse.json().then(data => {
                    console.log('Solve response:', data);
                    if (data.steps && data.steps.length > 0) {
                        console.log('First step explanation:', data.steps[0].explanation);
                        console.log('Last step explanation:', data.steps[data.steps.length - 1].explanation);
                    }
                });
            });
        }
        
        return result;
    };
    
    // Add a button to manually test the explanation display
    const testBtn = document.createElement('button');
    testBtn.textContent = 'Test Explanation Display';
    testBtn.style.marginTop = '20px';
    testBtn.addEventListener('click', function() {
        if (explanationText) {
            explanationText.textContent = 'Test explanation: This is a test to ensure the explanation display is working correctly.';
            
            if (explanationContainer) {
                explanationContainer.style.display = 'block';
                explanationContainer.style.visibility = 'visible';
                explanationContainer.style.opacity = '1';
                
                // Force redraw
                explanationContainer.offsetHeight;
                
                console.log('After test: Explanation container display:', getComputedStyle(explanationContainer).display);
                console.log('After test: Explanation container visibility:', getComputedStyle(explanationContainer).visibility);
                console.log('After test: Explanation container opacity:', getComputedStyle(explanationContainer).opacity);
            }
        }
    });
    
    // Insert the test button after the step controls
    const stepControls = document.getElementById('step-controls');
    if (stepControls && stepControls.parentNode) {
        stepControls.parentNode.insertBefore(testBtn, stepControls.nextSibling);
    } else {
        // Fallback - add to body
        document.body.appendChild(testBtn);
    }
}); 
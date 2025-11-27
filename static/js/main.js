// Simple main.js - just handles the back button with null checks
document.addEventListener('DOMContentLoaded', () => {
    const backBtn = document.getElementById('back-btn');
    
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            // Clear results and show converter
            const resultsSection = document.getElementById('results-section');
            const backBtnContainer = document.getElementById('back-btn-container');
            const errorMessage = document.getElementById('error-message');
            
            if (resultsSection) resultsSection.classList.remove('active');
            if (backBtnContainer) backBtnContainer.style.display = 'none';
            if (errorMessage) errorMessage.style.display = 'none';
        });
    }
    
    console.log('Ghana Coordinate Converter loaded successfully!');
});
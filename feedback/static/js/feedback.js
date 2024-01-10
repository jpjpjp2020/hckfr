// DOM wrapper for preloading
document.addEventListener('DOMContentLoaded', function() {

    // textarea resize
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', autoResize);

        // Trigger resize on loading if textarea has content
        if (textarea.value) {
            autoResize.call(textarea);
        }
    }

    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }

    // Copy to clipboard
    window.copyToClipboard = function(codeId) {
        const codeElement = document.getElementById(codeId);

        if (!codeElement) {
            alert('No code found to copy.');
            return;
        }

        navigator.clipboard.writeText(codeElement.textContent).then(() => {
            alert('Code copied to clipboard.');
        }).catch(err => {
            console.error('Error copying text: ', err);
            alert('Unable to copy the code. Please try again or manually copy the code.');
        });
    }

    window.copyAllFeedbackToClipboard = function() {
        const feedbackContainer = document.getElementById('feedback-content');
        const textArea = document.createElement("textarea");
    
        textArea.value = feedbackContainer.innerText;
        
        document.body.appendChild(textArea);
        textArea.select();
    
        navigator.clipboard.writeText(textArea.value).then(() => {
            alert('Feedback copied to clipboard!');
        }).catch(err => {
            console.error('Error copying text: ', err);
            alert('Error copying feedback. Please try again or manually copy the content.');
        });
    
        document.body.removeChild(textArea);
    }

});
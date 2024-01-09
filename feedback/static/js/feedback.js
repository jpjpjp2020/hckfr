// textarea resize

const textarea = document.querySelector('textarea');
textarea.addEventListener('input', autoResize);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}

// trigger resize on loading

document.addEventListener('DOMContentLoaded', (event) => {
    if (textarea.value) {
        autoResize.call(textarea);
    }
});

// efwefef
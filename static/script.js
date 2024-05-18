document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');
    const loader = document.getElementById('loader');

    generateBtn.addEventListener('click', function() {
        const input = inputText.value.trim();

        if (!input) {
            generatedText.innerHTML = 'Please enter some text.';
            return;
        }

        // Show loader
        loader.style.display = 'block';
        generatedText.innerHTML = '';

        fetch('/generate-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input_text: input })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            generatedText.innerHTML = data.generated_text;
        })
        .catch(error => {
            console.error('Error:', error);
            generatedText.innerHTML = 'An error occurred. Please try again later.';
        })
        .finally(() => {
            // Hide loader
            loader.style.display = 'none';
        });
    });
});

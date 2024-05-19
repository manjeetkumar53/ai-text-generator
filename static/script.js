document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');
    const loader = document.getElementById('loader');
    const copyBtn = document.getElementById('copy-btn');

    generateBtn.addEventListener('click', function() {
        const input = inputText.value.trim();

        if (!input) {
            generatedText.innerHTML = 'Please enter some text.';
            return;
        }

        // Show loader
        loader.style.display = 'block';
        generatedText.innerHTML = '';
        copyBtn.style.display = 'none';

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
            generatedText.innerHTML = formatOutput(data.generated_text);
            copyBtn.style.display = 'inline-block';
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

    copyBtn.addEventListener('click', function() {
        const text = generatedText.innerText;
        navigator.clipboard.writeText(text).then(function() {
            alert('Text copied to clipboard');
        }).catch(function(error) {
            console.error('Could not copy text: ', error);
        });
    });

    function formatOutput(text) {
        // Replace **text** with <strong>text</strong>
        let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Replace *text* with <em>text</em>
        formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Replace _text_ with <u>text</u>
        formattedText = formattedText.replace(/_(.*?)_/g, '<u>$1</u>');
        // Replace newlines with <br> for line breaks
        formattedText = formattedText.replace(/\n/g, '<br>');
        // Handle numbered lists
        formattedText = formattedText.replace(/^\d+\.\s+(.*?)(?=\n|$)/gm, '<li>$1</li>');
        formattedText = formattedText.replace(/(<li>.*<\/li>)/g, '<ol>$1</ol>');
        // Handle bullet points
        formattedText = formattedText.replace(/^\*\s+(.*?)(?=\n|$)/gm, '<li>$1</li>');
        formattedText = formattedText.replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>');
        
        return formattedText;
    }
});

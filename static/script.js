document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');
    const loader = document.getElementById('loader');
    const copyBtn = document.getElementById('copy-btn');
    const modelSelect = document.getElementById('model-select');
    const temperatureInput = document.getElementById('temperature');
  
    generateBtn.addEventListener('click', function() {
      const input = inputText.value.trim();
      const model = modelSelect.value;
      const temperature = parseFloat(temperatureInput.value);
  
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
        body: JSON.stringify({
          input_text: input,
          model: model,
          temperature: temperature
        })
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
      let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>');
      formattedText = formattedText.replace(/_(.*?)_/g, '<u>$1</u>');
      formattedText = formattedText.replace(/\n/g, '<br>');
  
      formattedText = formattedText.replace(/^\d+\.\s+(.*?)(?=\n|$)/gm, '<li>$1</li>');
      formattedText = formattedText.replace(/(<li>.*<\/li>)/g, '<ol>$1</ol>');
  
      formattedText = formattedText.replace(/^\*\s+(.*?)(?=\n|$)/gm, '<li>$1</li>');
      formattedText = formattedText.replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>');
  
      return formattedText;
    }
  });
  
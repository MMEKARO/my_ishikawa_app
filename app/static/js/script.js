document.getElementById('categorize-btn').addEventListener('click', function() {
    const problem = document.getElementById('problem-input').value;

    fetch('/categorize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ problem: problem }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('causes').textContent = data.causes;
    });
});

document.getElementById('generate-pdf-btn').addEventListener('click', function() {
    const problem = document.getElementById('problem-input').value;
    const causes = document.getElementById('causes').textContent;

    fetch('/generate_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ problem: problem, causes: causes }),
    })
    .then(response => response.json())
    .then(data => {
        window.open(data.pdf);
    });
});

let sentimentChart = null;

document.getElementById('song-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const songTitle = document.getElementById('song-title').value;
    const artistName = document.getElementById('artist-name').value;
    const resultDiv = document.getElementById('result');

    // Clear previous results and chart
    resultDiv.innerHTML = '<p>Analyzing...</p>';
    if (sentimentChart) {
        sentimentChart.destroy();
        sentimentChart = null;
    }

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ song_title: songTitle, artist_name: artistName }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        // Build the lyrics HTML with sentiment
        let lyricsHtml = '<h3 class="mt-4">Lyrics with Sentiment Analysis:</h3>';
        const lines = data.lyrics.split('\n');
        lines.forEach((line, index) => {
            const sentiment = data.sentiments[index];
            const score = data.scores[index];
            let colorClass = sentiment.toLowerCase();
            lyricsHtml += line.trim() ? `<p class="${colorClass}">${line} <span class="small text-muted">(Score: ${score.toFixed(2)})</span></p>` : '<br>';
        });

        // Sentiment distribution HTML
        const sentimentDistHtml = `
            <h3>Sentiment Distribution:</h3>
            <ul class="list-group mb-4">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Positive
                    <span class="badge bg-success rounded-pill">${data.sentiment_distribution.Positive.toFixed(2)}%</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Negative
                    <span class="badge bg-danger rounded-pill">${data.sentiment_distribution.Negative.toFixed(2)}%</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Neutral
                    <span class="badge bg-warning text-dark rounded-pill">${data.sentiment_distribution.Neutral.toFixed(2)}%</span>
                </li>
            </ul>
        `;

        resultDiv.innerHTML = `
            <h2>${data.song_title} by ${data.artist_name}</h2>
            <h4>Overall Sentiment: <span class="text-${data.overall_sentiment.toLowerCase()}">${data.overall_sentiment}</span></h4>
            ${sentimentDistHtml}
            ${lyricsHtml}
        `;

        // Create the sentiment chart
        const ctx = document.getElementById('sentimentChart').getContext('2d');

        sentimentChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.scores.map((_, index) => `Line ${index + 1}`),
                datasets: [{
                    label: 'Sentiment Score',
                    data: data.scores,
                    backgroundColor: data.scores.map(score =>
                        score < -0.05 ? 'rgba(220, 53, 69, 0.5)' :
                        score > 0.05 ? 'rgba(40, 167, 69, 0.5)' :
                        'rgba(255, 193, 7, 0.5)'
                    ),
                    borderColor: data.scores.map(score =>
                        score < -0.05 ? 'rgba(220, 53, 69, 1)' :
                        score > 0.05 ? 'rgba(40, 167, 69, 1)' :
                        'rgba(255, 193, 7, 1)'
                    ),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        min: -1,
                        max: 1,
                    }
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let sentiment = data.sentiments[context.dataIndex];
                                return `Score: ${context.parsed.y.toFixed(2)} (${sentiment})`;
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        resultDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
        console.error('Error details:', error);
    }
});


// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

themeToggle.addEventListener('click', () => {
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
});

// On Load, set theme based on preference or saved setting
window.addEventListener('DOMContentLoaded', () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark' || (prefersDarkScheme.matches && !currentTheme)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
});

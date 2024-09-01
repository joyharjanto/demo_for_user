document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', searchClips);
    
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchClips();
        }
    });

    // Store the original content
    window.originalContent = document.getElementById('results').innerHTML;

    // Add event listener for the search input
    searchInput.addEventListener('input', function(e) {
        if (this.value.trim() === '') {
            restoreOriginalContent();
        }
    });
});

function searchClips() {
    const query = document.getElementById('searchInput').value.trim();
    console.log("Searching for:", query);
    
    if (query === '') {
        restoreOriginalContent();
        return;
    }

    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log("Search results:", data);
            const resultsDiv = document.getElementById('results');
            
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No results found.</p>';
            } else {
                resultsDiv.innerHTML = ''; // Clear current results
                data.forEach(clip => {
                    const clipDiv = document.createElement('div');
                    clipDiv.className = 'clip';
                    clipDiv.innerHTML = `
                        <div class="clip-content">
                            <h4>${clip.filename}</h4>
                            <video width="280" height="200" controls>
                                <source src="/video/${clip.filename}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                            <div class="tags">
                                ${clip.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                        </div>
                        <div class="button-container">
                            <a href="/download/${clip.filename}?download_name=${encodeURIComponent(clip.filename)}" class="download-button">Download</a>
                        </div>
                    `;
                    resultsDiv.appendChild(clipDiv);
                });
                makeVideosPlayable();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results').innerHTML = '<p>An error occurred while searching.</p>';
        });
}

function restoreOriginalContent() {
    document.getElementById('results').innerHTML = window.originalContent;
    makeVideosPlayable();
}

function makeVideosPlayable() {
    setTimeout(() => {
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            video.load();
        });
    }, 100); // Small delay to ensure DOM is updated
}
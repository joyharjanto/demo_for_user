document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var formData = new FormData(this);
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (uploadStatus) {
                    uploadStatus.textContent = data.message;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (uploadStatus) {
                    uploadStatus.textContent = 'Error uploading file(s)';
                }
            });
        });
    }
});
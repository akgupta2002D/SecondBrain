// github_dashboard.js
document.addEventListener('DOMContentLoaded', () => {
  // Fetch Spotify data asynchronously
  fetch('/github_data/spotify/')
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error('Spotify API error:', data.error)
        return
      }

      const trackListContainer = document.getElementById('track-list')
      data.top_tracks.forEach(track => {
        const trackCard = document.createElement('div')
        trackCard.classList.add('track-card')
        trackCard.innerHTML = `
                  <img src="${track.album_image}" alt="Album cover">
                  <h3>${track.name}</h3>
                  <p>${track.artist}</p>
                  <audio controls>
                      <source src="${track.preview_url}" type="audio/mpeg">
                      Your browser does not support the audio element.
                  </audio>
              `
        trackListContainer.appendChild(trackCard)
      })
    })
    .catch(error => {
      console.error('Error fetching Spotify data:', error)
    })
})

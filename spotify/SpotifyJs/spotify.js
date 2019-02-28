var mainContainer = document.getElementById('js-main-container'),
    loginContainer = document.getElementById('js-login-container'),
    loginButton = document.getElementById('js-btn-login'),
    background = document.getElementById('js-background');

var spotifyPlayer = new SpotifyPlayer();

var info = ``;


var template = function (data) {
  info = ``;
  info = `

  <div class="main-wrapper">
    <div class="now-playing__img">
          <img style=" position: absolute; width: 150px; bottom: 45px; right: 285.5px;" src="${data.item.album.images[0].url}">
    </div>
    <div class="now-playing__side">
    <div class="now-playing__artist">${data.item.artists[0].name}</div>
      <div class="now-playing__status ">
        <i class="material-icons" style="position: absolute; right: 55px;"> ${data.is_playing ? 'pause_circle_outline' : 'play_circle_outline'} </i>
        ${data.is_playing ? 'Playing' : 'Paused'}
      </div>

      <div class="progress">
        <div class="progress__bar" style="width:${data.progress_ms * 100 / data.item.duration_ms}%"></div>
      </div>
      <div class="now-playing__name">${data.item.name}</div>
    </div>
  </div>
  <div class="background" style="background-image:url(${data.item.album.images[0].url})"></div>
`;

localStorage.info = JSON.stringify(info);

return info;
};

spotifyPlayer.on('update', response => {
  mainContainer.innerHTML = template(response);
});

spotifyPlayer.on('login', user => {
  if (user === null) {
    loginContainer.style.display = 'none';
    mainContainer.style.display = 'none';

    
    var html5docs = JSON.parse(localStorage.info);
    document.getElementById('js-default-container').innerHTML = html5docs;
    document.getElementById('js-default-container').style.display = 'block';
    

  } else {
    loginContainer.style.display = 'none';
    mainContainer.style.display = 'block';
  }
});

/*loginButton.addEventListener('click', () => {
    spotifyPlayer.login();
}); */

spotifyPlayer.init();
spotifyPlayer.login();


function loadData(system) {

  // CURRENT CONDITIONS
  var $icon = $('#icon');
  var $temp = $('#temp');
  var $tempScale = $('#tempScale');
  var inputCity = system;

  //var accuweatherApiKey = "eOYiiAjNR0EuRaIGNoxAlXQQLn56cQMb";
  var accuweatherApiKey = "KrnJm3pGAtha40EFim82KLEqvaikzMeS"; // Accuweather api key2
  //var accuweatherApiKey = "XVmXE5NJJKoX17t4EucrFusDJSwYcStk"; // My api key
  var locationResourceURL = 'https://dataservice.accuweather.com/locations/v1/cities/search?apikey=' + accuweatherApiKey + '&q=' + inputCity;

  $.ajax({
    url: locationResourceURL,
    method: 'GET'
  }).done(function(result) { // Success
    
    
  var locationKey = result[0].Key; // Location key
  //var location = result[0].EnglishName; // City name

  var currentConditionsResourceURL = 'https://dataservice.accuweather.com/currentconditions/v1/' + locationKey + '?apikey=' + accuweatherApiKey + '&details=true';

      // Get current conditions (Accuweather Current Conditions API)
      $.ajax({
        url: currentConditionsResourceURL,
        method: 'GET'
      }).done(function(result) { // Success

        var temp;
        var tempScale;

        //Get the new icon image. All the image files are located in icons/conditions folder
        var icon = '../weather/icons/conditions/' + result[0].WeatherIcon + '.svg';
        

        //Get the new temperature
        temp = Math.round(result[0].Temperature.Imperial.Value).toString();

        //Get the Scale
        tempScale = '°F';

        //Change the temperature, scale and icon from the HTML Identifier.
        $temp.text(temp);
        $tempScale.text(tempScale);
        $icon.attr("src", icon);

      }).fail(function(err) { // Error handling
        console.log("error");
        throw err;
      });

    }).fail(function(err) { // Error handling
      console.log("error");
      throw err;
    });
  }

  //Always run this function with location name "Chico"
  loadData("Chico");
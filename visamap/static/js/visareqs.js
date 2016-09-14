$(document).ready(function() {
      var initializeMap = function(){
        $('#vmap').vectorMap(
        {
            map: 'world_en',
            backgroundColor: '#a5bfdd',
            borderColor: '#818181',
            borderOpacity: 0.25,
            borderWidth: 1,
            color: '#f4f3f0',
            enableZoom: true,
            hoverColor: 'pink',
            hoverOpacity: null,
            normalizeFunction: 'linear',
            scaleColors: ['#b6d6ff', '#005ace'],
            selectedColor: '#c9dfaf',
            selectedRegions: null,
            showTooltip: true,
            colors: null,
            onRegionClick: function(element, code, region)
            {
                element.preventDefault();
            }
        });
      };

      initializeMap();

      var getVisaColor = function(visaType){
          switch(visaType){
              case "Visa required":
                  color = 'red';
                  break;
              case "Visa not required":
                  color = 'green';
                  break;
              case "Visa on arrival":
                  color = 'yellow';
                  break;
              default:
                  color = 'gray';
          }
          return color;
      };

      var resetMap = function(){
          /* It is needed to create a new map because there is no function to redraw the map */
          $('#vmap').replaceWith('<div id="vmap" style="width: 600px; height: 400px;"></div>');
          initializeMap();
      };

      var resetVisaDetails = function(){
          $("#visaDetail").html("");
          $("#visaDetail").val("0");
      };

      /* Changes map colors when selecting an origin country */
      $("#origCitizenship").change(function(){
          $.get("requirements/" + this.value, function(countryRequirements){
              var countryColors = {}

              /* Iterating over visa types to check which countries use it */
              for (var visaType in countryRequirements) {
                  if (countryRequirements.hasOwnProperty(visaType)) {
                      color = getVisaColor(visaType);
                      countriesWithThisVisa = countryRequirements[visaType];
                      arrayLength = countriesWithThisVisa.length;
                      for(var i=0; i < arrayLength; i++){
                          countryColors[countriesWithThisVisa[i]] = color;
                      }
                  }
              }

              /* We need to reset the map to avoid old colors from the last country */
              resetMap();

              /* Also resetting visa details */
              resetVisaDetails();

              $('#vmap').vectorMap('set', 'colors', countryColors);
          });
      });

      var showVisaObservations = function(destination_id){
          originCountryId =  $("#origCitizenship").val();

          if(originCountryId != 0){
              $.get("requirements/" + originCountryId + "/" + destination_id, function(data){
                  $("#visaDetail").html("<strong>Observations</strong><br/>" +
                                        data.observations);
              });
          }
      };

      $("#destCountry").change(function(){
          showVisaObservations(this.value);
      });

});
$(document).ready(function() {

      /* Changes map colors when selecting an origin country */
      $("#origCitizenship").change(function(){
          $("#destCountry").val("0");
          $.get("requirements/" + this.value, function(countryRequirements){
              var countryColors = {}

              /* Iterating over visa types to check which countries use it */
              for (var visaType in countryRequirements) {
                  if (countryRequirements.hasOwnProperty(visaType)) {
                      color = mapHandler.getVisaColor(visaType);
                      countriesWithThisVisa = countryRequirements[visaType];
                      arrayLength = countriesWithThisVisa.length;
                      for(var i=0; i < arrayLength; i++){
                          countryColors[countriesWithThisVisa[i]] = color;
                      }
                  }
              }

              /* We need to reset the map to avoid old colors from the last country */
              mapHandler.resetMap();

              /* Also resetting visa details */
              mapHandler.resetVisaDetails();

              $('#vmap').vectorMap('set', 'colors', countryColors);
          });
      });

      var showVisaObservations = function(destination_id){
          originCountryId =  $("#origCitizenship").val();

          if(originCountryId != 0){
              $.get("requirements/" + originCountryId + "/" + destination_id + "/", function(data){
                  $("#visaDetail").html("<strong>Observations</strong><br/>" +
                                        data.observations);
              });
          }
      };

      $("#destCountry").change(function(){
          showVisaObservations(this.value);
      });

      var mapCallback = function(code){
          showVisaObservations(code);
          $("#destCountry").val(code);
      };

      mapHandler.initializeMap(mapCallback);

});
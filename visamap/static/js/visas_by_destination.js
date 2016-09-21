$(document).ready(function() {

     /* Changes map colors when selecting a destination country */
      $("#destCountry").change(function(){
          $("#origCountry").val("0");
          $.get("/requirements_reversed/" + this.value + "/", function(countryRequirements){
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

      var showVisaObservations = function(origin_code){
          var destCountryId =  $("#destCountry").val();

          if(destCountryId != 0){
              $.get("/requirements/" + origin_code + "/" + destCountryId + "/", function(data){
                  $("#visaDetail").html("<strong>Observations</strong><br/>" +
                                        data.observations);
              });
          }
      };

      $("#origCountry").change(function(){
          showVisaObservations(this.value);
      });

      var mapCallback = function(code){
          showVisaObservations(code);
          $("#origCountry").val(code);
      };

      mapHandler.initializeMap(mapCallback);
});
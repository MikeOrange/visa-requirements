$(document).ready(function() {

     /* Changes map colors when selecting a destination country */
      $("#destCountry").change(function(){
          $("#origCountry").val("0");

          /* Resetting visa details */
          mapHandler.resetVisaDetails();

          /* Show to let user know that content is loading */
          $("#loadingSpinner").show();

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

              $('#vmap').vectorMap('set', 'colors', countryColors);

              /* Finished loading */
              $("#loadingSpinner").hide();
          });
      });

      var showVisaObservations = function(origin_code){
          var destCountryId =  $("#destCountry").val();

          if(destCountryId != 0){
              $("#loadingSpinner").show();
              $.get("/requirements/" + origin_code + "/" + destCountryId + "/", function(data){
                  $("#visaDetail").html("<strong>Observations</strong><br/>" +
                                        data.observations);
                  $("#loadingSpinner").hide();
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
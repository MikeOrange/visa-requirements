var mapHandler = (function(self){

      self.initializeMap = function(callback){

        self.mapCallback = callback;

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
                self.mapCallback(code);
            }
        });

        sizeMap();
      };

      /* responsiveness solution found on http://stackoverflow.com/questions/26618012/trying-to-get-a-jqvmap-to-scale-correctly-on-iphone */
      function sizeMap() {
        var containerWidth = $('#worldMap').width(),
            containerHeight = (containerWidth / 1.6);

        $('#vmap').css({
            'width': containerWidth,
            'height': containerHeight
        });
      }
      $(window).on("resize", sizeMap);

      self.getVisaColor = function(visaType){
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
              case "origin country":
                  color = 'blue';
                  break;
              default:
                  color = 'gray';
          }
          return color;
      };

      self.resetMap = function(){
          /* It is needed to create a new map because there is no function to redraw the map */
          $('#vmap').replaceWith('<div id="vmap" style="width: 600px; height: 400px;"></div>');
          self.initializeMap(self.mapCallback);
      };

      self.resetVisaDetails = function(){
          $("#visaDetail").html("");
          $("#visaDetail").val("0");
      };

      return self;
}(mapHandler || {}));
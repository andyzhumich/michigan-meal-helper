function replace_amount_id(new_id) {
    var amount = document.getElementById("amount");
    amount.id = new_id + "-amount";
}

function init_sliders() {
    //cal slider
    $( function() {
        $( "#cal-range" ).slider({
          range: true,
          min: 0,
          max: 1500,
          values: [ 0, 500 ],
          step: 20,
          slide: function( event, ui ) {
            $( "#cal-amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
          }
        });
        $( "#cal-amount" ).val($( "#cal-range" ).slider( "values", 0 ) + " - " + $( "#cal-range" ).slider( "values", 1 ) );
      } );
    //protein slider
    $( function() {
        $( "#protein-range" ).slider({
          range: true,
          min: 0,
          max: 100,
          values: [ 0, 50 ],
          step: 5,
          slide: function( event, ui ) {
            $( "#protein-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
          }
        });
        $( "#protein-amount" ).val($( "#protein-range" ).slider( "values", 0 ) + "g - " + $( "#protein-range" ).slider( "values", 1 ) + "g" );
      } );
    //fat slider
    $( function() {
        $( "#fat-range" ).slider({
          range: true,
          min: 0,
          max: 100,
          values: [ 0, 50 ],
          step: 5,
          slide: function( event, ui ) {
            $( "#fat-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
          }
        });
        $( "#fat-amount" ).val($( "#fat-range" ).slider( "values", 0 ) + "g - " + $( "#fat-range" ).slider( "values", 1 ) + "g" );
      } );
    //carb slider
    $( function() {
        $( "#carb-range" ).slider({
          range: true,
          min: 0,
          max: 100,
          values: [ 0, 50 ],
          step: 5,
          slide: function( event, ui ) {
            $( "#carb-amount" ).val( ui.values[ 0 ] + "g - " + ui.values[ 1 ] + "g" );
          }
        });
        $( "#carb-amount" ).val($( "#carb-range" ).slider( "values", 0 ) + "g - " + $( "#carb-range" ).slider( "values", 1 ) + "g" );
      } );
}

scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});
		
    	$('#tleTable').DataTable();	
    	$('.selectpicker').selectpicker();


    	$("#button_one").click(function() {
 		 window.alert( "Handler for .click() called." );
		});

    	
});


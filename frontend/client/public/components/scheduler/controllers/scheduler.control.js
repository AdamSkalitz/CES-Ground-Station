scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL){
		$scope.hello = "hello tdddhere ya tit";
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});
		
    	$('#tleTable').DataTable();	
});


scheduler
	.controller('SchedulerController', function($scope, TLE, AZEL){
		TLE.query().$promise.then(function(data) {
			$scope.tles = data;
		});
		AZEL.query().$promise.then(function(date){
			$scope.azel = data;
		});

		/**
		$scope.button_click = function() {
          window.alert("boopity");
      };

    	angular.element(document).ready(function(){
    		$('#tleTable').DataTable();	
  			//$('.selectpicker').selectpicker('refresh');   	
    	})
    	**/
    	
});


scheduler.directive('bootSelectPicker', function(){
	 return {
     restrict: "A",
     require: "ngModel",
     link: function(scope, element, attrs, ctrl) {      
       $(element).selectpicker('refresh');
     }
   };
})






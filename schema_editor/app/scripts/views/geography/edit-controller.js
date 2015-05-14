(function () {
    'use strict';

    /* ngInject */
    function GeographyEditController($stateParams, Geography) {
        var ctl = this;
        initialize();


        /**
         * Updates the selected geometry
         */
        ctl.geoUpdate = function() {
            delete(ctl.workingGeo.source_file);
            var bounds = new Geography(ctl.workingGeo);

            var updateRequest = bounds.$update();
            ctl.updateState = 'requesting';
            updateRequest.then(function(data) {
                ctl.updateState = 'update-success';
                ctl.serverSays = data;
            }, function(data) {
                ctl.updateState = 'update-error';
                ctl.errorMessage = Geography.errorMessage(data.status);
            });

        };

        function initialize() {
            ctl.colors = ['Red', 'Blue', 'Green'];
            ctl.workingGeo = Geography.get({ uuid: $stateParams.uuid });
        }
    }

    angular.module('ase.views.geography')
    .controller('GeoEditController', GeographyEditController);
})();

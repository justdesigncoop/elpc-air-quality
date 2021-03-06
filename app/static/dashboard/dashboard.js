/*----------------------------------------------------------------------------
  global vars
 *----------------------------------------------------------------------------*/
var pmLevels = [0.0, 12.0, 35.0, 55.0];

var countLevels = [0, 100, 500, 2500];

var geoTypes = {
    NONE: 0,
    NEIGHBORHOODS: 1,
    TRACTS: 2,
    WARDS: 3,
    HEXAGONS: 4,
    ZIPCODES: 5,
    properties: {
        0: {value: 0, name: '', column: '', table: '', cb: getNone},
        1: {value: 1, name: 'Neighborhood', column: 'neighborhood', table: 'neighborhoods', cb: getNeighborhoods},
        2: {value: 2, name: 'Census', column: 'tract',  table: 'tracts', cb: getTracts},
        3: {value: 3, name: 'Ward', column: 'ward', table: 'wards', cb: getWards},
        4: {value: 4, name: 'Hexagon', column: 'hexagon', table: 'hexagons', cb: getHexagons},
        5: {value: 5, name: 'Zip Code', column: 'zipcode', table: 'zipcodes', cb: getZipcodes},
   }
};

var defaultLoc = 0;

// https://coolors.co/2da641-f9dc2e-f57f22-f4001c-1616e5
var coverageColor = '#1616E5';

var sensorNames = [
  'AirBeam-PM',
  'AirBeam2-PM2.5'
];

var sampleSize = 5000;

var maxOpacity = 0.7;
var minOpacity = 0.15;

$.ajaxSetup({
    headers: { "X-CSRFToken": '{{csrf_token}}' }
});

/*----------------------------------------------------------------------------
  check sensor name
 *----------------------------------------------------------------------------*/
function checkSensorName(sensor_name) {
  return sensorNames.includes(sensor_name);
}

/*----------------------------------------------------------------------------
  get legend
 *----------------------------------------------------------------------------*/
function getLegend(title, levels, color) { 
    var labels = [],
        from, to;
    
    labels.push(title);

    for (var i = 0; i < levels.length; i++) {
        from = levels[i];
        to = levels[i + 1];

        labels.push(
            '<i style="background:' + color(from) + '"></i> ' +
            from + (to ? '–' + to : '+'));
    }
    
    return labels.join('<br />');
}

/*----------------------------------------------------------------------------
  last updated
 *----------------------------------------------------------------------------*/
function lastUpdated(data, callback) {
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/last_updated/',
        data: data,
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get users
 *----------------------------------------------------------------------------*/
function getUsers(data, callback) {
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_users/',
        data: data,
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get sessions
 *----------------------------------------------------------------------------*/
function getSessions(data, callback) {
    var user_ids = JSON.stringify(data['user_ids']);
    var keywords = JSON.stringify(data['keywords']);
    //console.log(user_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_sessions/',
        data: {
            'user_ids': user_ids,
            'keywords': keywords,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get streams
 *----------------------------------------------------------------------------*/
function getStreams(data, callback) {
    var session_ids = JSON.stringify(data['session_ids']);
    var sensor_names = JSON.stringify(data['sensor_names']);
    var sample_size = JSON.stringify(data['sample_size']);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_streams/',
        data: {
            'session_ids': session_ids,
            'sensor_names': sensor_names,
            'sample_size': sample_size,
        },
        dataType: 'json',
        success: callback,
    }); 
}

/*----------------------------------------------------------------------------
  get measurements
 *----------------------------------------------------------------------------*/
function getMeasurements(data, callback) {
    var stream_ids = JSON.stringify(data['stream_ids']);
    var geo_type = JSON.stringify(data['geo_type']);
    var geo_boundaries = JSON.stringify(data['geo_boundaries']);
    var sample_size = JSON.stringify(data['sample_size']);
    var min_value = JSON.stringify(data['min_value']);
    var max_value = JSON.stringify(data['max_value']);
    var week_day = JSON.stringify(data['week_day']);
	var start_date = JSON.stringify(data['start_date']);
	var end_date = JSON.stringify(data['end_date']);
	var start_time = JSON.stringify(data['start_time']);
	var end_time = JSON.stringify(data['end_time']);
    //console.log(stream_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_measurements/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
            'geo_boundaries': geo_boundaries,
            'sample_size': sample_size,
            'min_value': min_value,
            'max_value': max_value,
            'week_day': week_day,
			'start_date': start_date,
			'end_date': end_date,
			'start_time': start_time,
			'end_time': end_time,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get selected options
 *----------------------------------------------------------------------------*/
function getSelectedOptions(id) {
    // get list of options as int
    var options = [];
    $(id.concat(" option")).each(function() {
        if(this.selected) {
            options.push(parseInt($(this).val(), 10));
        }
    });
    //console.log(options);
    
    return options;
}

/*----------------------------------------------------------------------------
  color map from AirCasting
 *----------------------------------------------------------------------------*/
function colorMap(value) {
    if(value < pmLevels[1]) {
        return '#2DA641';
    }
    else if(value < pmLevels[2]) {
        return '#F9DC2E';
    }
    else if(value < pmLevels[3]) {
        return '#F57F22';
    }
    else {
        return '#F4001C';
    }
}

/*----------------------------------------------------------------------------
  get neighborhoods
 *----------------------------------------------------------------------------*/
function getNeighborhoods(data, callback) {
    var neighborhood_ids = JSON.stringify(data['neighborhood_ids']);
    //console.log(neighborhood_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_neighborhoods/',
        data: {
            'neighborhood_ids': neighborhood_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get tracts
 *----------------------------------------------------------------------------*/
function getTracts(data, callback) {
    var tract_ids = JSON.stringify(data['tract_ids']);
    //console.log(tract_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_tracts/',
        data: {
            'tract_ids': tract_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get wards
 *----------------------------------------------------------------------------*/
function getWards(data, callback) {
    var ward_ids = JSON.stringify(data['ward_ids']);
    //console.log(ward_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_wards/',
        data: {
            'ward_ids': ward_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get hexagons
 *----------------------------------------------------------------------------*/
function getHexagons(data, callback) {
    var hexagon_ids = JSON.stringify(data['hexagon_ids']);
    var min_counts = JSON.stringify(data['min_counts']);
    //console.log(hexagon_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_hexagons/',
        data: {
            'hexagon_ids': hexagon_ids,
            'min_counts': min_counts,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get zipcodes
 *----------------------------------------------------------------------------*/
function getZipcodes(data, callback) {
    var zipcode_ids = JSON.stringify(data['zipcode_ids']);
    //console.log(zipcode_ids);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_zipcodes/',
        data: {
            'zipcode_ids': zipcode_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get none
 *----------------------------------------------------------------------------*/
function getNone(data, callback) {
    callback([]);
}

/*----------------------------------------------------------------------------
  get averages
 *----------------------------------------------------------------------------*/
function getAverages(data, callback) {
    var stream_ids = JSON.stringify(data['stream_ids']);
    var geo_type = JSON.stringify(data['geo_type']);
    var week_day = JSON.stringify(data['week_day']);
	var start_date = JSON.stringify(data['start_date']);
	var end_date = JSON.stringify(data['end_date']);
	var start_time = JSON.stringify(data['start_time']);
	var end_time = JSON.stringify(data['end_time']);
    var sample_size = JSON.stringify(data['sample_size']);
     
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_averages/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
            'week_day': week_day,
			'start_date': start_date,
			'end_date': end_date,
			'start_time': start_time,
			'end_time': end_time,
			'sample_size': sample_size,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get counts
 *----------------------------------------------------------------------------*/
function getCounts(data, callback) {
    var stream_ids = JSON.stringify(data['stream_ids']);
    var geo_type = JSON.stringify(data['geo_type']);
    
    // execute ajax call
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        type: 'POST',
        url: '/dashboard/ajax/get_counts/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
        },
        dataType: 'json',
        success: callback,
    });
}

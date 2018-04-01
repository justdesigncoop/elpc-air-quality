/*----------------------------------------------------------------------------
  global vars
 *----------------------------------------------------------------------------*/
var pmLevels = [0.0, 12.0, 35.0, 55.0];

var geoTypes = {
    NONE: 0,
    CENSUS: 1,
    NEIGHBORHOODS: 2,
    WARDS: 3,
    properties: {
        0: {value: 0, name: '', column: '', ret: '', cb: null},
        1: {value: 1, name: 'Census', column: 'tract', ret: 'census', cb: getCensus},
        2: {value: 2, name: 'Neighborhoods', column: 'neighborhood', ret: 'neighborhoods', cb: getNeighborhoods},
        3: {value: 3, name: 'Wards', column: 'ward', ret: 'wards', cb: getWards},
   }
};

// https://coolors.co/2da641-f9dc2e-f57f22-f4001c-1616e5
var coverageColor = '#1616E5';

/*----------------------------------------------------------------------------
  get users
 *----------------------------------------------------------------------------*/
function getUsers(data, callback) {
    // execute ajax call
    $.ajax({
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
    //console.log(sessions);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_streams/',
        data: {
            'session_ids': session_ids,
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
    //console.log(stream_ids);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_measurements/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
            'geo_boundaries': geo_boundaries,
            'sample_size': sample_size,
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
  color map
 *----------------------------------------------------------------------------*/
function colorMap(value) {
    //var hue = ((1.0 - value)*100).toString(10);
    //return ['hsl(', hue, ', 100%, 50%)'].join('');
    
    // color mapping from AirCasting
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
        url: '/dashboard/ajax/get_neighborhoods/',
        data: {
            'neighborhood_ids': neighborhood_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get census
 *----------------------------------------------------------------------------*/
function getCensus(data, callback) {
    var tracts = JSON.stringify(data['tracts']);
    //console.log(tracts);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_census/',
        data: {
            'tracts': tracts,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get wards
 *----------------------------------------------------------------------------*/
function getWards(data, callback) {
    var wards = JSON.stringify(data['wards']);
    //console.log(wards);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_wards/',
        data: {
            'wards': wards,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get averages
 *----------------------------------------------------------------------------*/
function getAverages(data, callback) {
    var stream_ids = JSON.stringify(data['stream_ids']);
    var geo_type = JSON.stringify(data['geo_type']);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_averages/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
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
        url: '/dashboard/ajax/get_counts/',
        data: {
            'stream_ids': stream_ids,
            'geo_type': geo_type,
        },
        dataType: 'json',
        success: callback,
    });
}

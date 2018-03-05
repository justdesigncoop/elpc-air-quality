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
    var user_ids = JSON.stringify(data);
    //console.log(user_ids);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_sessions/',
        data: {
            'user_ids': user_ids,
        },
        dataType: 'json',
        success: callback,
    });
}

/*----------------------------------------------------------------------------
  get streams
 *----------------------------------------------------------------------------*/
function getStreams(data, callback) {
    var sessions = JSON.stringify(data);
    //console.log(sessions);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_streams/',
        data: {
            'sessions': sessions,
        },
        dataType: 'json',
        success: callback,
    }); 
}

/*----------------------------------------------------------------------------
  get measurements
 *----------------------------------------------------------------------------*/
function getMeasurements(data, callback) {
    var streams = JSON.parse(data['streams']);
    //console.log(streams);
    
    // iterate through streams, get measurements
    for (i = 0; i < streams.length; ++i) {
        // check for correct sensor
        if(streams[i]['fields']['sensor_name'] == 'AirBeam-PM') {
            // execute ajax call
            $.ajax({
                url: '/dashboard/ajax/get_measurements/',
                data: {
                    'stream_id': streams[i]['pk'],
                },
                dataType: 'json',
                success: callback,
            });
        }
    }
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


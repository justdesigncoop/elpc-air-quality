// get users
function getUsers(data, callback) {
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_users/',
        data: data,
        dataType: 'json',
        success: callback,
    });
}

// get sessions
function getSessions(data, callback) {
    //console.log(data);
    
    // iterate through measurements, get streams
    for (i = 0; i < sessions.length; ++i) {
        // execute ajax call
        $.ajax({
            url: '/dashboard/ajax/get_sessions/',
            data: data,
            dataType: 'json',
            success: getStreams
        });
    }
}

// get streams
function getStreams(data, callback) {
    var sessions = JSON.parse(data['sessions']);
    //console.log(sessions);
    
    // iterate through measurements, get streams
    for (i = 0; i < sessions.length; ++i) {
        // execute ajax call
        $.ajax({
            url: '/dashboard/ajax/get_streams/',
            data: {
                'session_id': sessions[i]['pk'],
            },
            dataType: 'json',
            success: callback,
        }); 
    }
}

// get measurements
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


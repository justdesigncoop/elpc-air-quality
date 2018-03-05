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
    //console.log(stream_ids);
    
    // execute ajax call
    $.ajax({
        url: '/dashboard/ajax/get_measurements/',
        data: {
            'stream_ids': stream_ids,
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


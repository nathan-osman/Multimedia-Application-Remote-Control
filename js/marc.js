/* Global object for communicating with the server. */
var MARC = {
    
    /* Utility method for connecting back to the server to make an API request. */
    'request': function(method, callback) {
        $.ajax({
            'success': callback,
            'type':    'POST',
            'url':     '/api' + method,
        });
    },
    
    /* Simple and (hopefully) self-explanatory methods. */
    'prev': function() { this.request('/amarok/prev'); },
    'play': function() { this.request('/amarok/play'); },
    'next': function() { this.request('/amarok/next'); }
};
/* Global object for communicating with the server. */
var MARC = {
    
    /* The current player and a method for switching it. */
    'currentPlayer': '',
    'switchPlayer': function(player) {
        this.currentPlayer = player;
        $('#player').attr('class', 'icons icons-' + player);
    },
    
    /* Utility method for connecting back to the server to make an API request. */
    'request': function(method, callback) {
        $.ajax({
            'success': callback,
            'type':    'POST',
            'url':     '/api/' + this.currentPlayer + method,
        });
    },
    
    /* Enumerate all currently running media players. */
    'init': function() {
        this.switchPlayer('amarok');
    },
    
    /* Simple and (hopefully) self-explanatory methods. */
    'prev': function() { this.request('/prev'); },
    'play': function() { this.request('/play'); },
    'next': function() { this.request('/next'); }
};

/* Initialize the player. */
MARC.init();
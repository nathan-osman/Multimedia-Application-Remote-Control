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
    
    /* Displays information about the currently playing song. */
    'refreshInfo': function() {
        this.request('/info', function(data) {
            $('#info').html('<table><tr><th>Title:</th><td>' + data['title'] + '</td></tr><tr><th>Artist:</th><td>' + data['artist'] + '</td></tr><tr><th>Album:</th><td>' + data['album'] + '</td></tr></table>');
            $('#art').html('<img src="/art/' + data['art'] + '" />');
        });
    },
    
    /* Enumerate all currently running media players. */
    'init': function() {
        this.switchPlayer('amarok');
        this.refreshInfo();
    },
    
    /* Simple and (hopefully) self-explanatory methods. */
    'prev': function() { this.request('/prev'); },
    'play': function() { this.request('/play'); },
    'next': function() { this.request('/next'); }
};

/* Initialize the player. */
MARC.init();
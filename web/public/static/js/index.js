$('document').ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('system', {data: 'I\'m connected!'});
    });
    //
});
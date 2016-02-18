const React = require("react");
const ReactDOM = require('react-dom');

const Serreminator = require('./Serreminator.js');
const autobahn = require('autobahn');

$(document).ready(function(){
    var connection = new autobahn.Connection({
        url: 'ws://localhost:8080/ws',
        realm: 'realm1'
    });

    connection.onopen = function(session){
        console.log("Connected to ws://localhost:8080/ws !");
        ReactDOM.render(<Serreminator session={session} />, document.getElementById('root'));
    };
    connection.open();
});

const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');

const opts = {
    topic: "sensor.box_temp",
    id: "boite",
    PIDtarget: "pid.input.temp",
    name: "Température",
    unity: "°C",
    PIDsetter: "pid.temp.set_target",
    max: 60,
    min: 0
}

const Box = React.createClass({
    render: function() {
        console.log("Render Box");
        return <div>
            <div className="col-md-9">
                <Graph {...opts} session={this.props.session}/>
            </div>

            <div className="col-md-3">
                <Value {...opts} session={this.props.session}/>
            </div>
        </div>;
    }
});

module.exports = Box;

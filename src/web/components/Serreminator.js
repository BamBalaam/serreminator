const React = require("react");
const Metric = require('./Metric.js');

const Serreminator = React.createClass({
   render: function() {
        console.log("Render Serreminator");
        return <div>
           <h1>Serreminator</h1>
           <Metric session={this.props.session} topic="sensor.lux"/>
        </div>;
  }
});

module.exports = Serreminator;

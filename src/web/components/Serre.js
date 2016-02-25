const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');

const Serre = React.createClass({
    render: function() {
        console.log("Render Serre");
        return <div>
            <div className="col-md-9">
                <Graph {...this.props}/>
            </div>

            <div className="col-md-3">
                <Value {...this.props}/>
            </div>
        </div>;
    }
});

module.exports = Serre;

const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');
const ChildController = require('./ChildController.js');

const opts = {
    topic: "box.temp.value",
    id: "boite",
    PIDtarget: "box.temp.target",
    name: "Température dans la boite",
    unity: "°C",
    PIDsetter: "box.temp.set_target",
    max: 60,
    min: 0
}

const Box = React.createClass({
    getInitialState: function() {
        return {value: 0, target:0};
    },
    componentDidMount: function() {
        this.props.session.subscribe(opts.topic, function(args){
            this.setState({value:args[0]})
        }.bind(this));
        this.props.session.subscribe(opts.PIDtarget, function(args){
            this.setState({target:args[0]})
        }.bind(this));
    },
    render: function() {
        var w = $("#box-col").width();

        var arrow = {
            color: "#b7b7b7",
            width: 5,
            height: w/2,
        }

        var sections = ['#4d55ff', '#3d907f', '#8dc152', '#ffb64d', '#e84428'];


        return <div>
            <div className="col-md-9">
                <Graph {...opts} session={this.props.session}/>
            </div>

            <div className="col-md-3" id="box-col">
                <Value {...opts}
                    session={this.props.session}
                    value={this.state.value}
                    target={this.state.target}/>

                <ChildController session={this.props.session} />
            </div>
        </div>;
    }
});

module.exports = Box;

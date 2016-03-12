const React = require("react");
const Graph = require('./Graph.js');
const Value = require('./Value.js');
const SimpleValue = require('./SimpleValue.js');

const opts = {
    topic: "house.light.value",
    id: "serre",
    PIDtarget: "house.light.target",
    name: "Luminosité dans la serre",
    unity: "Lux",
    PIDsetter: "house.light.set_target",
    max: 900,
    min: 0
}

const Serre = React.createClass({
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
        console.log("Render Serre");
        return <div>
            <div className="col-md-9">
                <Graph {...opts} session={this.props.session}/>
            </div>

            <div className="col-md-3">
                <Value {...opts}
                    session={this.props.session}
                    value={this.state.value}
                    target={this.state.target}/>
                <br/>
                <SimpleValue
                    session={this.props.session}
                    topic={'house.ground_humidity.value'}
                    unity={'%'}
                    name={'Humidité du sol'} />
                <SimpleValue
                    session={this.props.session}
                    topic={'house.temp.value'}
                    unity={'°C'}
                    name={'Température de l\'air'}
                    target={20}/>
            </div>
        </div>;
    }
});

module.exports = Serre;



const React = require("react");
const rd3 = require('react-d3');
const LineChart = rd3.LineChart;

const Metric = React.createClass({
    getInitialState: function() {
        return {lineData: [0]};
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.addData(args[0]);
        }.bind(this));
    },
    addData: function(data_point){
        var newdata = this.state.lineData.concat([data_point])
        this.setState({lineData: newdata});
    },
    render: function() {
        var lineData = this.state.lineData.map(function(item, i){
            return {
                x: i,
                y: item
            }
        }.bind(this));
        if(lineData.length > 50){
            lineData = lineData.slice(-50);
        }
        var data = [{
            name: "plop",
            values: lineData
        },
        {
            name: "plop2",
            values: [
                {
                    x: lineData[0]['x'],
                    y: 800
                },
                {
                    x: lineData.slice(-1)[0]['x'],
                    y: 800
                }
            ]
        },
        {
            name: "zero",
            values: [
                {
                    x: lineData[0]['x'],
                    y: 0
                },
                {
                    x: lineData[0]['x'],
                    y: 1200
                }
            ]
        }];
        return <div className="row">
            <h2 className="col-md-12">{this.props.topic}</h2>
            <div className="col-md-6">
                <h2>Valeur actuelle: <strong>{this.state.lineData.slice(-1)[0]}</strong></h2>
                <LineChart
                    data={data}
                    height={600}
                    width={600}
                    yAxisLabel="Luminosité (Lux)"
                    xAxisLabel="Temps"
                    gridHorizontal={true} />
            </div>
        </div>;
    }
});

module.exports = Metric;

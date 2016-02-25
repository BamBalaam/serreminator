const React = require("react");
const rd3 = require('react-d3');
const LineChart = rd3.LineChart;

const Graph = React.createClass({
    getInitialState: function() {
        return {lineData: [0], target:0, linewidth:600};
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.addData(args[0]);
        }.bind(this));
        this.props.session.subscribe(this.props.PIDtarget, function(args){
            this.setState({lineData:this.state.lineData, target:args[0]});
        }.bind(this));
        var w = $("#" + this.props.topic.replace(".","-") + "-linechart").width();
        this.setState({linewidth:w});
    },
    addData: function(data_point){
        var newdata = this.state.lineData.concat([data_point])
        this.setState({lineData: newdata, target:this.state.target});
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
                    y: this.state.target
                },
                {
                    x: lineData.slice(-1)[0]['x'],
                    y: this.state.target
                }
            ]
        },
        {
            name: "zero",
            values: [
                {
                    x: lineData[0]['x'],
                    y: this.props.min
                },
                {
                    x: lineData[0]['x'],
                    y: this.props.max
                }
            ]
        }];
        return <div className="row">
            <h2 className="col-md-12">{this.props.name}</h2>
            <div className="col-md-12" id={this.props.topic.replace(".", "-") + "-linechart"}>
                <LineChart
                    data={data}
                    height={600}
                    width={this.state.linewidth}
                    yAxisLabel={this.props.name + " en " + this.props.unity}
                    xAxisLabel="Temps"
                    gridHorizontal={true} />
            </div>
        </div>;
    }
});

module.exports = Graph;

const React = require("react");
const rd3 = require('react-d3');
const LineChart = rd3.LineChart;

const Graph = React.createClass({
    getInitialState: function() {
        return {
            lineData: [{x:0,y:0}],
            target:0,
            i:0
        };
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.addData(args[0]);
        }.bind(this));
        this.props.session.subscribe(this.props.PIDtarget, function(args){
            this.setState({target:args[0]});
        }.bind(this));
    },
    addData: function(data_point){
        var newdata = this.state.lineData.slice(); // copy the array
        var i = this.state.i + 1;
        newdata.push({x:i, y:data_point});
        console.log(newdata);
        if(newdata.length > 50){
            newdata.shift()
        }

        this.setState({
            lineData: newdata,
            i: i
        });
    },
    render: function() {
        var lineData = this.state.lineData;
        var data = [{
            name: "plop",
            values: lineData
        },
        {
            name: "plop2",
            strokeDashArray: "5,5",
            strokeWidth: 3,
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
        var w = $("#" + this.props.topic.replace(".","-") + "-linechart").width();

        return <div className="row">
            <h2 className="col-md-12">{this.props.name}</h2>
            <div className="col-md-12" id={this.props.topic.replace(".", "-") + "-linechart"}>
                <LineChart
                    data={data}
                    height={600}
                    width={w}
                    yAxisLabel={this.props.name + " en " + this.props.unity}
                    xAxisLabel="Temps"
                    gridHorizontal={true} />
            </div>
        </div>;
    }
});

module.exports = Graph;

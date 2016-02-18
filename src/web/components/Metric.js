const Metric = React.createClass({
    getInitialState: function() {
        return {lineData: []};
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.addData(args[0]);
        }.bind(this));
    },
    addData: function(data_point){
        console.log("newdata");

        // newdata = this.state.lineData;
        console.log("newdata2");

        newdata.push(data_point);
        console.log("newdata3");

        this.setState({lineData: newdata});
        console.log("newdata4");

    },
    render: function() {
       return <div>
          <h2>{this.props.topic}</h2>
       </div>;
    }
});

module.exports = Metric;

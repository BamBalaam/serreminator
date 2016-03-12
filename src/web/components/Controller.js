const React = require("react");


const Controller = React.createClass({
    getInitialState: function(){
        return {pressed: false};
    },
    mouseDown: function(){
        this.setState({pressed: true});
        this.props.session.call(this.props.topic, [true]);
    },
    mouseUp: function(){
        this.setState({pressed: false});
        this.props.session.call(this.props.topic, [false]);
    },
    componentDidMount: function(){

    },
    render: function() {
        var type = "btn-success";
        if(!this.props.is_manual){
            type = "";
        }
        else if(this.state.pressed){
            type = "btn-warning";
        }

        return <button
            className={"btn btn-block " + type}
            disabled={this.props.is_manual ? "" : "disabled"}
            onMouseUp={this.mouseUp}
            onMouseDown={this.mouseDown}>
            {this.props.name}
        </button>
    }
});

module.exports = Controller;

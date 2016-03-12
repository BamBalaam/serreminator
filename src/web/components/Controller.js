const React = require("react");


const Controller = React.createClass({
    mouseDown: function(){
        this.props.session.call(this.props.topic, [true]);
    },
    mouseUp: function(){
        this.props.session.call(this.props.topic, [false]);
    },
    componentDidMount: function(){

    },
    render: function() {
        return <button
            className="btn btn-success btn-block"
            disabled={this.props.is_manual ? "" : "disabled"}
            onMouseUp={this.mouseUp}
            onMouseDown={this.mouseDown}>
            {this.props.name}
        </button>
    }
});

module.exports = Controller;

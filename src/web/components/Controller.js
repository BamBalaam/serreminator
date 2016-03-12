const React = require("react");


const Controller = React.createClass({
    render: function() {
        return <button className="btn btn-success btn-block" disabled={this.props.disabled ? "disabled" : ""}>
            {this.props.name}
        </button>
    }
});

module.exports = Controller;

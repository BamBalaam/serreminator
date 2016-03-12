const React = require("react");


const ToggleController = React.createClass({
    render: function() {
        return <div className="btn-group btn-group-justified">
            <div className="btn-group">
                <button
                    className={this.props.is_manual ? "btn btn-primary" : "btn btn-default"}
                    onClick={this.props.set_manual}>ON</button>
            </div>
            <div className="btn-group">
                <button
                    className={this.props.is_manual ? "btn btn-default" : "btn btn-primary"}
                    onClick={this.props.set_auto}>OFF</button>
            </div>
        </div>
    }
});

module.exports = ToggleController;

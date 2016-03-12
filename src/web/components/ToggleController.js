const React = require("react");


const ToggleController = React.createClass({
    render: function() {
        return <div className="btn-group btn-group-justified">
            <div className="btn-group">
                <button
                    className={this.props.disabled ? "btn btn-default" : "btn btn-primary"}
                    onClick={this.props.enable}>ON</button>
            </div>
            <div className="btn-group">
                <button
                    className={this.props.disabled ? "btn btn-primary" : "btn btn-default"}
                    onClick={this.props.disable}>OFF</button>
            </div>
        </div>
    }
});

module.exports = ToggleController;

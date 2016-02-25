const React = require("react");

const Value= React.createClass({
    getInitialState: function() {
        return {value: 0, target:0};
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.setState({value:args[0], target:this.state.target})
        }.bind(this));
        this.props.session.subscribe(this.props.PIDtarget, function(args){
            this.setState({target:args[0], value:this.state.value})
        }.bind(this));
    },
    render: function() {
        return <div>
            <div className="alert alert-info" role="alert">
            Valeur actuelle : <strong>{this.state.value} {this.props.unity}</strong>
            <span className="text-muted">(idéal : {this.state.target} {this.props.unity})</span>
            </div>
            <form className="form-horizontal">
            <div className="input-group">
                <input type="text" className="form-control" id="exampleInputAmount" placeholder="Consigne"/>
                <span className="input-group-btn">
                    <button type="submit" className="btn btn-primary">Set</button>
                </span>
            </div>
            </form>
            </div>;
    }
})

module.exports = Value;

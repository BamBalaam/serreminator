const React = require("react");

const Value= React.createClass({
    getInitialState: function() {
        return {value: 0};
    },
    componentDidMount: function() {
        this.props.session.subscribe(this.props.topic, function(args){
            this.setState({value:args[0]})
        }.bind(this));
    },
    render: function() {
        var t = "";
        if(this.props.target !== undefined){
            t = <span className="text-muted">
                    <br/>
                    (Idéal : <strong>
                        {this.props.target}{this.props.unity}</strong>
                    )
                </span>;
        }

        return <div className="alert alert-info text-center" role="alert">
                {this.props.name} : <strong>{this.state.value} {this.props.unity}</strong> {t}
            </div>;
    }
})

module.exports = Value;

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
    senddata: function(){
        input = $("#"+this.props.topic.replace(".","-")+"-inputval");
        var value = parseInt(input.val());
        if(value > 0){
            console.log(value);
            this.props.session.call(this.props.PIDsetter,[value])
            input.val('');
        }
    },
    handleKeyPress: function(e){
        if (e.key === 'Enter') {
            this.senddata();
        }
    },
    render: function() {
        return <div>
            <br/>
            <div className="alert alert-info" role="alert">
            Valeur actuelle : <strong>{this.state.value} {this.props.unity}</strong>
            <span className="text-muted"><br/>(Idéal : {this.state.target} {this.props.unity})</span>
            </div>
            <div className="input-group">
                <input
                    onKeyPress={this.handleKeyPress}
                    type="number"
                    className="form-control"
                    id={this.props.topic.replace(".","-")+"-inputval"}
                    placeholder="Consigne"/>
                <span className="input-group-btn">
                    <button
                        onClick={this.senddata}
                        id={this.props.topic.replace(".","-")+"-changebuttun"}
                        className="btn btn-primary">
                        Changer
                    </button>
                </span>
            </div>
            </div>;
    }
})

module.exports = Value;

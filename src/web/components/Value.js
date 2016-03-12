String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};


const React = require("react");

const Value= React.createClass({
    senddata: function(){
        input = $("#"+this.props.topic.replaceAll(".","-")+"-inputval");
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
                <div className="alert alert-success text-center" role="alert">
                    Valeur actuelle :<h1><strong>{this.props.value} {this.props.unity}</strong></h1>
                    <span className="text-muted">(Idéal : <strong>{this.props.target} {this.props.unity}</strong>)</span>
                    <p className="text-muted"><br/>Changez la valeur désirée :</p>
                    <div className="input-group">
                        <input
                            onKeyPress={this.handleKeyPress}
                            type="number"
                            className="form-control"
                            id={this.props.topic.replaceAll(".","-")+"-inputval"}
                            placeholder="Consigne"/>
                        <span className="input-group-btn">
                            <button
                                onClick={this.senddata}
                                id={this.props.topic.replaceAll(".","-")+"-changebuttun"}
                                className="btn btn-primary">
                                Changer
                            </button>
                        </span>
                    </div>
                </div>
            </div>;
    }
})

module.exports = Value;

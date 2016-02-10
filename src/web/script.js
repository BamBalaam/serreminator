var App = React.createClass({
   render: function() {
        console.log("Render App");
        return <div>
           <h1>Serrminator</h1>
           <Metric session={this.props.session} topic="sensor.lux"/>
        </div>;
  }
});

var Metric = React.createClass({
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


$(document).ready(function(){
    var connection = new autobahn.Connection({
        url: 'ws://localhost:8080/ws',
        realm: 'realm1'
    });

    connection.onopen = function(session){
        console.log("Connected to ws://localhost:8080/ws !");
        ReactDOM.render(<App session={session} />, document.getElementById('root'));
    };
    connection.open();
});

import React, { Component } from 'react';
import './App.css';
import { Button } from 'react-bootstrap';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';


var self = undefined

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      ip_address: '',
      ws: undefined,
      move: undefined
    };
  }

  componentDidMount(){
    this.connectToWS('192.168.25.3')
  }

  handleIpAdrressChange(e){
    this.setState({ip_address: e.target.value});
    console.log(this.state.ip_address)
  }

  handlePressEnter(e){
    if (e.key === 'Enter') {
      this.connectToWS(this.state.ip_address)
    }
  }

  connectToWS(ip_address){
    var ws = new WebSocket(`ws://${ip_address}:8000`);
    ws.onopen = () => {
      // connection opened
      ws.send('Remote activated'); // send a message
      this.setState( {ws: ws} )
      self = this
      this.loopInput()
    };
    ws.onclose = (e) => {
      // this.showAlert('Error', 'Não foi possível se conectar com o veículo.')
      console.log(e.code, e.reason);
      this.setState( {ws: undefined} )
    };
  }

  movePiece(move){
    this.state.ws.send(`input,${move}`)
  }

  leftDown(e){
    this.setState({move: 'left'})
  }

  leftUp(e){
    this.setState({move: undefined})
  }

  rightDown(e){
    this.setState({move: 'right'})
  }

  rightUp(e){
    this.setState({move: undefined})
  }
  
  loopInput(){

    if (self.state.move){
      self.movePiece(self.state.move)
    }

    if (self.state.ws){
      setTimeout(self.loopInput, 150)
    }
  }

  
  renderButtons(){
    return (

      <div className="App">
        <header className="App-header">

          {/* <div className="container"> */}
          <div style={{display: 'flex', justifyContent: 'center'}}>
              <div className="row" >
                <Button 
                  bsStyle="primary"
                  onMouseDown={(e) => this.leftDown() }
                  onMouseUp={(e) => this.leftUp() }
                  style={{display: 'flex', padding:30, margin:30}}
                > {'   <   '}  </Button>
                <br/>
                <Button 
                  bsStyle="primary"
                  onMouseDown={(e) => this.rightDown() }
                  onMouseUp={(e) => this.rightUp() }
                  style={{display: 'flex', padding:30, margin:30}}
                > {'   >   '} </Button>
              </div>
          </div>

        </header>
      </div>
    )
  }

  renderConnectButton(){
    return (<div className="App">
    <header className="App-header">

    <form>
      <input 
        type="text" 
        name="ip_adress" 
        placeholder="192.168.1.2" 
        onChange={(txt) => this.handleIpAdrressChange(txt) } 
        onKeyPress={this.handlePressEnter}
      />
      <button 
        type="button" 
        onClick={ () => this.connectToWS(this.state.ip_address) }
      > Connect </button>
    </form>
      
    </header>
  </div>)
  }

  render() {

    var current = this.state.ws ? this.renderButtons() : this.renderConnectButton()
    return (

      <div>
        <meta 
          name='viewport'
          content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' 
        />
        {current}
      </div>
    );
  }
}



export default App;

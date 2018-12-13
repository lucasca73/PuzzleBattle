import React, { Component } from 'react';
import './App.css';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      ip_address: '',
      ws: undefined
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

  renderButtons(){
    return (

      <div className="App">
        <header className="App-header">

          <div className="container">
              <div className="row">
                <button 
                  type="button" 
                  onClick={ () => this.movePiece('left') }
                > {'   <   '}  </button>
                <button 
                  type="button" 
                  onClick={ () => this.movePiece('right') }
                > {'   >   '} </button>
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
    console.log(this.state.ws ? 'is connected!' : 'is not connected...')
    return (
      <div>
        {current}
      </div>
    );
  }
}

export default App;

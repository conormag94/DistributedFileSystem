import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

class App extends Component {
  constructor() {
    super()
    this.state = {
        files: []
    }
  }
  componentDidMount() {
      this.getFiles();
  }
  getFiles() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/files`)
    .then((res) => { this.setState({ files: res.data.files }); })
    .catch((err) => { console.log(err); })
  }
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <br/>
            <h1>All of the Files</h1>
            <hr/><br/>
            {
                this.state.files.map((file) => {
                return <h4 key={file.id} className="well"><strong>{ file.name }</strong> - { file.content }</h4>
                })
            }
          </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);

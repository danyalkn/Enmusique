import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

// In  <Route path='/room/:roomCode' component={Room} /> we use : to denote a variable

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
      // have to add
    return (<Router>
        
        <Switch>
            <Route exact path='/'><p>This is home page</p></Route>
            <Route path='/join' component={RoomJoinPage} />
            <Route path='/create' component={CreateRoomPage} />
            <Route path='/room/:roomCode' component={Room} />
        </Switch>
    </Router>);
  }
}

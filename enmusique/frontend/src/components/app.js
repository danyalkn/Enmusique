import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
    // need to have a parent element
    <div>
      <HomePage />
    </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
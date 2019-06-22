/*  PARENT COMPONENT: App.js
 *  DESCRIPTION: Main page for user
 *
 *
 */

import React, { Component } from "react";
import Header from "./homepage/Header";
import PostHeader from "./homepage/PostHeader";
import MainBody from "./homepage/MainBody";

export class Homepage extends Component {
  static propTypes = {};

  render() {
    return (
      <div>
        <Header />
        <PostHeader queryUser="eseisaki" />
        <MainBody />
      </div>
    );
  }
}

export default Homepage;

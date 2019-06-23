/*  PARENT COMPONENT: App.js
 *  DESCRIPTION: Main page for user
 *
 *
 */

import React, { Component } from "react";
import Header from "./homepage/Header";
import PostHeader from "./homepage/PostHeader";
import MainBody from "./homepage/MainBody";
import queryString from "query-string";

export class Homepage extends Component {
  static propTypes = {};

  render() {
    let url = this.props.location.search;
    let params = queryString.parse(url);
    return (
      <div>
        <Header />
        <PostHeader queryUser={params} />
        <MainBody queryUser={params} />
      </div>
    );
  }
}

export default Homepage;

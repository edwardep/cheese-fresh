/*  PARENT COMPONENT: Homepage.js
 *  DESCRIPTION: Header with logo and account,logout buttons (NOT responsive).
 *
 *
 */
import React, { Component } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import logo from "../images/fullogo.png";
import IconButton from "@material-ui/core/IconButton";
import FaceIcon from "@material-ui/icons/Face";
import ExitIcon from "@material-ui/icons/ExitToApp";
import Grid from "@material-ui/core/Grid";
import { logout } from "../../axios/Get";
import { withRouter } from "react-router-dom";

/************************************************************************************************/
/* JSX-STYLE */
const styles = theme => ({
  root: { backgroundColor: "#990033" },
  imglogo: { width: 200, marginLeft: "80px" },
  buttons: { marginRight: "80px" }
});
/************************************************************************************************/
export class Header extends Component {
  /************************************************************************************************/
  /* FUNCTIONS */

  /*RETURNS: nothing
   *DESCRIPTION:  Informs the backend for logout and redirect to login page.
   *
   */
  handleLogout = () => {
    let response = logout();

    if (response) {
      this.props.history.push("/");
    } else {
      alert("Server error");
    }
  };
  /*RETURNS: nothing
   *DESCRIPTION:  Redirects to homepage of current user.
   *
   */
  handleGoToProfile = () => {
    // var current_user = jwt.decode(localStorage.getItem("jwt_token"), {
    //   complete: true
    // }).payload["identity"];
    let current_user = "temp_user";
    this.props.history.push("/homepage?user=" + current_user);
  };

  /************************************************************************************************/
  render() {
    const { classes } = this.props;
    return (
      <header>
        <AppBar className={classes.root} position="static">
          <Toolbar>
            <Grid container justify="space-between">
              {/*container with cheese logo*/}
              <Grid item>
                <img src={logo} alt="logo" className={classes.imglogo} />
              </Grid>
              {/*container with account, logout buttons*/}
              <Grid item className={classes.buttons}>
                <IconButton
                  aria-label="menu"
                  color="inherit"
                  onClick={this.handleGoToProfile}
                >
                  <FaceIcon />
                </IconButton>

                <IconButton
                  aria-label="menu"
                  color="inherit"
                  onClick={this.handleLogout}
                >
                  <ExitIcon />
                </IconButton>
              </Grid>
            </Grid>
          </Toolbar>
        </AppBar>
      </header>
    );
  }
}

export default withRouter(withStyles(styles)(Header));

/*  PARENT COMPONENT: Homepage.js
 *  DESCRIPTION:Includes profile picture, edit profile choice
 *              and basic informations about user.
 *
 */
import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";
import { public_profile } from "../../axios/Get";
import PropTypes from "prop-types";
import Avatar from "@material-ui/core/Avatar";
import Fab from "@material-ui/core/Fab";
import EditIcon from "@material-ui/icons/Edit";
import FriendIcon from "@material-ui/icons/PersonAdd";
import Button from "@material-ui/core/Button";
import PopupList from "./mainbody/postheader/PopupList";
import Typography from "@material-ui/core/Typography";
import Dialog from "@material-ui/core/Dialog";
/************************************************************************************************/
/* JSX-STYLE */
const styles = theme => ({
  profileImage: {
    display: "inline-block",
    width: "180px",
    height: "180px",
    margin: 20,
    marginBottom: 0,
    marginLeft: "80px"
  },
  avatar_button: {
    display: "inline-block",
    marginTop: -50,
    marginLeft: -200
  },
  follow_button: {
    width: "60px",
    height: "60px",
    marginTop: 80,
    backgroundColor: "#990033",
    "&:hover": { backgroundColor: "#660022" }
  },
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }
});
/************************************************************************************************/
export class PostHeader extends Component {
  constructor() {
    super();
    this.state = {
      username: null,
      email: null,
      is_stranger: null,
      my_profile: null,
      followers: [],
      following: [],
      followers_num: null,
      following_num: null,
      reg_date: null,
      basicUrl: null,
      following_open: false,
      followers_open: false
    };
  }
  /************************************************************************************************/
  /* FUNCTIONS */

  componentDidMount = () => {
    const query = this.props.queryUser;
    let response = public_profile(query);

    response.then(value => {
      this.setState({
        username: value.username,
        email: value.email,
        is_stranger: value.is_stranger,
        my_profile: value.my_profile,
        followers: value.followers,
        following: value.following,
        followers_num: value.followers_num,
        following_num: value.following_num,
        reg_date: value.reg_date,
        basicUrl: value.profile_image
      });
    });
  };
  /************************************************************************************************/

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Grid container spacing={4}>
          {/*profile picture with edit icon */}
          <Grid item>
            <Avatar
              alt="avatar"
              src={this.state.basicUrl}
              className={classes.profileImage}
            />
            {/*!!!!!!!!!!!!*/}
            {/*need to check if user is looking his own profile */}
            <label htmlFor="upload-file-avatar">
              <input
                id="upload-file-avatar"
                type="file"
                name="file"
                onChange={this.UpdateAvatar}
                style={{ display: "none" }}
              />
              <Fab
                component="span"
                color="default"
                type="submit"
                aria-label="update_avatar"
                className={classes.avatar_button}
              >
                <EditIcon style={{ marginLeft: 18, marginTop: 15 }} />
              </Fab>
            </label>
          </Grid>
          {/*User name */}
          <Grid item>
            <h2>{"John Doe"}</h2>
            <Button onClick={() => this.setState({ followers_open: true })}>
              {this.state.followers_num} Followers
            </Button>
            <Dialog
              className={classes.modal}
              open={this.state.followers_open}
              onClose={() =>
                this.setState({ following_open: false, followers_open: false })
              }
            >
              <PopupList
                list={this.state.followers}
                title="You are following: "
              />
            </Dialog>
            <br />
            <Button onClick={() => this.setState({ following_open: true })}>
              {this.state.following_num} Following
            </Button>

            <Dialog
              className={classes.modal}
              open={this.state.following_open}
              onClose={() =>
                this.setState({ following_open: false, followers_open: false })
              }
            >
              <PopupList
                list={this.state.following}
                title="You are following: "
              />
            </Dialog>
            <br />
            <Typography variant="subtitle2">
              Member since: <br />
              <i>{this.state.reg_date}</i>
            </Typography>
          </Grid>
          {/*!!!!!!!!!!!!*/}
          {/*need to check if user is not following this person */}
          {/*Follow button */}
          <Grid item>
            <Fab
              color="primary"
              aria-label="follow"
              className={classes.follow_button}
              onChange={this.followUser}
            >
              <FriendIcon />
            </Fab>
          </Grid>
        </Grid>
      </div>
    );
  }
}

PostHeader.propTypes = { queryUser: PropTypes.string.isRequired };

export default withRouter(withStyles(styles)(PostHeader));

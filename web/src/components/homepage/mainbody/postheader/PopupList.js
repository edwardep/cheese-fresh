/*  PARENT COMPONENT: PostHeader.js
 *  DESCRIPTION:List with followers and users following.
 *
 */
import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Avatar from "@material-ui/core/Avatar";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import Paper from "@material-ui/core/Paper";
import PersonIcon from "@material-ui/icons/Person";
import AddIcon from "@material-ui/icons/AccountCircleOutlined";
import CheckCircle from "@material-ui/icons/CheckCircleOutline";
import blue from "@material-ui/core/colors/blue";
/************************************************************************************************/
/* JSX-STYLE */
const styles = {
  avatar: {
    backgroundColor: blue[100],
    color: blue[600]
  }
};
/************************************************************************************************/
export class PopupList extends Component {
  render() {
    const { classes, list, title } = this.props;

    return (
      <div>
        <Paper>
          <List>
            <h4>{title} </h4>
            {list.map(user => (
              <ListItem
                button
                onClick={this.handleListItemClick(user.username)}
                key={user}
              >
                <ListItemAvatar>
                  <Avatar className={classes.avatar}>
                    <PersonIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText primary={user.username} />
                <ListItemAvatar>
                  {!user.in_common ? <AddIcon /> : <CheckCircle />}
                </ListItemAvatar>
              </ListItem>
            ))}
          </List>
        </Paper>
      </div>
    );
  }
}

PopupList.propTypes = {
  list: PropTypes.array.isRequired
};

export default withStyles(styles)(PopupList);

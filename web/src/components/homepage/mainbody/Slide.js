/*  PARENT COMPONENT: ImageSlider.js
 *  DESCRIPTION:Each slide contains an image and each comments .
 *
 *
 */
import React, { Component } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Typography from "@material-ui/core/Typography";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import AddCommentIcon from "@material-ui/icons/AddComment";
import IconButton from "@material-ui/core/IconButton";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import PropTypes from "prop-types";
/************************************************************************************************/
/* JSX-STYLE */
const styles = theme => ({
  imagePart: {
    width: "530px",
    margin: "20px"
  },
  commentPart: {
    width: "530px",
    margin: "20px"
  }
});
/************************************************************************************************/
export class Slide extends Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: [
        {
          id: 1,
          author: "Alice",
          text: "Asdsfh dsssgaak skskskska llwwkjrhhwialgh ,dnjhhh eewihohjhd."
        },
        { id: 2, author: "Bob", text: "Akkksjah skskksja." }
      ]
    };
  }
  /************************************************************************************************/
  /* FUNCTIONS */

  /************************************************************************************************/
  render() {
    const { classes, image } = this.props;
    return (
      <div>
        <Grid container justify="center" alignItems="stretch" spacing={0}>
          {/*Fist element of slide is an image*/}
          <Grid item>
            <img src={image.url} alt="slide" className={classes.imagePart} />
          </Grid>
          {/*Second element of slide is a list with comments realated to the image*/}
          <Grid item>
            <List className={classes.root}>
              {this.state.comments.map(comment => (
                <ListItem
                  alignItems="flex-start"
                  className={classes.commentPart}
                  key={comment.id}
                >
                  <Grid container justify="space-around">
                    <Grid item xs={11}>
                      {/*Comment's Author */}
                      <Typography
                        component="span"
                        variant="h6"
                        className={classes.inline}
                        color="textPrimary"
                      >
                        {comment.author}
                      </Typography>
                      {/*Comment's Body */}
                      {"-  "}
                      {comment.text}
                    </Grid>
                    <Grid item xs={1}>
                      {/*Delete comment button */}
                      <IconButton
                        className={classes.deleteComm}
                        /*!!!!!!!!!!!!!!!!!!!!  function deleteComment()*/
                        onClick={() => {}}
                      >
                        <DeleteForeverIcon />
                      </IconButton>
                    </Grid>
                  </Grid>
                </ListItem>
              ))}

              {/*Add a new comment */}
              <ListItem button divider>
                <TextField
                  id="input-with-icon-grid"
                  fullWidth
                  label="Write a comment.."
                  /*!!!!!!!!!!!!!!!!!!!! function addComment()*/
                  onChange={() => {}}
                />
                <Button
                  type="submit"
                  variant="text"
                  autoFocus
                  /*!!!!!!!!!!!!!!!!!!!! function submitComment()*/
                  onClick={() => {}}
                >
                  <AddCommentIcon />
                </Button>
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </div>
    );
  }
}
Slide.propTypes = {
  image: PropTypes.object.isRequired
};

export default withStyles(styles)(Slide);

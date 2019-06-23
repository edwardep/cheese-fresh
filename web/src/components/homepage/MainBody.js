/*  PARENT COMPONENT: HomePage.js
 *  DESCRIPTION:The mainbody of page which contains a gallery bar and displays
 *              images of the selected gallery.
 *
 */
import React, { Component } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Paper from "@material-ui/core/Paper";
import Tabs from "@material-ui/core/Tabs";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Gallery from "./mainbody/Gallery";
import Tab from "@material-ui/core/Tab";
import AddGalleryIcon from "@material-ui/icons/AddToPhotos";
import Button from "@material-ui/core/Button";
import DeleteIcon from "@material-ui/icons/DeleteForever";
import IconButton from "@material-ui/core/IconButton";
import PropTypes from "prop-types";

function TabContainer(props) {
  return (
    <Typography component="div" style={{ padding: 8 * 3 }}>
      {props.children}
    </Typography>
  );
}

/************************************************************************************************/
/* JSX-STYLE */
const styles = theme => ({
  tabs: {
    marginTop: 20,
    marginLeft: "80px",
    marginRight: "80px"
  },
  button: {
    color: "#990033"
  },
  buttonIcon: { marginRight: 3 }
});
/************************************************************************************************/
export class MainBody extends Component {
  constructor(props) {
    super(props);
    this.state = {
      galleries: ["Fish", "Dogs", "Trees", "Cats"],
      my_profile: true,
      index: 0
    };
  }
  /************************************************************************************************/
  /* FUNCTIONS */

  selectGallery = (event, value) => {
    this.setState({ index: value });
  };

  /************************************************************************************************/
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.tabs}>
        <Paper>
          <Grid container justify="space-between" alignItems="center">
            {/*Create new gallery button*/}
            <Grid item>
              <Button
                variant="text"
                color="primary"
                className={classes.button}
                onClick={this.openCreateGallery}
              >
                <AddGalleryIcon className={classes.addGalIcon} />
                Create
              </Button>
            </Grid>

            {/*Gallery name tags */}
            <Grid item>
              <Tabs
                value={this.state.index}
                /*!!!!!!!!!!!!!!!!!!!! function selectGallery()*/
                onChange={this.selectGallery}
                variant="scrollable"
                scrollButtons="auto"
                className={classes.tab}
              >
                {this.state.galleries.map(item => (
                  <Tab label={item} key={item} />
                ))}
              </Tabs>
            </Grid>

            {/*Delete a gallery button*/}
            <Grid item>
              <IconButton
                className={classes.button}
                /*!!!!!!!!!!!!!!!!!!!! function deleteGallery()*/
                onClick={this.deleteIcon}
              >
                <DeleteIcon className={classes.buttonIcon} />
              </IconButton>
            </Grid>
          </Grid>
        </Paper>
        <TabContainer>
          <Gallery
          // images={this.state.images}
          // my_profile={my_profile}
          // gallery_title={queryGalleries[this.state.value]}
          />
        </TabContainer>
      </div>
    );
  }
}

MainBody.propTypes = { queryUser: PropTypes.object.isRequired };

export default withStyles(styles)(MainBody);

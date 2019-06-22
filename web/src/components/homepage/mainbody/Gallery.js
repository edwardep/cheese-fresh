/*  PARENT COMPONENT: MainBody.js
 *  DESCRIPTION:A grid which contains all images of the selected gallery.
 *
 *
 */
import React, { Component } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import Button from "@material-ui/core/Button";
import AddPhotoIcon from "@material-ui/icons/AddAPhoto";
import ImageSlider from "./ImageSlider";
import ClearBtn from "@material-ui/icons/Clear";
import IconButton from "@material-ui/core/IconButton";
import { GridListTileBar } from "@material-ui/core";
import Modal from "@material-ui/core/Modal";
import PropTypes from "prop-types";
/************************************************************************************************/
/* JSX-STYLE */
const styles = theme => ({
  button_container: { width: "100%" },
  upload_button: {
    height: 280
  },
  input: { display: "none" },
  clearTile: {
    background: "transparent"
  },
  clearBtn: {
    color: "white"
  },
  modal: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  }
});
/************************************************************************************************/
export class Gallery extends Component {
  constructor(props) {
    super(props);
    this.state = {
      images: [
        {
          id: 1,
          url: "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/aurora.jpg"
        },
        {
          id: 2,
          url: "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/canyon.jpg"
        },
        {
          id: 3,
          url: "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/city.jpg"
        },
        {
          url: "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/desert.jpg"
        },
        {
          id: 4,
          url:
            "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/mountains.jpg"
        },
        {
          id: 5,
          url: "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/redsky.jpg"
        },
        {
          id: 6,
          url:
            "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/sandy-shores.jpg"
        },
        {
          id: 7,
          url:
            "https://s3.us-east-2.amazonaws.com/dzuz14/thumbnails/tree-of-life.jpg"
        }
      ],
      open: false,
      slide: null
    };
  }
  /************************************************************************************************/
  /* FUNCTIONS */

  /************************************************************************************************/
  render() {
    const { classes } = this.props;
    return (
      <div>
        <GridList cellHeight={280} cols={4}>
          {/*!!!!!!!!!!!!*/}
          {/*need to check if user is looking his own profile */}
          {/* Create a new gallery button.*/}
          <GridListTile key={"000"}>
            <div>
              <label htmlFor="upload-file" className={classes.button_container}>
                <input
                  id="upload-file"
                  type="file"
                  name="file"
                  /*!!!!!!!!!!!!!!!!!!!! function addNewImage()*/
                  onChange={this.addNewImage}
                  className={classes.input}
                />
                <Button
                  component="span"
                  type="submit"
                  className={classes.upload_button}
                  fullWidth
                >
                  <AddPhotoIcon style={{ fontSize: 90 }} />
                </Button>
              </label>
            </div>
          </GridListTile>
          {/* Show all images of gallery in a grid.*/}
          {this.state.images.map(tile => (
            <GridListTile key={tile.url}>
              <img
                src={tile.url}
                alt={tile.url}
                onClick={() => {
                  this.setState({ open: true, slide: tile });
                }}
              />
              {/*!!!!!!!!!!!!*/}
              {/*need to check if user is looking his own profile */}
              {/*Delete image button*/}
              <GridListTileBar
                className={classes.clearTile}
                actionIcon={
                  /*!!!!!!!!!!!!!!!!!!!! function deleteImage()*/
                  <IconButton onClick={() => this.deleteImage(tile.id)}>
                    <ClearBtn className={classes.clearBtn} />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
        {/*A slider in order to view each image seperately.*/}
        <Modal
          className={classes.modal}
          open={this.state.open}
          onClose={() => this.setState({ open: false })}
        >
          <ImageSlider
            images={this.state.images}
            index={this.state.images.indexOf(this.state.slide)}
          />
        </Modal>
      </div>
    );
  }
}

Gallery.propTypes = { images: PropTypes.array, my_profile: PropTypes.object };

export default withStyles(styles)(Gallery);

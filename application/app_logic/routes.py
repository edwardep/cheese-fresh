from flask_restful import Api
from flask import Blueprint

from . import resources

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

api.add_resource(resources.index, '/')

# GET
api.add_resource(resources.GetPublicProfile, '/public_profile')
# api.add_resource(resources.GetGalleries, '/list_galleries')
# api.add_resource(resources.GalleryPhotos, '/gallery_photos')
# api.add_resource(resources.GetComments, '/comments')

# # POST
# api.add_resource(resources.AddProfilePicture, '/profile_picture')
# api.add_resource(resources.Follow, '/follow')
# api.add_resource(resources.AddGallery, '/add_gallery')
# api.add_resource(resources.AddComment, '/add_comment')
api.add_resource(resources.AddImage, '/add_image')

# # UPDATE
# api.add_resource(resources.UpdateUser, '/update_user')

# # DELETE
# api.add_resource(resources.DeleteGallery, '/delete_gallery')
# api.add_resource(resources.DeleteImage, '/delete_image')
# api.add_resource(resources.DeleteComment, '/delete_comment')

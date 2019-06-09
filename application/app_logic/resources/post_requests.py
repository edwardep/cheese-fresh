from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..data.users import User
from ..data.galleries import Gallery
from ..data.images import Image
from ..data.comments import Comment
import uuid
import requests
from .. import STORAGE_HOST

'''
# ------------------------CONTENTS-----------------------------
# _______________________AddProfilePicture(/profile_picture)___
# _______________________AddGallery(/add_gallery)______________
# _______________________AddComment (/comment)_________________
# _______________________AddImage(/add_image)________________
'''


# Used when we want to add or change profile pic
class AddProfilePicture(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        me = User.objects(username=current_user).first()

        if 'file' not in request.files:
            return make_response(jsonify('BAD'), 400)
        file = request.files['file']

        if file.filename == '':
            return make_response(jsonify('BAD'), 400)

        if not file or not allowed_file(file.filename):
            return make_response(jsonify('BAD'), 400)

        my_string = file.filename
        idx = my_string.index('.')
        filename = secure_filename(my_string[:idx] + '_' + uuid.uuid4().hex +
                                   my_string[idx:])

        location = '/uploads/' + filename
        me.profile_image = location
        me.save()

        sendFile = {"file": (filename, file.stream, file.mimetype)}

        try:
            requests.post(STORAGE_HOST + '/post_image', files=sendFile)
        except:
            return make_response(jsonify('storage_error'), 500)

        return make_response(jsonify('OK'), 201)

# Used when we want to follow a user/doesn't return anything
class Follow(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        to_follow = request.json['username']
        friend = User.objects(username=to_follow).first()
        me = User.objects(username=current_user).first()
        # make sure its not me or its not already in my following list
        if to_follow in me.following or to_follow == current_user:
            output = jsonify("You can't follow this user")
            return make_response(output, 406)  # 406 not accepted

        friend.followers.append(current_user)
        friend.save()
        me.following.append(to_follow)
        me.save()
        return make_response(jsonify('DONE'), 201)

#Used to create a new gallery / returns--> gallery info
class AddGallery(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        gallery = Gallery()
        title = request.json['gallery_title']


        if not title or title == '':
            title = "Gallery"

        user = User.objects(username=current_user).first()
        len_title = len(title)

        for emb_gallery in user.galleries:
            if emb_gallery.title == title and len(emb_gallery.title) == len_title:
                title = title + '(1)'
            elif emb_gallery.title[-3] == "(" and emb_gallery.title[
                    -1] == ")" and emb_gallery.title[:-3] == title:
                s = list(emb_gallery.title)
                i = int(emb_gallery.title[-2]) + 1
                s[-2] = str(i)
                title = "".join(s)

        gallery.title = title
        gallery.owner = current_user
        user.galleries.insert(0, gallery)
        user.save()
        return make_response(jsonify("OK"), 201)

# Used to add pictures in a gallery/ needs storage service to be successful
class AddImage(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        flag = False
        g_title = request.args.get('gallery_title')
        me = User.objects(username=current_user).first()
        for emb_gallery in me.galleries:
            if emb_gallery.title == g_title:
                flag = True
                break
        if not flag:
            return make_response(jsonify('gallery_not_found'), 404)

        if 'file' not in request.files:
            return make_response(jsonify('file_type'), 400)
        file = request.files['file']

        if file.filename == '':
            return make_response(jsonify('file_name_empty'), 400)

        if not file or not allowed_file(file.filename):
            return make_response(jsonify('file_extension'), 400)

        my_string = file.filename
        idx = my_string.index('.')
        filename = secure_filename(my_string[:idx] + '_' + uuid.uuid4().hex +
                                   my_string[idx:])
        image = Image()
        image.path = '/uploads/' + filename
        image.owner = current_user
        image.save()
        image.iid = str(image.id)
        image.save()
        emb_gallery.images.insert(0, image.iid)
        me.save()

        output = "OK"
        sendFile = {"file": (filename, file.stream, file.mimetype)}

        try:
            requests.post(STORAGE_HOST + '/post_image', files=sendFile)
        except:
            return make_response(jsonify('storage_error'), 500)

        return make_response(jsonify(output), 201)

# Add comment to a specific photo ---> returns 404,403 or 201
class AddComment(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        comment = Comment()
        image_id = request.json['image_id']
        text = request.json['text']
        comment_id = uuid.uuid4().hex
        image = Image.objects(iid=image_id).first()

        if not image:
            output= "Image doesn't exists"
            return make_response(jsonify(output), 404)

        user = User.objects(username=current_user).first()
        if image.owner not in user.following and current_user != image.owner:
            output = "Not allowed!"
            return make_response(jsonify(output), 403)

        comment.owner = current_user
        comment.text = text
        comment._id = comment_id
        image.comments.append(comment)
        image.save()
        output = "OK"

        return make_response(jsonify(output), 201)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


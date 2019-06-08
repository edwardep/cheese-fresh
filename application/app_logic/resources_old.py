from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from .data.users import User
from .data.galleries import Gallery
from .data.images import Image
import uuid
import requests
from . import STORAGE_HOST


class index(Resource):
    def get(self):
        return "Hello from ~Application"


class GetPublicProfile(Resource):
    @jwt_required
    def get(self):
        is_stranger = False
        my_profile = False
        following_list = []
        followers_list = []
        user_name = request.args.get('user')
        current_user = get_jwt_identity()
        user = User.objects(username=user_name).first()
        me = User.objects(username=current_user).first()
        if current_user != user_name and user_name not in me.following:
            is_stranger = True

        if current_user == user_name:
            my_profile = True

        for f in user.following:
            follow = FollowObj()
            follow.in_common = False
            follower = User.objects(username=f).first()
            if f in me.following:
                follow.in_common = True
            if f != current_user and f != user_name:
                follow.username = f
                follow.profile_image = follower.profile_image
                following_list.append(follow)
        for f in user.followers:
            follow = FollowObj()
            follow.in_common = False
            follower = User.objects(username=f).first()
            if f in me.following:
                follow.in_common = True
            if f != current_user and f != user_name:
                follow.username = f
                follow.profile_image = follower.profile_image
                followers_list.append(follow)

        output = {
            'username': user.username,
            'reg_date': user.registered_date,
            'is_stranger': is_stranger,
            'my_profile': my_profile,
            'following': following_list,
            'followers': followers_list,
            'followers_num': len(user.followers),
            'following_num': len(user.following),
            'profile_image': user.profile_image
        }
        return make_response(jsonify(output), 200)


class AddGallery(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        gallery = Gallery()
        title = request.json['title']

        # Validation??
        if not title or title == '':
            title = "Gallery"

        print(title)
        user = User.objects(username=current_user).first()
        len_title = len(title)

        for n in user.galleries:
            if n.title == title and len(n.title) == len_title:
                title = title + '(1)'
            elif n.title[-3] == "(" and n.title[
                    -1] == ")" and n.title[:-3] == title:
                s = list(n.title)
                i = int(n.title[-2]) + 1
                s[-2] = str(i)
                title = "".join(s)

        gallery.title = title
        gallery.owner = current_user
        user.galleries.insert(0, gallery)
        user.save()
        output = {
            'title': gallery.title,
            'owner': gallery.owner,
            'date': gallery.registered_date,
            'images': gallery.images
        }
        return make_response(jsonify({'result': output}), 201)


class AddImage(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        flag = False
        g_title = request.args.get('title')
        user = User.objects(username=current_user).first()
        for g in user.galleries:
            if g.title == g_title:
                flag = True
                break
        if not flag:
            output = "There is no such gallery for user "
            return make_response(jsonify(output), 404)
        # #description = request.json['description']
        description = 'My panda'

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
        image.description = description
        image.save()
        image.iid = str(image.id)
        image.save()
        g.images.insert(0, image.iid)
        user.save()

        output = {
            'id': image.iid,
            'path': image.path,
            'owner': image.owner,
            'date': image.registered_date,
            'description': image.description,
            'comments': image.comments
        }
        sendFile = {"file": (filename, file.stream, file.mimetype)}

        try:
            requests.post(STORAGE_HOST + '/post_image', files=sendFile)
        except:
            return make_response(jsonify('storage_error'), 500)
        # requests.post(zk_get_addr(storage_servers[0]) + '/post_image',
        #               files=sendFile)
        # time.sleep(1)
        # file.seek(0)
        # sendFile = {"file": (filename, file.stream, file.mimetype)}
        # requests.post(zk_get_addr(storage_servers[1]) + '/post_image',
        #               files=sendFile)
        return make_response(jsonify(output), 201)


class GalleryPhotos(Resource):
    @jwt_required
    def get(self):
        user_name = request.args.get('user')
        gallery_title = request.args.get('gallery')

        current_user = get_jwt_identity()
        me = User.objects(username=current_user).first()
        output = []
        if user_name not in me.following and user_name != current_user:
            output = "Oooops user doesn't exists!"
            return make_response(jsonify({'result': output}), 404)
        user = User.objects(username=user_name).first()
        try:
            gallery = user.galleries.get(title=gallery_title)
        except:
            gallery = None

        if gallery is None:
            output = "Gallery doesn't exists!!"
            return make_response(jsonify({'result': output}), 404)

        for image_id in gallery.images:
            image = Image.objects(iid=image_id).first()
            if zk_from_storage(image.storage[0]):
                location = zk_get_addr(image.storage[0])
            elif zk_from_storage(image.storage[1]):
                location = zk_get_addr(image.storage[1])
            else:
                location = "server_down"

            output.append({
                'id': image.iid,
                'path': 'http:172.24.0.43:4003' + image.path,
                'owner': image.owner,
                'date': image.registered_date,
                'description': image.description,
                'comments': image.comments
            })
        return make_response(jsonify(output), 200)

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     response.headers[
#         'Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
#     response.headers[
#         'Access-Control-Allow-Headers'] = 'Access-Control-Allow-Origin'
#     response.headers[
#         'Access-Control-Expose-Headers'] = 'Authorization, Headers, error'
#     response.headers['Content-Type'] = 'application/json, multipart/form-data'

#     return response


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

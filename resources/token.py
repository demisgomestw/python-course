from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource


class TokenResource(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}

from flask import jsonify,request,current_app,url_for
from . import api 
from .. import db
from ..models import Post,Permission,Comment
from .decorators import permission_required


@api.route("/comments")
def fetch_comments():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
            page,
            per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False
    )

    comments = pagination.items
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': None,
        'next': None,
        'count': pagination.total
        })


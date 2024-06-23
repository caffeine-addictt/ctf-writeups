import time
import secrets
from typing import Optional, cast
from werkzeug.exceptions import Forbidden
from flask import current_app as app, flash, session
from flask import render_template, request, make_response

from ..models import CroissantReview, save


ENDPOINT: str = f"/api/{secrets.token_urlsafe(64)}"
COOKIES: dict[str, float] = {}


def set_token() -> str:
    session["token"] = gen_token()
    session["token_exp"] = time.time() + 60  # 1 minute
    return session["token"]


def gen_token() -> str:
    return secrets.token_urlsafe()


def validate_token(with_check: bool = True) -> Optional[str]:
    token = request.headers.get("X-Token")

    if with_check and (not token or token != session.get("token")):
        raise Forbidden("Invalid token")

    session.pop("token", None)
    session.pop("token_exp", None)

    return token


@app.before_request
def before_request():
    if "token" not in session or session.get("token_exp", 0) < time.time():
        set_token()


@app.route("/", methods=["GET", "POST"])
def root():
    reviews: list[CroissantReview] = CroissantReview.query.all()

    if request.method == "POST":
        try:
            rating = request.form.get("rating")
            comment = request.form.get("comment")

            if not rating:
                raise Exception("Rating is required")
            if not comment:
                raise Exception("Comment is required")
            if not (1 <= int(rating) <= 5):
                raise Exception("Rating must be a number between 1 and 5")

            newReview = CroissantReview(
                rating=int(rating),
                comment=cast(str, comment).replace("endpoint", ENDPOINT, 1),
            )
            reviews.append(newReview)
            save(newReview)

            set_token()

        except Exception as e:
            app.logger.error(e)
            flash(f"Failed to add review: {e}", "error")

    resp = make_response(
        render_template("index.html", reviews=reviews, token=session["token"])
    )

    cookie = secrets.token_hex(64)
    COOKIES[cookie] = time.time() + 60
    resp.set_cookie("cookie", cookie)

    return resp


@app.get(ENDPOINT)
def get_flag():
    if "cookie" not in request.cookies:
        return {
            "message": "Hey!! What about my chocolate chip cookies?!",
            "status": 403,
        }, 403

    validate_token()
    return FLAG

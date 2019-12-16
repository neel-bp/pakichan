import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db
from flaskblog.forms import (PostForm, SubPostForm)
from flaskblog.models import Post, SubPost


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    thread_id = post_id
    post = Post.query.get_or_404(post_id)
    subposts = SubPost.query.filter(SubPost.post_id == thread_id).all()
    return render_template('post.html', title=post.title, post=post, subposts=subposts)


# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')


# @app.route("/post/<int:post_id>/delete", methods=['POST'])
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     SubPost.query.filter(SubPost.post_id == post_id).delete(synchronize_session=False)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('home'))

@app.route("/post/<int:post_id>/subpost/new", methods=['POST','GET'])
def new_subpost(post_id):
    redirectpostid=post_id
    form = SubPostForm()
    if form.validate_on_submit():
        subpost = SubPost(content=form.content.data, post_id=post_id)
        db.session.add(subpost)
        db.session.commit()
        flash('Your subpost has been created!', 'success')
        return redirect(url_for('post', post_id=redirectpostid))
    return render_template('create_subpost.html', form=form)


# @app.route("/post/<int:post_id>/subpost/<int:subpost_id>/update", methods=['GET', 'POST'])
# def update_subpost(post_id,subpost_id):
#     post = Post.query.get_or_404(post_id)
#     subpost = SubPost.query.get_or_404(subpost_id)
#     if subpost.author != current_user:
#         abort(403)
#     form = SubPostForm()
#     if form.validate_on_submit():
#         subpost.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.content.data = subpost.content
#     return render_template('create_subpost.html', title='Update SubPost',
#                            form=form, legend='Update SubPost')


# @app.route("/post/<int:post_id>/subpost/<int:subpost_id>/delete", methods=['POST','GET'])
# def delete_subpost(post_id, subpost_id):
#     post = Post.query.get_or_404(post_id)
#     subpost = SubPost.query.get_or_404(subpost_id)
#     if subpost.author != current_user:
#         abort(403)
#     db.session.delete(subpost)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('post',post_id=post.id))

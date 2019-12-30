from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db
from flaskblog.forms import PostForm, SubPostForm
from flaskblog.models import Post  # SubPost
from flaskblog.utilfuncs import utc_to_local, thread_save_picture, post_save_picture, do_clean, greentext, greenregex

@app.route("/")
@app.route("/home")
def home():
    posts=[]
    for i in Post.query.order_by(Post.date_posted.desc()).all():
        thread_n_posts=[]
        if i.parent is None and i not in [q for w in posts for q in w]:
            thread_n_posts.append(i)
            subposts = Post.query.filter(Post.parent_id == i.id).all()[-5:]
            for j in subposts:
                thread_n_posts.append(j)
            posts.append(thread_n_posts)
        elif i.parent is not None and i.parent not in [q for w in posts for q in w]:
            thread_n_posts.append(i.parent)
            subposts = Post.query.filter(Post.parent_id == i.parent.id).all()[-5:]
            for k in subposts:
                thread_n_posts.append(k)
            posts.append(thread_n_posts)

    return render_template('home.html', posts=posts, utcToLocal=utc_to_local, Len=len, greenRegex=greenregex)


@app.route("/about")
def about():
    return render_template('about.html', title='About')



@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        ip = request.environ['REMOTE_ADDR']
        image = thread_save_picture(form.image.data)
        if form.name.data == '':
            post = Post(title=form.title.data, content=form.content.data,ip=ip, name='Anonymous',image_file=image)
        else:
            post = Post(title=form.title.data, content=form.content.data,ip=ip, name=form.name.data,image_file=image)
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
    subposts = Post.query.filter(Post.parent_id == thread_id).all()
    return render_template('post.html', title=post.title, post=post, subposts=subposts, utcToLocal=utc_to_local, Len=len, greenRegex=greenregex)


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
        ip = request.environ['REMOTE_ADDR']
        if form.name.data == '':
            name = 'Anonymous'
        else:
            name = form.name.data
        if form.image.data:
            image = post_save_picture(form.image.data)
            subpost = Post(content=form.content.data, parent_id=post_id,ip=ip,name=name,image_file=image)
        else:
            subpost = Post(content=form.content.data, parent_id=post_id,ip=ip,name=name,image_file='')
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
# jinja whitelisting few html tags

app.jinja_env.filters['clean'] = do_clean
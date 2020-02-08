from flask import render_template, url_for, redirect, request, abort, flash, session
from flaskblog import app, db, boards
from flaskblog.forms import PostForm, SubPostForm
from flaskblog.utilfuncs import utc_to_local, thread_save_picture, post_save_picture, do_clean, allRegex, moment, bumpOrderThreshold
from flaskblog.utilfuncs import get_class_by_tablename as board
from flaskblog.utilfuncs import post_replies
import os

@app.route("/", methods=['GET','POST'])
def frontpage():
    return render_template('about.html', title='FrontPage')

@app.route("/<string:boardname>", methods=['GET','POST'])
def home(boardname):
    form = PostForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            if session.get('ip') is not None:
                flash('wait a minute before trying to post again, dummy', 'postfailed')
                return redirect(url_for('home',boardname=boardname))
            else:
                ip = request.environ['REMOTE_ADDR']
                image = thread_save_picture(form.image.data)
                if form.name.data == '':
                    post = board(boardname)(title=form.title.data, content=form.content.data,ip=ip, name='Anonymous',image_file=image)
                else:
                    post = board(boardname)(title=form.title.data, content=form.content.data,ip=ip, name=form.name.data,image_file=image)
                db.session.add(post)
                db.session.commit()

                # content circulation
                if bumpOrderThreshold(boardname) != 'maxLimitNotReached':
                    leastactivethread = bumpOrderThreshold()
                    for i in board(boardname).query.filter(board(boardname).parent_id==leastactivethread.id).all():
                        try:
                            os.remove(os.path.join(app.root_path,'static','pics',i.image_file))
                            os.remove(os.path.join(app.root_path,'static','thumbs',i.image_file[:len(i.image_file) - 4]))
                        except FileNotFoundError:
                            pass
                    try:
                        os.remove(os.path.join(app.root_path,'static','pics',leastactivethread.image_file))
                        os.remove(os.path.join(app.root_path,'static','thumbs',leastactivethread.image_file[:len(leastactivethread.image_file) - 4]))
                    except FileNotFoundError:
                        pass
                    delete_subposts = board(boardname).__table__.delete().where(board(boardname).parent_id == leastactivethread.id)
                    db.session.execute(delete_subposts)
                    db.session.delete(leastactivethread)
                    db.session.commit()

                session.permanent = True
                session['ip'] = ip
                return redirect(url_for('home',boardname=boardname))
        else:
            flash(str(form.errors).replace("'",'').replace('[','').replace(']','').replace('{','').replace('}','').replace('This','').replace(':',''),'postfailed')
            return redirect(url_for('home',boardname=boardname))
    elif request.method == 'GET':
        posts=[]
        for i in board(boardname).query.order_by(board(boardname).date_posted.desc()).all():
            thread_n_posts=[]
            if i.parent is None and i not in [q for w in posts for q in w]:
                thread_n_posts.append(i)
                subposts = board(boardname).query.filter(board(boardname).parent_id == i.id).all()[-5:]
                for j in subposts:
                    thread_n_posts.append(j)
                posts.append(thread_n_posts)
            elif i.parent is not None and i.parent not in [q for w in posts for q in w]:
                thread_n_posts.append(i.parent)
                subposts = board(boardname).query.filter(board(boardname).parent_id == i.parent.id).all()[-5:]
                for k in subposts:
                    thread_n_posts.append(k)
                posts.append(thread_n_posts)

    return render_template('home.html', posts=posts, utcToLocal=utc_to_local, Len=len, allRegex=allRegex, form=form, title=boards[boardname], boardtitle=boards[boardname], boardname=boardname)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/<string:boardname>/<int:post_id>", methods=['GET','POST'])
def post(boardname,post_id):
    redirectpostid=post_id
    form = SubPostForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate():
            if session.get('ip') is not None:
                flash('wait a minute before trying to post again, dummy', 'postfailed')
                return redirect(url_for('post',boardname=boardname, post_id=redirectpostid))
            else:
                ip = request.environ['REMOTE_ADDR']
                if form.name.data == '':
                    name = 'Anonymous'
                else:
                    name = form.name.data
                if form.image.data:
                    image = post_save_picture(form.image.data)
                    subpost = board(boardname)(content=form.content.data, parent_id=post_id,ip=ip,name=name,image_file=image)
                else:
                    subpost = board(boardname)(content=form.content.data, parent_id=post_id,ip=ip,name=name,image_file='')
                db.session.add(subpost)
                db.session.commit()
                session.permanent = True
                session['ip'] = ip
                return redirect(url_for('post',boardname=boardname, post_id=redirectpostid))
        else:
            flash(str(form.errors).replace("'",'').replace('[','').replace(']','').replace('{','').replace('}','').replace('This','').replace(':',''),'postfailed')
            return redirect(url_for('post',boardname=boardname, post_id=redirectpostid))
    elif request.method == 'GET':
        thread_id = post_id
        post = board(boardname).query.get_or_404(post_id)
        if post.parent_id is not None:
            abort(404)
        subposts = board(boardname).query.filter(board(boardname).parent_id == thread_id).all()
    return render_template('post.html', post=post, subposts=subposts, utcToLocal=utc_to_local, Len=len, allRegex=allRegex, form=form, boardname=boardname, title=boards[boardname] + ' ' + post.title, boardtitle=boards[boardname], post_replies=post_replies)


# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# def update_post(post_id):
#     post = board(boardname).query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post',boardname=boardname, post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')



@app.route('/<string:boardname>/<int:post_id>/delete', methods=['POST','GET'])
def delete_post(boardname, post_id):
    post = board(boardname).query.get_or_404(post_id)
    if post.ip != request.environ['REMOTE_ADDR']:
        abort(403)
    if post.parent_id is None:  # that means its a whole thread instead of being a simple post
        for i in board(boardname).query.filter(board(boardname).parent_id==post.id).all():
            if i.image_file != '':
                try:
                    os.remove(os.path.join(app.root_path,'static','pics',i.image_file))
                    os.remove(os.path.join(app.root_path,'static','thumbs',i.image_file[:len(i.image_file) - 4]))
                except FileNotFoundError:
                    pass
        try:
            os.remove(os.path.join(app.root_path,'static','pics',post.image_file))
            os.remove(os.path.join(app.root_path,'static','thumbs',post.image_file[:len(post.image_file) - 4]))
        except FileNotFoundError:
            pass
        delete_suposts = board(boardname).__table__.delete().where(board(boardname).parent_id == post.id)
        db.session.execute(delete_suposts)
        db.session.delete(post)
        db.session.commit()
        flash('Thread Successfully deleted!', 'postdelete')
        return redirect(url_for('home',boardname=boardname))

    elif post.parent_id is not None:  # that means its a simple post and not a thread.
        if post.image_file != '':
            try:
                os.remove(os.path.join(app.root_path,'static','pics',post.image_file))
                os.remove(os.path.join(app.root_path,'static','thumbs',post.image_file[:len(post.image_file) - 4]))
            except FileNotFoundError:
                pass
        else:
            pass
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'postdelete')
        return redirect(url_for('post',boardname=boardname,post_id=post.parent_id))


# @app.route("/post/<int:post_id>/subpost/<int:subpost_id>/update", methods=['GET', 'POST'])
# def update_subpost(post_id,subpost_id):
#     post = board(boardname).query.get_or_404(post_id)
#     subpost = Subboard(boardname).query.get_or_404(subpost_id)
#     if subpost.author != current_user:
#         abort(403)
#     form = SubPostForm()
#     if form.validate_on_submit():
#         subpost.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post',boardname=boardname, post_id=post.id))
#     elif request.method == 'GET':
#         form.content.data = subpost.content
#     return render_template('create_subpost.html', title='Update SubPost',
#                            form=form, legend='Update SubPost')

# jinja filter for whitelisting html tags.
app.jinja_env.filters['clean'] = do_clean
# jinja filter for moment js
app.jinja_env.filters['moment'] = moment
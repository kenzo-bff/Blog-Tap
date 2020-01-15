####################################################
# IMPORTS (FROM LIBRARY) ###########################
####################################################

from flask import render_template, url_for, request, redirect, Blueprint, flash
from flask_login import current_user, login_required

####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog import db
from blog.models import BlogPost
from blog.post.forms import BlogPostForm

####################################################
# BLUEPRINT SETUP ##################################
####################################################

blog_posts = Blueprint('blog_posts', __name__)

####################################################
# CREATE POST SETUP ################################
####################################################

@blog_posts.route('/create', methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, category=form.category.data, text= form.text.data, user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        flash('Post Created!')

        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form, page_name='Create a Blog')

####################################################
# BLOG POST VIEW SETUP #############################
####################################################

@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_posts.html', title=post.title, date=post.date, post=post, category=post.category)

####################################################
# UPDATE POST SETUP ################################
####################################################

@blog_posts.route('/<int:blog_post_id>/update', methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)

    if (post.author != current_user):
        abort(403)
    
    form = BlogPostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.text= form.text.data
        post.category = form.category.data

        db.session.commit()
        return redirect(url_for('blog_posts.blog_post', blog_post_id=post.id))

    if (request.method == "GET"):
        form.title.data = post.title
        form.text.data = post.text
        form.category.data = post.category
    
    return render_template('create_post.html', page_name="Update Post", form=form)

####################################################
# DELETE POST SETUP ################################
####################################################

@blog_posts.route('/<int:blog_post_id>/delete', methods=["GET", "POST"])
@login_required
def delete(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)

    if (post.author != current_user):
        abort(403)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('core.index'))
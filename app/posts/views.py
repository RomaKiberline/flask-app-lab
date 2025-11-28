from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from . import post_bp
from .models import Post, CategoryEnum
from .forms import PostForm


@post_bp.route('/', methods=['GET'])
@post_bp.route('', methods=['GET'])
def list_posts():
    from flask import request
    flt = request.args.get('filter', 'all')
    stmt = db.select(Post).order_by(Post.posted.desc())
    if flt == 'active':
        stmt = stmt.where(Post.is_active == True)
    elif flt == 'inactive':
        stmt = stmt.where(Post.is_active == False)
    posts = db.session.scalars(stmt).all()
    return render_template('posts/all_posts.html', posts=posts, current_filter=flt)


@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=CategoryEnum(form.category.data),
            is_active=bool(form.enabled.data),
            posted=form.publish_date.data or None,
            author=current_user.username if getattr(current_user, 'is_authenticated', False) else 'Anonymous',
        )
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully', 'success')
        return redirect(url_for('post.list_posts', filter='all'))
    return render_template('posts/add_post.html', form=form, is_edit=False)


@post_bp.route('/<int:id>', methods=['GET'])
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('posts/detail_post.html', post=post)


@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.category.data = post.category.value if post.category else 'other'
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = bool(form.enabled.data)
        post.posted = form.publish_date.data or post.posted
        post.category = CategoryEnum(form.category.data)
        if getattr(current_user, 'is_authenticated', False):
            post.author = current_user.username
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('post.detail_post', id=post.id))
    return render_template('posts/add_post.html', form=form, is_edit=True, post=post)


@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', 'success')
        return redirect(url_for('post.list_posts'))
    return render_template('posts/delete_confirm.html', post=post)

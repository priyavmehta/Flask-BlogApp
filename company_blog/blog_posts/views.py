# blog_posts/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user, logout_user,login_required
from company_blog import db
from company_blog.models import BlogPost
from company_blog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts',__name__)

#CREATE
@blog_posts.route('/create',methods = ['GET','POST'])
def create_post():
    form = BlogPostForm()
    print("Came here")

    if form.validate_on_submit():
        print("I qm Here")
        blog_post = BlogPost(title = form.title.data,
                            text = form.text.data,
                            user_id = current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        print("This error")

    else:
        print("errored")
    
    return render_template('create_post.html',form = form)

#UPDATE
@blog_posts.route('/<int:blog_post_id>/update',methods = ['GET','POST'])
@login_required
def update(blog_post_id):
    blogPost = BlogPost.query.get_or_404(blog_post_id)

    if blogPost.author != current_user:
        abort(403)
    
    form = BlogPostForm()

    if form.validate_on_submit():
        blogPost.title = form.title.data
        blogPost.text = form.text.data

        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id = blogPost.id))
    
    elif request.method == 'GET':
        form.title.data =  blogPost.title
        form.text.data = blogPost.text
    
    return render_template('create_post.html',title='Updating',form = form)

#READ
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blogPost = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title = blogPost.title,
                            date = blogPost.date,post = blogPost)

#DELETE
@blog_posts.route('/<int:blog_post_id>/delete',methods = ['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blogPost = BlogPost.query.get_or_404(blog_post_id)

    if blogPost.author != current_user:
        abort(403)
    
    db.session.delete(blogPost)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))


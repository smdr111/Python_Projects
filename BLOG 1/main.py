from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from sqlalchemy.util.langhelpers import repr_tuple_names
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()


# FORM FOR NEW BLOG POST
class NewPostForm(FlaskForm):
    title = StringField('Blog Post Title',validators=[DataRequired()])
    subtitle = StringField('Blog Post Title',validators=[DataRequired()])
    author = StringField('Your Name',validators=[DataRequired()])
    img_url = StringField('Blog Image URL',validators=[DataRequired(),URL()])
    body = CKEditorField('Blog Content',validators=[DataRequired()])
    submit = SubmitField('Submit Post')

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    requested_post = db.session.get(BlogPost,post_id)
    return render_template("post.html", post=requested_post)


@app.route('/new-post',methods=['GET','POST'])
def create_new_post():
    new_form = NewPostForm()
    if new_form.validate_on_submit():
        title = db.session.execute(db.select(BlogPost).where(BlogPost.title == new_form.title.data)).scalar()
        if not title:
                new_blog = BlogPost(
                                title=new_form.title.data,
                                subtitle=new_form.subtitle.data,
                                date=datetime.now().strftime("%B %-d, %Y"),
                                body=new_form.body.data,
                                author=new_form.author.data,
                                img_url=new_form.img_url.data
                                )
                db.session.add(new_blog)
                db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html',form=new_form)


@app.route('/edit-post/<int:post_id>',methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost,post_id)
    edit_form = NewPostForm(title=post.title,
                            subtitle=post.subtitle,
                            img_url=post.img_url,
                            author=post.author,
                            body=post.body)
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post',post_id=post.id))
    return render_template('make-post.html',form=edit_form,is_edit=True)


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

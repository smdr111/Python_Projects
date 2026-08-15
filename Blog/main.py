from flask import Flask,render_template,request
import requests
from messenger import NotificationManager

response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
response.raise_for_status()
text = response.json()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',data=text)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=["POST","GET"])
def contact():
    submit = False
    if request.method == 'POST':
        data = request.form
        msg = f"Subject: New Message\n\nName: {data['name']}\n\nEmail: {data['email']}\n\nPhone: {data['phone']}\n\nMessage: {data['message']}"
        notify = NotificationManager()
        notify.send_email('support@tipstation.app',msg)
        submit = True
    return render_template('contact.html',success=submit)

@app.route('/posts/<int:num>')
def get_post(num):
    requested = None
    for blog in text:
        if blog['id'] == num:
            requested = blog
    return render_template('post.html',post=requested,number=num)

if __name__ == '__main__':
    app.run(debug=True)
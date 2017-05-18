title: Intro to Flask
slug: intro-to-flask
date: 14 May 2017
sortdate: 20170514
teaser: Get started building quick easy UIs for your custom tools.
twitter: https://twitter.com/mehemken/status/864171792625131520

##What is Flask?

Flask is a Python library that allows you to build a website quickly using
Python. It is well known throughout the Python community and supports both
Python 2 and 3. As an alternative to Django, Flask is (IMHO) easier to learn.
You don't have to deal with setting up a database if you don't need it. If
you do need it though, you can use your favorite database without worrying
about clashes with the Flask framework. Django is opinionated about that and
works best with relational databases.

##Intro

This post will walk you through how to set up a basic Flask UI. I won't get
into making it look nice with CSS or anything like that. And I won't get into
any JavaScript.

In this tutorial we will build a basic HTML form that doesn't do anything. This
is just to get you started. If you would like to see a followup post that shows
you how to connect the form to a database I can do that.

Outline:

* Print `hello world` to the browser
* Print HTML to the browser
* Using a template for your web page
* Serve an HTML template
* Add a form to the page

---

##Print text in the browser

The first thing to do is set up a new directory for your project and add a file
called `app.py`.

    scratch/
    └── app.py

    0 directories, 1 file

You will also need to install Flask. Use your favorite method for creating a
virtual environment. I use `conda` from the Anaconda Python distribution
([conda docs][1]). But `virtualenv` is also a good option ([virtualenv
docs][2]). Once you have your environment for this project set up you'll just
do a `pip install flask`. It will also pull in a few dependencies.

In `app.py` add the following

    :::python
    # file: app.py

    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello World!"

    if __name__ == "__main__":
        app.run(debug=True)

A few things happening here

* The `app` object is instantiated. This will be a useful tool.
* We define the root url with the `@app.route` decorator.
* We define the response to be returned to anyone who requests our page.
* The `if` statement is [explained here][3].

Now we can go to our terminal and run this. I recommend you run it in a new terminal because it blocks.

    $ python app.py

Now head to your browser and enter the url `localhost:5000`. Flask uses port 5000 by default. You should see the text `Hello World!` in your browser.

---

##Return HTML

Ok that was easy, but how do we return HTML to the browser? Easy

    :::python
    @app.route("/")
    def index():
        return "<html><body><h1>I am HTML</h1></body></html>"

Just change the hello world line to print html.

---

##Using a template

But you want to have HTML in an `.html` file, not a `.py` file. So we'll use a template. Flask comes with the [jinja2][4] template package. It is super useful. To get started we'll need to create a new `index.html` file and put it here:

    scratch/
    ├── app.py
    └── templates/
        └── index.html

And to use it you just do two things

* add `render_template` to our list of imports
* use it in place of returning plain text

Flask takes care of everything else. Here is the entire file so far

    :::python
    # file: app.py

    from flask import Flask, render_template
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template('index.html')

    if __name__ == "__main__":
        app.run(debug=True)

Now if you reload the page you will see nothing. And this is exactly what we want to see. So let's add something to our `index.html`.

    :::html
    <!-- file: index.html -->

    <html>
        <head>
            <title>Default</title>
        </head>
        <body>
            <h1>Spam</h1>
            <p>Eggs, bacon, baked beans.</p>
        </body>
    </html>

Now, if you reload the page you will see your new html.

---

##HTML Forms

The last thing we'll do here is add a form. As a resource I've used the [W3 Schools][5] page on the subject. I don't have form elements memorized.

Open the `index.html` template and add the form elements below. This is the entire file

    :::html
    <!-- file: index.html -->

    <html>
        <head>
            <title>Default</title>
        </head>
        <body>
            <h1>Spam</h1>
            <p>Eggs, bacon, baked beans.</p>
            <form>
                First name: <br>
                <input type="text" name="firstname"><br>
                Last name: <br>
                <input type="text" name="lastname"><br>
            </form>
        </body>
    </html>

---

##Conclusion

We've created a very simple web page that contains text and some form elements. However, because we don't have any server logic to handle any returned data from those elements they don't do anything. That is a topic for another time. Or if I find a good resource that goes into how to use data from form elements, I'll link to it here. Questions, comments, concerns, shoot me an email!

---

[1]: https://conda.io/docs/using/envs.html#id2 "conda envs"
[2]: https://virtualenv.pypa.io/en/stable/userguide/#usage "virtualenv envs"
[3]: http://stackoverflow.com/questions/419163/what-does-if-name-main-do
[4]: http://jinja.pocoo.org/ "jinja2"
[5]: https://www.w3schools.com/html/html_forms.asp "HTML Forms"

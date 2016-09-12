from flask import flash
from flask import redirect
from flask import render_template
from App import app
from .forms import LoginForm
from .forms import ScrapeForm
from tagTrends import startProcess

@app.route('/')

@app.route('/index')
def index():
    user = {'nickname' : 'Oscar'} #fake user
    posts = [ #fake array of posts
        {'author': {'nickname' : 'John'},
         'body' : 'This sure is a fun tutorial!' },
        {'author' : {'nickname' : 'Sue'},
         'body' : 'This sure does keep on keeping on'}]
    return render_template('index.html', title = 'Home', user = user,
                           posts = posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID %s, remember_me %s' %(form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/tags', methods=['GET', 'POST'])
def getTags():
    form = ScrapeForm()
    tagResponse = "Please wait......."
    if form.validate_on_submit():
        u = form.uname.data
        p = form.pseud.data
        ig = form.src.data
        codes = form.picCodes.data
        print(u, " ", p, " ", ig, " ", codes)
        # get python stuff into this setup, import the function I need
        # call the function with the params I have here
        tagResponse = startProcess(ig, u, p, codes)
    return render_template('tagGetter.html', title='Tag Getter', form=form, tagResponse = tagResponse)

#and maybe a version that lets you add things the easy way???
@app.route('/tags/<ig>/<uname>/<pseud>/')
def getTagsAuto():
    '''This is probably not going to work because what do I do about codes?
    :param ig: whether or not this is for instagram
    :param uname: the username of the page to check
    :param pseud: for AO3, the pseud to check
    picture codes need to go somewhere but they can't go here'''
    #get python stuff into this setup, import the function I need
    #call the function with the params I have here
    return render_template('index.html')
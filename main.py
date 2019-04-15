from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

form = """

"""

@app.route("/", methods=['GET','POST'])
def index():
    template = jinja_env.get_template('gloriousform.html')
    if(request.method != 'POST'):
        return template.render(name="", name_error="", passphrase="", pass_error="", check="", verify_error="", address="", email_error="")
        #return form.format(name="", name_error="", passphrase="", pass_error="", check="", verify_error="", address="", email_error="")
    else:
        name=request.form['username']
        password=request.form['password']
        verify=request.form['verify']
        email=request.form['email']

        name_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""
        emailval2 = True

        if len(name) < 3 or len(name) > 20 or " " in name:
            name_error="Not a valid name"

        if len(password) < 3 or len (password) > 20 or " " in password:
            pass_error="Not a valid password"

        if password != verify:
            verify_error="Passwords don't match"

        if email:
            emailval = 0
            for ix in range(len(email)):
                if email[ix]=="@":
                    emailval+=1
            if emailval != 1:
                emailval2 = False

            emailval = 0
            for ix in range(len(email)):
                if email[ix]==".":
                    emailval+=1
            if emailval != 1:
                emailval2 = False
            if len(email) < 3 or len(email) > 20 or " " in email:
                emailval2 = False

        if(emailval2==False):
            email_error="Not a valid email address"

        if not name_error and not pass_error and not verify_error and not email_error:
            return redirect('/welcome?username={0}'.format(name))
        else:
            return template.render(name=name, name_error=name_error, passphrase="", pass_error=pass_error, check="", verify_error=verify_error, address=email, email_error=email_error)
            #return form.format(name=name, name_error=name_error, passphrase="", pass_error=pass_error, check="", verify_error=verify_error, address=email, email_error=email_error)


@app.route("/welcome")#, methods=['POST'])
def welcome():
    template = jinja_env.get_template('gloriouswelcome.html')
    name=request.args.get('username')
    return template.render(name=cgi.escape(name))
#<h1>Welcome, {0} </h1>".format(cgi.escape(name))
app.run()

# END ROUTE about


# ROUTE admin
app.secret_key = b'$API_KEY'


@app.route("/login", methods=["GET", "POST"])
def login():
    from flask import session
    if request.form.get("password") is not None:
        if request.form.get("password") == "$ADMIN_PASSWORD":
            session['logged_in'] = True
            return admin()
        else:
            return render_template("login.html", error="Invalid Credentials. Please try again.")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    from flask import session
    session['logged_in'] = False
    return index()


@app.route("/admin", methods=["GET", "POST"])
def admin():
    from flask import session
    if not session.get('logged_in'):
        return render_template('login.html', error="You need to login to access the Admin page")
    else:
        message = None
        # list vocabs in GitHub
        r = requests.get(
            "https://api.github.com/repos/surroundaustralia/ga-vocabs/contents/ggic",
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        vocabs = []
        for v in r.json():
            vocabs.append({
                "name": v["name"].replace(".ttl", ""),
                "id": v["name"],
                "uri": v["download_url"],
            })

        if request.method == "POST":
            if request.form.get("func") == "cache":
                cache_reload()
                message = "VocPrez cache reloaded"
            elif request.form.get("func") == "one":
                message = "Vocab {} (re)loaded".format(request.form.get("reload-one"))
            elif request.form.get("func") == "all":
                message = "All vocabs reloaded"
            else:
                pass
            return render_template("admin.html", vocabs=vocabs, message=message)
        else:
            return render_template("admin.html", vocabs=vocabs)
# ROUTE admin


# ROUTE sparql

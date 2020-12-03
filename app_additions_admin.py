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
        vocabs = get_vocabs_from_github()

        del_vocabs = []
        for k, v in g.VOCABS.items():
            del_vocabs.append({
                "name": v.title,
                "uri": v.uri,
            })

        if request.method == "POST":
            if request.form.get("func") == "cache":
                cache_reload()
                message = "VocPrez cache reloaded"
            elif request.form.get("func") == "one":
                try:
                    success = load_one_vocab_from_github(request.values.get("reload-one"))

                    if not success[0]:
                        message = "The insert function didn't work. Error: {}".format(success[1])
                        return render_template("admin.html", vocabs=vocabs, message=message)
                    else:
                        message = "Vocabulary {} loaded or reloaded ok".format(request.form.get("reload-one"))
                        return render_template("admin.html", vocabs=vocabs, message=message)

                    message = "Vocab {} (re)loaded".format(request.form.get("reload-one"))
                except Exception as e:
                    message = "Error loading vocab {}: {}".format(request.form.get("reload-one"), e)
                    return render_template("admin.html", vocabs=vocabs, message=message)
            elif request.form.get("func") == "del":
                success = delete_one_vocab(request.values.get("del-one"))

                if not success[0]:
                    message = "The delete function didn't work. Error: {}".format(success[1])
                    return render_template("admin.html", del_vocabs=del_vocabs, vocabs=vocabs, message=message)
                else:
                    message = "Vocabulary {} deleted ok".format(request.form.get("del-one"))
                    return render_template("admin.html", del_vocabs=del_vocabs, vocabs=vocabs, message=message)
            elif request.form.get("func") == "all":
                success = reload_all_vocabs()
                if success[0]:
                    message = "<ul>"
                    for vocab in success[1]:
                        if vocab[1][0]:
                            message += "<li>" + vocab[0] + ": loaded</li>"
                        else:
                            message += "<li style=\"color:red;\">" + vocab[0] + ": error: " + vocab[1][1] + "</li>"
                    message += "</ul>"
                else:
                    message = success[1]

                return render_template("admin.html", del_vocabs=del_vocabs, vocabs=vocabs, message=message)

            return render_template("admin.html", del_vocabs=del_vocabs, vocabs=vocabs, message=message)
        else:
            return render_template("admin.html", del_vocabs=del_vocabs, vocabs=vocabs)


def get_vocabs_from_github():
    def _get_contents(uri):
        r = requests.get(
            uri,
            headers={
                'Accept': 'application/vnd.github.v3+json',
                "Authorization": "token 88d1cbc9d261c14e82b33f0a640ba67188fc9ff4"
            }
        )
        return r.json()

    folders = _get_contents(config.GITHUB_API_URI)
    if folders.get("message") is not None:
        return []

    vocabs = []
    for folder in folders:
        if folder["name"] in config.GITHUB_VOCAB_FOLDERS.split(","):
            vs = _get_contents(folder["url"].replace("?ref=master", ""))
            for v in vs:
                if v["name"].endswith(".ttl"):
                    vocabs.append({
                        "name": v["name"].replace(".ttl", ""),
                        "id": v["name"],
                        "uri": v["download_url"],
                    })

    return vocabs


def delete_one_vocab(named_graph_uri):
    r = requests.post(
        "{}/repositories/{}/statements".format(config.GRAPH_DB_URI, config.GRAPHDB_REPO_ID),
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/rdf+xml', 'Accept': 'application/json'},
        params={"update": "DROP GRAPH <{}>".format(named_graph_uri)}
    )
    if r.status_code not in [204]:
        return False, str(r.status_code) + "\n" + r.content.decode('utf-8')
    else:
        return True, ""


def load_one_vocab_from_github(vocab_url):
    from rdflib.namespace import RDF, SKOS
    gr = Graph()
    gr.parse(location=vocab_url, format="turtle")
    for s in gr.subjects(predicate=RDF.type, object=SKOS.ConceptScheme):
        named_graph_uri = str(s)
        for o in gr.objects(subject=s, predicate=SKOS.prefLabel):
            pref_label = str(o)

    if named_graph_uri is None or pref_label is None:
        message = "Could not get a Named Graph (vocab) URI or a Concept Scheme prefLabel from the RDF file"
        return False, message

    namespace = named_graph_uri + '/'

    r = requests.post(
        "{}/rest/data/import/upload/{}/url".format(config.GRAPH_DB_URI, config.GRAPHDB_REPO_ID),
        auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        json={
            'baseURI': namespace,
            'context': named_graph_uri,
            'data': vocab_url,
            'forceSerial': True,
            'format': 'text/turtle',
            'message': '',
            'name': pref_label,
            'parserSettings': {
                'failOnUnknownDataTypes': False,
                'failOnUnknownLanguageTags': True,
                'normalizeDataTypeValues': True,
                'normalizeLanguageTags': True,
                'preserveBNodeIds': True,
                'stopOnError': True,
                'verifyDataTypeValues': True,
                'verifyLanguageTags': True,
                'verifyRelativeURIs': True,
                'verifyURISyntax': True
            },
            'replaceGraphs': [
                named_graph_uri  # same as Context
            ],
            'status': 'PENDING',
            'timestamp': 0,
            'type': 'string',
            'xRequestIdHeaders': 'string'
        }
    )

    if r.status_code not in [201, 202]:
        return False, str(r.status_code) + "\n" + r.content.decode('utf-8')
    return True, ""


def reload_all_vocabs():
    logging.debug("reload all vocabs triggered")
    try:
        r = requests.delete(
            "{}/repositories/{}/statements".format(config.GRAPH_DB_URI, config.GRAPHDB_REPO_ID),
            auth=(config.GRAPHDB_USR, config.GRAPHDB_PWD),
            headers={'Accept': 'application/json'}
        )
        if r.status_code not in [204]:
            return False, str(r.status_code) + "\n" + r.content.decode('utf-8')

        vocabs = get_vocabs_from_github()
        vocabs_loaded = []
        for v in vocabs:
            try:
                vocabs_loaded.append((v["uri"].split("/")[-1], load_one_vocab_from_github(v["uri"])))
            except Exception as e:
                vocabs_loaded.append((v["uri"].split("/")[-1], (False, str(e))))

        return True, vocabs_loaded
    except Exception as e:
        return False, "Reloading all vocabs error: " + str(e)
# END ROUTE admin


# ROUTE sparql

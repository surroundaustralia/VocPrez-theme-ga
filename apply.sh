# copy all style content to VP
cp $VP_THEME_HOME/style/* $VP_HOME/vocprez/view/style

# copy all templates to VP
cp $VP_THEME_HOME/templates/* $VP_HOME/vocprez/view/templates

# append paths to VP routes, removing running locally commands
# truncate app.py
sed -i -n '/# run the Flask app/q;p' $VP_HOME/vocprez/app.py
# add new routes
more $VP_THEME_HOME/routes.txt >> $VP_HOME/vocprez/app.py


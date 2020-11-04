echo "Styles"
echo "copying $VP_THEME_HOME/style content to $VP_HOME/vocprez/view/style"
cp $VP_THEME_HOME/style/* $VP_HOME/vocprez/view/style

echo "Templates"
echo "copying $VP_THEME_HOME/templates content to $VP_HOME/vocprez/view/templates"
cp $VP_THEME_HOME/templates/* $VP_HOME/vocprez/view/templates

echo "Config"
echo "creating VocPrez config with $VP_THEME_HOME/config.py"
echo "Alter config.py to include variables"
sed 's#$SPARQL_ENDPOINT#'"$SPARQL_ENDPOINT"'#' $VP_THEME_HOME/config.py > $VP_THEME_HOME/config_updated.py
sed -i 's#$SPARQL_USERNAME#'"$SPARQL_USERNAME"'#' $VP_THEME_HOME/config_updated.py
sed -i 's#$SPARQL_PASSWORD#'"$SPARQL_PASSWORD"'#' $VP_THEME_HOME/config_updated.py
sed -i 's#$GRAPHDB_REPO_ID#'"$GRAPHDB_REPO_ID"'#' $VP_THEME_HOME/config_updated.py
sed -i 's#$GRAPH_DB_URI#'"$GRAPH_DB_URI"'#' $VP_THEME_HOME/config_updated.py
sed -i 's#$GITHUB_RAW_URI_BASE#'"$GITHUB_RAW_URI_BASE"'#' $VP_THEME_HOME/config_updated.py
sed -i 's#$GITHUB_TOKEN#'"$GITHUB_TOKEN"'#' $VP_THEME_HOME/config_updated.py
mv $VP_THEME_HOME/config_updated.py $VP_HOME/vocprez/_config/__init__.py

echo "Routes for app.py"
echo "Route admin"
sed -n '/# END ROUTE about/q;p' $VP_HOME/vocprez/app.py > $VP_THEME_HOME/app_temp.py
sed 's#$API_KEY#'"$API_KEY"'#' $VP_THEME_HOME/app_additions_admin.py > $VP_THEME_HOME/app_additions_admin_temp.py
sed -i 's#$ADMIN_PASSWORD#'"$ADMIN_PASSWORD"'#' $VP_THEME_HOME/app_additions_admin_temp.py
cat $VP_THEME_HOME/app_additions_admin_temp.py >> $VP_THEME_HOME/app_temp.py
rm $VP_THEME_HOME/app_additions_admin_temp.py
sed -e '1,/# ROUTE sparql/ d' $VP_HOME/vocprez/app.py >> $VP_THEME_HOME/app_temp.py
mv $VP_THEME_HOME/app_temp.py $VP_HOME/vocprez/app.py

echo "customisation done"
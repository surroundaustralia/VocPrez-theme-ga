echo "Style: copying $VP_THEME_HOME/style content to $VP_HOME/vocprez/view/style"
cp $VP_THEME_HOME/style/* $VP_HOME/vocprez/view/style

echo "Templates: copying $VP_THEME_HOME/templates content to $VP_HOME/vocprez/view/templates"
cp $VP_THEME_HOME/templates/* $VP_HOME/vocprez/view/templates

echo "Config: creating VocPrez config with $VP_THEME_HOME/config.py"
echo "Alter config.py to include variables"
sed 's#$SPARQL_ENDPOINT#'"$SPARQL_ENDPOINT"'#' config.py > config_updated.py
sed 's#$SPARQL_USERNAME#'"$SPARQL_USERNAME"'#' config.py > config_updated.py
sed 's#$SPARQL_PASSWORD#'"$SPARQL_PASSWORD"'#' config.py > config_updated.py
mv $VP_THEME_HOME/config_updated.py $VP_HOME/vocprez/_config/__init__.py

echo "customisation done"
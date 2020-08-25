echo "Style: copying $VP_THEME_HOME/style content to $VP_HOME/vocprez/view/style"
cp $VP_THEME_HOME/style/* $VP_HOME/vocprez/view/style

echo "Templates: copying $VP_THEME_HOME/templates content to $VP_HOME/vocprez/view/templates"
cp $VP_THEME_HOME/templates/* $VP_HOME/vocprez/view/templates

echo "Config: creating VocPrez config with $VP_THEME_HOME/config.py"
cp $VP_THEME_HOME/config.py $VP_HOME/vocprez/_config/__init__.py

echo "customisation done"
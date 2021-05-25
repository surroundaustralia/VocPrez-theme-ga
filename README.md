# VocPrez-theme-ga
A VocPrez UI theme for [Geoscience Australia](https://www.ga.gov.au/).

`apply.sh` adds these elements - templates, style files - to a local VocPrez instance.

The only config needed is to set the following environment variables before using `apply.sh`:

* `$VP_THEME_HOME` - installation dir of this theme, no trailing slash
* `$VP_HOME` - installation dir of VocPrez, no trailing slash
* `$SPARQL_ENDPOINT` - the underlying SPARL endpoint used by VocPrez to query for vocabularies
  * and `SPARQL_USERNAME` & `SPARQL_PASSWORD` if appropriate
* `$SYSTEM_BASE_URI` - tells VocPrez where online it's actually located

`docker-build.sh` takes the same variables as `apply.sh` but builds a Docker image which can then be deployed.
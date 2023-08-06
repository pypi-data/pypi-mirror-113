rm -rf dist
python setup.py sdist bdist_wheel
# git add . && git commit -m "$@"
twine check dist/* && twine upload -u ggdwbg -p $(cat ../pypi_creds.txt) dist/*
xonsh ./bump_version.xsh
# git push -u origin main

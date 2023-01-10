# Release checklist

- Tests run at least in all supported versions of python. Use `tox`
- Increment version
- Update Changelog
- build with $ `./setup.py sdist bdist_wheel`
- upload to testpypi as required $ `twine upload --repository testpypi dist/simplesuper-*`
- Test install and check the new version from pypi as per the instructions on the testpypi page
- Tag release
- Push git tags
- upload to pypi as required $ `twine upload dist/simplesuper-*`

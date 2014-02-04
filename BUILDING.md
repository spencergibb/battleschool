### Building locally

    git checkout devel

    # make changes

    git commit

    git push

    git checkout master

    make sdist

    git checkout devel #make sure to go back to devel to make changes

### deploying to pypi

make sure `~/.pypirc` is setup correctly

    [pypirc]
    servers = pypi
    [server-login]
    username:<username>
    password:<password>

then

    python setup.py sdist upload
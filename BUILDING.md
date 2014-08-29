### Building locally

    git checkout devel

    # make changes

    git commit

    git push

    git checkout master

	 git merge devel

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

#### Tips for building on a blank osx vm

http://ntk.me/2012/09/07/os-x-on-os-x/

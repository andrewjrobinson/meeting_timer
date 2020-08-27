#!/bin/bash
#
# Updates the version to the value passed on cmd, builds package, 
#

# get root directory
ROOT_DIR=$(readlink -f $(dirname $0)/..)

# run in subshell
(

cd $ROOT_DIR

if [ $# -ne 1 ]; then
    echo "usage: $0 VERSION"
    exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
VERSION=$1

# make sure version number is correct format
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Incorrect version format.  Must be MAJOR.MINOR.PATCH"
    exit 2
fi

# make sure branch is master
if [[ ! $CURRENT_BRANCH == "master" ]]; then
    echo "You can only update version number of master branch"
    exit 3
fi

# check for uncommited files
if [ ! -z "$(git diff --name-only)" ]; then
    echo "WARNING: uncommited changes found"
    read -p "Continue? [Yn] " ANS
    if [[ ! ${ANS,,} == "y" ]] && [[ ! ${ANS,,} == "" ]]; then
        exit 0
    fi
fi

# output versions
grep "version=" setup.py | sed 's/^.*version="/Current Version="/'
echo "    New Version=\"$VERSION\","


echo
read -p "Is this correct? [Yn] " ANS
if [[ ! ${ANS,,} == "y" ]] && [[ ! ${ANS,,} == "" ]]; then
    exit 0
fi

# update version
echo
echo "Updating version"
echo "sed -i 's/^.*version=\".*\",/    version=\"'$VERSION'\",/' setup.py"
sed -i 's/^.*version=".*",/    version="'$VERSION'",/' setup.py
echo "sed -i \"s/__version__\s*=\s*'.*'/__version__ = '$VERSION'/\" src/meeting_timer/__init__.py"
sed -i "s/__version__\s*=\s*'.*'/__version__ = '$VERSION'/" src/meeting_timer/__init__.py

# # build package
echo
read -p "Build package? [Yn] " ANS
if [[ ${ANS,,} == "y" ]] || [[ ${ANS,,} == "" ]]; then
    echo
    echo "python3 setup.py sdist bdist_wheel"
    python3 setup.py sdist bdist_wheel
    
    # check it works
    echo
    read -p "Test package install? [Yn] " ANS
    if [[ ${ANS,,} == "y" ]] || [[ ${ANS,,} == "" ]]; then
        
        PKG_NAME="${ROOT_DIR}/dist/meeting_timer-${VERSION}.tar.gz"

        # ensure package is built
        if [ ! -e $PKG_NAME ]; then
            echo "ERROR: package not found: ${PKG_NAME}"
            exit 3
        fi
        
        # ensure build env exists and activate it
        if [ ! -e build ]; then
            mkdir build
        fi
        if [ -e build/pkgtest-venv/bin/activate ]; then
            echo "--Remove last build env--"
            rm -r build/pkgtest-venv
            echo "Done"
        fi
        echo
        echo "--Create VENV--"
        python3 -m venv build/pkgtest-venv
        source build/pkgtest-venv/bin/activate
        pip install --upgrade pip wheel
        
        # install package
        echo
        echo "--Install Package--"
        pip install ${PKG_NAME}
        
        echo
        echo "--Check applications exist--"
        if ! which meeting-timer; then echo "ERROR: meeting-timer not found"; fi
        
        echo "--Done--"
    fi

    echo
    read -p "Commit and tag? [Yn] " ANS
    if [[ ${ANS,,} == "y" ]] || [[ ${ANS,,} == "" ]]; then
        
        echo
        echo "git add setup.py src/meeting_timer/__init__.py"
        git add setup.py src/meeting_timer/__init__.py
        
        echo "git commit -m \"Version ${VERSION}\""
        git commit -m "Version ${VERSION}"
        
        echo "git tag -a -m \"Version ${VERSION}\" v${VERSION}"
        git tag -a -m "Version ${VERSION}" v${VERSION}
    
        echo
        read -p "Push upstream? [Yn] " ANS
        if [[ ${ANS,,} == "y" ]] || [[ ${ANS,,} == "" ]]; then
            
            echo
            echo "git push origin HEAD"
            git push origin HEAD
            
            echo
            echo "git push origin --tags"
            git push origin --tags
        fi
        
    fi # end commit and tag
    
    echo
    read -p "Push to pypi? [Yn] " ANS
    if [[ ${ANS,,} == "y" ]] || [[ ${ANS,,} == "" ]]; then
        echo
        echo "twine upload dist/meeting_timer-$VERSION.tar.gz dist/meeting_timer-$VERSION-py3-none-any.whl"
        twine upload dist/meeting_timer-$VERSION.tar.gz dist/meeting_timer-$VERSION-py3-none-any.whl
    fi
fi


echo
echo "Done"

) # end subshell

# pass exit code up
exit $?


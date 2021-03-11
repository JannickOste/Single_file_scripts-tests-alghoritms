#!/bin/bash
workspace=~/Desktop/Workspace

echo '##########################################################################'
echo '# Enter password to start installation (required for install permisions) #'
echo '#                                                                        #'
echo '# Installation includes:                                                 #'
echo '# -> Git (Version control)                                               #'
echo '# -> Apache (HTTP server)                                                #'
echo '# -> PHP + (Apache module)                                               #'
echo '# -> Python / Python3 (interpreters)                                     #'
echo '# -> Snapd (Required for some instalations))                             #'
echo '# -> Open JDK 8 (Required for java development)                          #'
echo '# -> GIMP (Image editor)                                                 #'
echo '# -> Eclipse (Java IDE)                                                  #'
echo '# -> Pycharm (Python IDE)                                                #'
echo '##########################################################################'

function InstallPackages()
{
    snapLock=/etc/apt/preferences.d/nosnap.pref
    if test -e $snapLock;
    then 
        echo "[Removing snapd lock (for linux mint)]"
        sudo rm $snapLock
        echo ""
    fi
    
    echo "[[Starting apt based package instalations]]"
    for package in apache2 php libapache2-mod-php python python3 snapd openjdk-8-jdk GIMP 
    do
        exists=$(dpkg -l | grep $package)
        if [ "$exists" == '' ];
            then 
                echo "[Out] => Installing: $package"
                sudo apt-get --yes install $package
                echo ""

                echo "[Out] => Performing apt update"
                sudo apt update
                echo ""
            else 
                echo "[Out] => $package is already installed, skipping instalation]"
         fi
    done

    echo ""
    echo "[Configuring PHP module]"
    sudo a2enmod php 
    echo "[Rebooting apache module]"
    sudo systemctl restart apache2

    echo "[[Starting snap based package instalations]]"
    for package in eclipse pycharm-community
    do
        exists=$(snap list | grep $package)
        if [ "$exists" == '' ];
            then 
                echo "[Out] => Installing: $package"
                sudo snap install $package --classic
                echo ""
            else 
                echo "[Out] => $package is already installed, skipping instalation]"
        fi
    done
}

function CreateWorkspace()
{
    if test -e $workspace; 
    then
        echo -n ""
    else 
        echo "[[Creating workspace directory with symbolic links]]"
        mkdir $workspace
        cd $workspace
        ln -s ~/PycharmProjects "./Pycharm"
        ln -s /var/www/ "./Apache server"
        mkdir "./Eclipse"
    fi
}

InstallPackages
CreateWorkspace

#!/bin/bash

# Symlink directory to workspaces.
workspace="/home/$USER/Desktop/Workspace"

# Apt install packages
default_packages=("apache2", "php", "libapache2-mod-php", "python", "python3", "snapd", "openjdk-8-jdk", "GIMP")

# Snap install packages
snap_packages=("eclipse", "pycharm-community", "android-studio", "snap-store")

# Check for distro required actions (Ex: Remove snapd lock from linux mint / Whitelist devices in kali / etc...)
function CheckDistro() 
{
    distro=$(cat /etc/*-release | grep DISTRIB_ID | cut -c 12-)
    case "$distro" in 
        "LinuxMint")
            snapLock=/etc/apt/preferences.d/nosnap.pref
            if test -e $snapLock;
            then 
                echo "[Removing snapd lock (for linux mint)]"
                sudo rm $snapLock
                echo ""
            else echo "No snaplock found"
            fi
        
        ;;
        *)
            echo "No distro required actions found"
    esac   
}

function InstallPackages()
{

    echo "[[Starting apt based package instalations]]"
    for package in $default_packages
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
    echo "[Configuring PHP module (if this outputs an error, check your installed php version and run 'sudo a2enmod phpVERSION')]"
    sudo a2enmod php7.4
    echo "[Rebooting apache module]"
    sudo systemctl restart apache2

    echo "[[Starting snap based package instalations]]"
    for package in $snap_packages
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
    echo $workspace
    while read line; do
        IFS="=" # Internal field seperator.
        read -r LIST <<< $line
        
        package=""
        for i in $LIST;
        do
            if [ "$package" == "" ];
                then
                    package=$i
                else 
                    exists=$(dpkg -l | grep $package)
                    snapexists=$(ls -lr /snap/ | grep $package)
                    if [[ "$exists" != '' || "$snapexists" != '' ]];
                    then
                        
                        echo "[out] => Package "$package" was installed creating symling"
                        search=$(printf "$%s" "USER")
                        ln -s ${i/"$search"/$USER} $workspace/$package
                    fi
            fi
        done
        IFS=" "
   done < "sympaths.cfg"
   # 
   # if test -e $workspace; 
   # then
   #     echo -n ""
   # else 
   #     echo "[[Creating workspace directory with symbolic links]]"
   #     mkdir $workspace
   #     cd $workspace
   #     mkdir "/home/$USER/Eclipse"
   #     mkdir "/home/$USER/PycharmProjects"
   #     
   #     ln -s /var/www/ "./Apache server"
   #     ln -s /home/$USER/PycharmProjects "./Pycharm"
   #     ln -s /home/$USER/Eclipse "./Eclipse"
   # fi
}
CheckDistro
# InstallPackages
CreateWorkspace

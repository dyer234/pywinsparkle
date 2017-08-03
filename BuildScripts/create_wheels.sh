
set -e
set -x



function download_latest_winsparkle()
{
    winsparkle_version="0.5.5"

    mkdir -p ./WORK
    cd WORK 

    wget https://github.com/vslavik/winsparkle/releases/download/v$winsparkle_version/WinSparkle-$winsparkle_version.zip
    unzip WinSparkle-$winsparkle_version.zip
    cd WinSparkle-$winsparkle_version

    libs_folder="../../../pywinsparkle/libs"
	
    # move the x86 version
    cp Release/WinSparkle.dll $libs_folder/x86
    diff Release/WinSparkle.dll $libs_folder/x86/WinSparkle.dll


    # move the x64 version
    cp x64/Release/WinSparkle.dll $libs_folder/x64/
    diff x64/Release/WinSparkle.dll $libs_folder/x64/WinSparkle.dll

    cd ../../
    rm -r WORK
}

# This fucntion creates a virtual environment for the version
# of python specified in the arguments.
# Args:
#     $1 major version
#     $2 minor version
#     $3 revision version
#     $4 platform
function build_python_wheel()
{
	rm -rf venv
	~/projects/build_python/install_python.sh --major $1 --minor $2 --revision $3
	source venv/bin/activate
	python -m pip install wheel
	
	python -m pip install pypandoc

	cd ../
	python setup.py bdist_wheel --plat-name=$4
	deactivate
	cd BuildScripts
}

function generate_documentation()
{
	rm -rf venv
	python3 -m venv venv
	source venv/bin/activate
	python -m pip install wheel
	python -m pip install sphinx
	cd BuildScripts/sphinx
	make html
}


function main()
{
	download_latest_winsparkle

	sudo apt-get install pandoc

	# create the wheel for python 3.6
	build_python_wheel 3 6 1 win32 
	build_python_wheel 3 6 1 win_amd64

	# create the wheel for python 3.5
	build_python_wheel 3 5 2 win32
	build_python_wheel 3 5 2 win_amd64

	# create the wheel for python 3.4
	build_python_wheel 3 4 5 win32
	build_python_wheel 3 4 5 win_amd64

	# create the wheel for python 3.3
	build_python_wheel 3 3 5 win32
	build_python_wheel 3 3 5 win_amd64

	# create the wheel for python 3.2
	#build_python_wheel 3 2 6 win32
	#build_python_wheel 3 2 6 win_amd64

	# create the wheel for python 2.7
	build_python_wheel 2 7 13 win32
	build_python_wheel 2 7 13 win_amd64

	sudo rm -rf WORK_TEMP	
	cd ../

	generate_documentation
}

main





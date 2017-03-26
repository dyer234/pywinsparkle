
set -e
set -x

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

	python setup.py bdist_wheel --plat-name=$4
	deactivate
}


function main()
{
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
}

main






function upload_wheels()
{
	rm -rf venv
	python3 -m venv venv
	source venv/bin/activate
	python -m pip install wheel
	python -m pip install twine

	python -m twine upload ../dist/*
	deactivate
	rm -rf venv
}

upload_wheels
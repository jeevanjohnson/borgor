import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "borgor",
	version = "0.1.5",
	author = "coverosu",
	author_email = 'coverosu@gmail.com',
	description = "An osu! python package.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/coverosu/borgor",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)

# python3.9 setup.py sdist bdist_wheel
# python3.9 -m twine upload --repository pypi dist/*
import setuptools

with open("README.md") as f:
  README = f.read()
  
setuptools.setup(
  name="DiscordBotWeb",
  version="0.0.2",
  description="Make A Simple Website For Your Discord Bot Without Any HTML Knowledge!",
  long_description=README,
  long_description_content_type="text/markdown",
  author="nooby xviii",
  author_email="xviii2008@gmail.com",
  packages=setuptools.find_packages(),
  include_package_data=True,
  install_requires=["os", "shutil"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.6"
  )
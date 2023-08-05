from setuptools import setup, find_packages
classifiers = []

setup(
    name="improvmxpy",
    version="1.4",
    description="A ImprovMX API Wrapper!",
    long_description=open("README.md").read()
    + "\n# Help \nPlease go to [Documentation](https://improvmxpy.tk)",
    long_description_content_type="text/markdown",
    url="https://github.com/dumb-stuff/improvmx_py",
    author="Rukchad Wongprayoon",
    author_email="contact@biomooping.tk",
    license="MIT",
    classifiers=classifiers,
    keywords="Tools",
    packages=find_packages(),
    install_requires=["requests", "aiohttp"],
    extras_require={"speed":["brotli","cchardet","aiodns"]},
    project_urls={
        "Documentation": "https://improvmxpy.tk",
        "Github Repository": "https://github.com/dumb-stuff/improvmx_py",
        "Issues Reporting": "https://github.com/dumb-stuff/improvmx_py/issues",
        "Pull Requests": "https://github.com/dumb-stuff/improvmx_py/pullrequests",
        "Discord server": "https://discord.gg/sHprKhGwg8",
        "Funny youtube clip": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },

)

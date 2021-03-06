# from glob import glob
# from posixpath import basename, splitext
import setuptools

g2p4utau_required_packages = [
    "jamo==0.4.1",
    "regex",
    "g2pk==0.9.3",
]

utaupyk_required_packages = [
    "utaupy==1.18.0",
    "tqdm",
    "pyyaml==6.0",
]

total_required_packages = []
total_required_packages += g2p4utau_required_packages
total_required_packages += utaupyk_required_packages

total_required_packages = list(set(total_required_packages))

setuptools.setup(
    name="enunu-kor-tool",
    version="0.0.5",
    author="cardroid",
    author_email="carbonsindh@gmail.com",
    description="enunu Korean language support script collection",
    install_requires=total_required_packages,
    license="MIT",
    packages=setuptools.find_packages(where="enunu-kor-tool"),
    package_dir={"": "enunu-kor-tool"},
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={"console_scripts": ["g2pk4utau=g2pk4utau.g2pk4utau:main"]},
)

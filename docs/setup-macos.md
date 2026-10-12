# macOS setup

Install Git and Python 3.10+ using your normal package manager or [Python's installer](https://www.python.org/downloads/macos/). Install [MacTeX](https://tug.org/mactex/) for a complete TeX distribution. Its tools normally appear under `/Library/TeX/texbin`; restart your terminal after installation.

If you already use Homebrew, one setup option is:

```bash
brew install git python poppler
brew install --cask mactex-no-gui
```

A smaller BasicTeX installation is also possible, but needs additional packages. With a TeX Live-based installation, the relevant extra packages are:

```bash
sudo /Library/TeX/texbin/tlmgr install geometry lm hyperref enumitem needspace hyphenat microtype
```

Use the package manager belonging to your TeX installation; `sudo` is only appropriate for a system installation you administer. The project itself never installs packages.

From the cloned folder:

```bash
python3 resume.py doctor
python3 resume.py build examples/demo-person --all
python3 resume.py new personal/my-resume --variant hybrid
```

Use `python3` for the README's `python` commands. The included editor tasks already use `python3` on macOS. Confirm all files listed by doctor are present before building.

Sources: [MacTeX](https://tug.org/mactex/), [Homebrew MacTeX cask](https://formulae.brew.sh/cask/mactex-no-gui), [Poppler formula](https://formulae.brew.sh/formula/poppler).

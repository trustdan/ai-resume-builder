# Linux setup

Install Git, Python 3.10+, a TeX Live distribution, Latin Modern fonts, and Poppler utilities through your distribution's package manager. On Ubuntu 24.04 or another compatible Debian-based system:

```bash
sudo apt update
sudo apt install git python3 texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
```

Use your distribution's equivalent packages elsewhere. `texlive-latex-extra` supplies the small layout packages used here. Use your OS package manager for a distribution-managed TeX installation rather than mixing it with a system-wide `tlmgr` install.

From the cloned folder:

```bash
python3 resume.py doctor
python3 resume.py build examples/demo-person --all
python3 resume.py new personal/my-resume --variant hybrid
```

Use `python3` for the README's `python` commands. The included editor tasks use `python3` on Linux. Python scripts require no pip packages.

References: [TeX Live](https://tug.org/texlive/), [Ubuntu package search](https://packages.ubuntu.com/), [Poppler](https://poppler.freedesktop.org/).

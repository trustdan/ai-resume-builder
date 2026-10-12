# Windows setup

Install [Git for Windows](https://git-scm.com/downloads/win), [Python 3.10 or newer](https://www.python.org/downloads/windows/), and [MiKTeX](https://miktex.org/howto/install-miktex) or [TeX Live](https://tug.org/texlive/). For Python, enable the installer option that adds Python to PATH.

In MiKTeX Console, update the distribution and install missing packages deliberately before building. This starter does not run installers. The required TeX files are listed by `doctor`; common package names include `geometry`, `lm`, `hyperref`, `enumitem`, `needspace`, `hyphenat`, and `microtype`.

Install PDF tools providing `pdftotext`, `pdffonts`, and `pdfinfo`. Some MiKTeX installations already provide all three. Otherwise install a Windows build linked from [Poppler's project page](https://poppler.freedesktop.org/) and add its executable directory to your user PATH. Optional `pdftoppm` is only for refreshing preview images.

Open a **new** PowerShell terminal after installation. From the cloned starter folder:

```powershell
python resume.py doctor
python resume.py build examples/demo-person --all
python resume.py new personal/my-resume --variant hybrid
```

If `python` opens the Microsoft Store or is not found, try `py -3 resume.py doctor`. Use `py -3` in place of `python` consistently, including editor task commands, or correct PATH to your installed Python. `Get-Command python,pdflatex,pdftotext,pdffonts,pdfinfo` helps locate executable problems.

The CLI recognizes MiKTeX and disables its automatic package installer during compilation. Install missing packages explicitly in MiKTeX Console, then retry. If compiling directly in another tool, its MiKTeX installer policy may differ. On a managed computer, use your organization's approved installation method. See [troubleshooting](troubleshooting.md).

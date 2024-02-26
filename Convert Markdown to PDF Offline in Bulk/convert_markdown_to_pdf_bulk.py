import glob
import subprocess

# Find all files with the .md extension in the current directory
md_files = glob.glob('*.md')

# Writing this line to make the latex part in the md file to work properly in the created pdf
latex_math_fix = '''<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });</script>'''

for filename in md_files:
    with open(filename, 'r+') as file:
        filedata = file.read()
        file.seek(0, 0)
        file.write(latex_math_fix + '\n\n' + filedata)
    subprocess.check_call(['md-to-pdf', filename], shell=True)
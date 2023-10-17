import glob
import subprocess

# Find all files with the .md extension in the current directory
md_files = glob.glob('*.md')

for file in md_files:
    subprocess.check_call(['md-to-pdf',file], shell=True)
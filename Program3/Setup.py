from cx_Freeze import setup, Executable


setup(
    name = "Backup to AWS",
    version = "V 1.0",
    description = "this program will upload your files to an existing or new AWS Bucket. ",
    executables =  [Executable("backup.py")])

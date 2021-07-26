import os
import subprocess

JAVA_OPTS_PATH = "/root/JAVA_OPTS"

def set_java_options():
    opts_raw = None
    with open(JAVA_OPTS_PATH, "r") as f:
        opts_raw = f.read()

    java_opts = opts_raw.split("\n")
    os.putenv("JAVA_OPTS", " ".join(java_opts))

def run_tomcat():
    subprocess.run(["/usr/local/tomcat/bin/catalina.sh", "run"])

def main():
    set_java_options();
    run_tomcat();

if __name__ == "__main__":
    main()

import subprocess
def setup_ssh_tunnel():
    subprocess.run(["gcloud", "--project", "omnisegment", "compute", "ssh", "--zone", "asia-northeast1-c",
                   "omnisegment-rabbitmq-1", "--", "-fNT", "-L", "127.0.0.1:15672:localhost:15672"])

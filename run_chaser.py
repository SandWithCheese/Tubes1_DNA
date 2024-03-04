import random
import string
import subprocess
import shlex

chars = string.ascii_letters

def random_text(length: int) -> str:
    return ''.join(random.choice(chars) for i in range(length))

email = "chaser" + random_text(3)
command = f"python3 main.py --logic Chaser --email={email}@email.com --name={email} --password=123456 --team etimo"
command_list = shlex.split(command)


subprocess.run(command_list)
# subprocess.Popen(command_list, close_fds=True)
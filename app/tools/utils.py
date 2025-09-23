def run_cmd(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    clip = 20000
    return p.returncode, out[-clip:], err[-clip:]

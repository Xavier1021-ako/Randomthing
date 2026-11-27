# kookoo.exe

A Windows desktop survival mini-game inspired by the KooKoo visual.

- Each round chooses a random target from 1–15.
- The counter advances once per second.
- Minimize every other visible application window before the counter reaches the target.
- KooKoo's own game window is excluded from the check.
- The game never closes or changes other apps; it only checks whether their windows are minimized.

## Download the EXE

Open the repository's **Actions** tab, select the latest **Build kookoo.exe** run, and download the **kookoo-windows-exe** artifact.

The workflow builds the Windows executable automatically whenever `kookoo.py` or its workflow changes.

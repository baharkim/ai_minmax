# Setting up on a modern Mac (Apple Silicon or Intel)

The original README's Mac instructions don't work on current macOS. These steps do
(tested on macOS 15, Apple M4 Pro).

**The catch:** `opponent.py` (the AI you play against) is encrypted. Only
`pytransform/platforms/darwin/x86_64/_pytransform.dylib` can decrypt it, and that file
only works with an **Intel** build of **Python 3.6 or 3.7**. So on Apple Silicon we run
an Intel Python 3.7 through Rosetta 2.

Run every command in Terminal from the assignment folder (`cd <assignment folder>`).

## 1. Install Rosetta 2 (Apple Silicon only)

```
softwareupdate --install-rosetta --agree-to-license
```

Lets an Apple Silicon Mac run Intel programs. Harmless if it's already installed.

## 2. Install micromamba

```
brew install micromamba
```

A small conda package manager (needs Homebrew: https://brew.sh). We need it because
conda-forge still has Intel builds of Python 3.7. python.org and uv no longer do.

## 3. Let macOS load the opponent's library

```
xattr -d com.apple.quarantine pytransform/platforms/darwin/x86_64/_pytransform.dylib
```

Files you download or AirDrop get a "quarantine" flag. This library is also unsigned,
so macOS refuses to load it ("_pytransform.dylib Not Opened"; click **Done**, not
*Move to Trash*). This command removes the flag from that one file only. If it says
`No such xattr`, the file wasn't quarantined and you can move on.

## 4. Create the Python environment

```
export MAMBA_ROOT_PREFIX=~/mamba
micromamba create -p "$PWD/.conda" --platform osx-64 -c conda-forge python=3.7.12 pip pyyaml=5.1.1
```

- `MAMBA_ROOT_PREFIX` tells micromamba where to keep its download cache.
- `-p "$PWD/.conda"` puts the environment in a `.conda` folder inside the assignment.
  The path must be absolute; a relative one is treated as a name and ends up elsewhere.
- `--platform osx-64` gets the **Intel** packages, even on Apple Silicon.
- PyYAML comes from conda-forge because pip only has it as source code, which would
  need compiling.

## 5. Install the game's libraries

```
./.conda/bin/python -m pip install --only-binary=:all: -r requirements-macos.txt
```

Installs Kivy 1.11.0 (the graphics library) and numpy 1.16.4, the versions from the
original `requirements.txt`, plus their dependencies at fixed versions.
`--only-binary=:all:` makes pip use ready-made packages only, so nothing gets compiled.

## 6. Check it works

```
./.conda/bin/python -c "import kivy, numpy, yaml, opponent; print('Environment OK')"
```

Should end with `Environment OK`. If `opponent` fails, go back to step 3.

## Running the game

```
./.conda/bin/python main.py settings.yml
```

Change `player_type` / `observations_file` in `settings.yml` as described in README.md.
In an editor (VS Code, PyCharm), choose `<assignment folder>/.conda/bin/python` as the
interpreter.

**Quit with the Esc key.** Closing the window any other way (red button, Cmd-Q)
leaves the game's player process running. The window freezes and the Dock shows two
"not responding" Python icons. To clean up, run in another terminal:

```
pkill -9 -f "main.py settings.yml"
```


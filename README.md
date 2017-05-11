AI-Game aigame
**********

**AI-Game aigame is a toolkit for developing and comparing reinforcement learning algorithms.**


Basics
======

There are two basic concepts in reinforcement learning: the
environment (namely, the outside world) and the agent (namely, the
algorithm you are writing). The agent sends `actions` to the
environment, and the environment replies with `observations` and
`rewards` (that is, a score).

The core `aigame` interface is `Env <https://github.com/Justontheway/aigame/blob/master/aigame/core.py>`_, which is
the unified environment interface and agent interface.
The following are the ``Env`` methods you
should know:

- `reset(self)`: Reset the environment's state. Returns `observation`.
- `step(self, action)`: Step the environment by one timestep. Returns `observation`, `reward`, `done`, `info`.
- `render(self, mode='human', close=False)`: Render one frame of the environment. The default mode will do something human friendly, such as pop up a window. Passing the `close` flag signals the renderer to close any such windows.

Installation
============
On Win7|10
- download ActivePython : http://downloads.activestate.com/ActivePython/releases/2.7.13.2714/ActivePython-2.7.13.2714-win64-x64-402182.exe
- download autopy : https://pypi.python.org/packages/7f/35/a7f1c8c2f2d380c9df73efa56043bf2296e66273074bae37b8625db7b608/autopy-0.51.win-amd64-py2.7.exe#md5=f67dee6f0a30673a2b267dec0431395e
- download aigame : git clone https://github.com/Justontheway/aigame.git
- cd aigame
- python setup.py install
- cd examples
- python random_agent.py

Note
====
1. 因为运行时需要操作window窗口,所以运行脚本的时候要用管理员身份打开cmd

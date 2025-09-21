## MYRAGE

Tool to set up a Tor session for outgoing requests

The `tor`command must be available. If the command is located in a different location, you can symlink it.
Another solution is to use nix-shell `nix-shell -p tor`

To Do:
- [ ] If use_tor is set to False, don't call tor and use local session
- [ ] Make myrage as a context manager

### Version 0.7.0

- #46 & #37 fixed installs on OS X El Capitan. Moved battleschool files to `/usr/local`
- #39 via #40 added `--use-default-callbacks` option to use ansible callbacks for things like prompting vars via @OldhamMade.
- #38 fixed some error printing bugs via @OldhamMade.
- #42 add remaining password options from updated ansible via @dochang.
- #45 updated usage on readme via @vladdancer.

### Version 0.6.1

- #33 extra vars parse error with ansible v1.9.1 via @subsetpark

### Version 0.6.0

- #25 battleschool now supports ansible v1.9.1 and it is required (thanks to @eyadsibai for pointing me to @dochang's initial fix https://github.com/dochang/battleschool/commit/e54ded165dd80060741b844cb2f09877b1b4f6d6).   The new short option for `--update-sources` is `-X`.

### Version 0.5.2

- #28 added script_postfix and script_data params to mac_pkg (for homebrew install)

### Version 0.5.1

- require ansible version <= 1.8.4 see #25 for support of ansible 1.9.x

### Version 0.5.0

- merged #23 by @OldhamMade allow use of battleschool as a library

### Version 0.4.1

- merged #22 by @OldhamMade allow overriding of `battleschool_dir` variable to be passed into `main()`, allowing easier extension of battleschool by external tools.
- error messages that provide better debugging

### Version 0.4.0

- merged #16 by @acaire to fix urls with special characters
- merged #17 by @lndbrg to support newer versions of ansible 1.8+

### Version 0.3.6

- fixes #11 allowing incomplete or missing config.yml (noted by @AnneTheAgile)
- doc fixes by @robyoung 5d8ddff03577146551f3f443202388522837abe3
- fixed os.path.isfile call #9 by @graingert 

### Version 0.3.5

- allow the mac_pkg module to be run outside of battleschool (#7 courtesy of @vascoosx)
- move respository to https://github.com/spencergibb/battleschool

### Version 0.3.4

- added symlinks=True to copytree in AppPackage.install (fixes app installs that have symlinks)
- added jinja2 and pyyaml as setup.py requires to fix installs using homebrew installed pip and python

### Version 0.3.3

- serialize extra_vars to $TMPDIR/battleschool_extra_vars.json so mac_pkg can read options set in battle 5db798827a
- added acquire-only option (useful to prep for demos)
- removed --tags option since not all playbooks will have the same tags

### Version 0.3.2

- added archive_type=tar support bc9180b5fbf

### Version 0.3.1

- fixed bugs introduced if using ansible 1.5

### Version 0.2.2

- Changed the `--update-source` option to `--update-sources`

### Version 0.2.1

- remote config.yml (for first run on a machine)
- url sources
- configurable cache_dir

### Version 0.1.0

- initial open source release
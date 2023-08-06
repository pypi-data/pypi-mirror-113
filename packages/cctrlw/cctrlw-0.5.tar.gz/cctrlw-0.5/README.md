# cctrlw

Configurable Ctrl-W (see gifs to understand what that means).

This project addresses the pitfalls of [xonsh](https://xon.sh/) (a brilliant project) btw builtin Ctrl-W functionality.

What exactly was wrong? There was no way to configure which characters are considered equivalent (and hence, to be deleted on a Ctrl-W keystoke). Say you wanted to edit a 'cd to/a/very/long/path' and press a C-W. Then everything till space is removed, which often is not the desired behaviour.

Ok, so how to configure such a thing? Mathematically such configuration is equivalent to a [partition](https://en.wikipedia.org/wiki/Partition_of_a_set) of the set of all characters. In terms of implementation, [disjoint set union data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) can be used to maintain partitions. Using a DSU is not really a requirement;  however it turns out to be the simplest and cleanest implementation.

See [docstring](https://github.com/ggdwbg/cctrlw/blob/main/cctrlw/algo.py#L166) for `load_partitions` in `cctrlw/algo.py` to understand the approach used to define partitions.

## Default configuration

Default `cw_modes.json` defines the following partitions:

- `S`: singletons
- `ldu`: `{{a..z}, {0..9}, {A..Z}}` (3 nontrivial classes)
- `ldup`: compared to `ldu`: elements of `string.punctuation` are now equivalent (4 nontrivial classes)
- `Ldp`: compared to `ldup`: lower and upper are merged (3 nontrivial classes)
- `Ap`: compared to `Ldp`: digits and letters are merged (2 nontrivial classes)
- `W`: compared to `Ap`: digits and punctuation are merged (1 nontrivial class, but space is not punctuation and still lives in a singleton)

Xonsh default Ctrl-W corresponds to `W` (approximately, because it removes trailing whitespace, which is never done in default config).

You can use your own config and add space to, for example, your custom ldu, then space will be removed automatically (furthermore, `FASFfdsf     dsfsfdsf    ` would turn into `FASF` with a single keystroke). Or do something completely different, that's why it's named config.

## What's included

This module provides a CLI and a xontrib for use with xonsh:
  - CLI: run `python -m cctrlw.cli -h` for details.
  - Xontrib: add `xontrib load xonsh_cctrlw` to your `.xonshrc`

    Controlling state is done through envvars:
      * `$CW_MODE`: active partition; default: `Ap`.
      * `$CW_CONFIG`: active configuration json; default: `<package location>/cw_modes.json`
      * `$CW_DEBUG`: `true` to to see debug messages like what partition is loaded, `false` to disable; default: `false`.

## What could be improved

See `TODOs.txt`. Major ones could be:
  * a (subjectively) better version of `whole-word-jumping`
  * \*sh plugin that uses CLI; originally cli was implemented exactly with that in mind.

    Learning bash/\*sh is not *really* that interesting, so this may never end up done, but maybe fish is not as bad.
  * configurable `__repr__` for `dsu`.

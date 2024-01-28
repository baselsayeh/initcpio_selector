# initramfs selector

Small scripts used to make switching/selecting boot inicpio archives easy

Mainly used with a single kernel image and (this) built initcpio archive where switching either of them is not an easy task (like portable handhelds that uses Android)

The menu selector reads input from `/dev/input` events and is easy to add your own key presses (See buildroot_overlay/menu/events_keybd.conf for example)

## Usage

To use it, you need to build buildroot with multiple packages included, mainly:
- `python3` and `python-pyyaml`
- `xz-utils` utility
- `zstd` utility
- `cpio` utility
- `file` utility
- `kbd` (optional) for font changing

and then build with `make BR2_ROOTFS_OVERLAY=/path/to/buildroot_overlay`

## Config

The selector uses yaml with the following sctructure:
```
menu:
    - Item one
    - Item two
    - Item Three
```

each item must contain the `Name` and `Path` attributes (case sensitive), and an optional `Env` array attribute

See `example_config.conf` for an example config

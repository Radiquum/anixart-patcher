# Compress

Patch is used to compress and remove resources to reduce final apk filesize

## settings (compress.config.json)

- remove_unknown_files: true/false - removes files from decompiled/unknown directory
- remove_unknown_files_keep_dirs: list[str] - keeps specified directories in decompiled/unknown directory
- remove_debug_lines: true/false - removes `.line n` from decompiled smali files
- remove_AI_voiceover: true/false - replaces voiceover of anixa character with a blank mp3
- compress_png_files: true/false - compresses PNG in decompiled/res directory
- remove_drawable_files: true/false - removes some drawable-* from decompiled/res
- remove_language_files: true/false - removes all languages except ru and en

## efficiency

Tested with 9.0 Beta 7

diff = original apk bytes - patch apk bytes

|   Setting    |       Filesize        |        Diff         |   %   |
| :----------- | :-------------------: | :-----------------: |  :-:  |
| None         | 17092 bytes - 17.1 MB |         -           |   -   |
| Compress PNG | 17072 bytes - 17.1 MB |   20 bytes - 0.0 MB | 0.11% |
| Remove files | 17020 bytes - 17.0 MB |   72 bytes - 0.1 MB | 0.42% |
| Remove draws | 16940 bytes - 16.9 MB |  152 bytes - 0.2 MB | 0.89% |
| Remove lines | 16444 bytes - 16.4 MB |  648 bytes - 0.7 MB | 3.79% |
| Remove ai vo | 15812 bytes - 15.8 MB | 1280 bytes - 1.3 MB | 7.49% |
| Remove langs | 15764 bytes - 15.7 MB | 1328 bytes - 1.3 MB | 7.76% |
| All enabled  | 13592 bytes - 13.6 MB | 3500 bytes - 4.8 MB | 20.5% |

# Demo for oembedpy.adapter.mkdocs

## Description

This page is demo about working `oembedpy.adapters.mkdocs`.

## Setup

1. Install `oEmbedPy`.
2. Add plugin `oembedpy` into your MkDocs configuration.

```yaml
plugins:
  - oembedpy
```

## Usage

Write contents that you want to display embed as code-block fenced `oembed`.
Contents in code-block must be written as TOML and are one required key and two optional keys.

### Keys

* `url`: (Required) URL of target content.
* `max_width`: (Optional) Max width of embed content.
* `max_height`: (Optional) Max height of embed content.

## Demo

### URL only

Source:

````markdown
```oembed
url = 'https://bsky.app/profile/attakei.net/post/3l6uxhgm3sz2t'
```
````

Output:

```oembed
url = 'https://bsky.app/profile/attakei.net/post/3l6uxhgm3sz2t'
```

### With size options

Source:

````markdown
```oembed
url = 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
max_width =  640
max_height = 640
```
````

Output:

```oembed
url = 'https://www.youtube.com/watch?v=Oyh8nuaLASA'
max_width =  640
max_height = 640
```

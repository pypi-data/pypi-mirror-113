# pistachio
Pistachio aims to simplify reoccurring tasks when working with the file system.

## Developing

To install pistachio, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

## Install

You can install pistachio by running the following command.

```bash
$ pip install pistachio
```

## Usage

To use pistachio you can inport the module by running the following commands.

```python
>>> import pistachio
```

### Describe

Method to return a description for the resource.

```python
>>> pistachio.describe('README.md')
{'abspath': '/path/to/file/README.md', 'exists': True, 'is_directory': False, 'is_file': True, 'is_symlink': False, 'name': 'README.md'}
```

### Exists

You can confirm if a directory, file or symbolic link exists using the following method.

```python
>>> pistachio.exists('README.md')
True
```

### Is Directory

Is the resource a directory? True or False.

```python
>>> pistachio.is_directory('README.md')
False
```

### Is File

Is the resource a file? True or False.

```python
>>> pistachio.is_file('README.md')
True
```

### Is Symlink

Is the resource a symbolic link? True or False.

```python
>>> pistachio.is_symlink('README.md')
False
```

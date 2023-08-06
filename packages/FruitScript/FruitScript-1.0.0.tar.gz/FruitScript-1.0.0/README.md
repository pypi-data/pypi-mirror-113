# FruitScript

FruitScript is a module with multiple purposes, file management, on the spot being able to use things and maybe a bunch of useless shit that you don't need, lol. 😀

## Installation

`pip install FruitScript`

## Simple Usage

### Importing

Here is a simple way of importing of course.

```py
import ext.FruitScript
from ext.FruitScript import *
```

There is also other useless imports that come from the other files I have like:

```py
import ext.manage
from ext.manage import *
import ext.external
from ext.external import *
```

### Example Code

Here is an example of using FruitScript File Management.

```py
import ext.FruitScript
from ext.FruitScript import fileM

fileM.create('HelloWorld.js') # Creates a file.
fileM.append('HelloWorld.js', 'console.log(\'I am alive.\')') # Appends/Writes/Updates a file with content.
fileM.delete('HelloWorld.js') # Deletes a file.
```

Or possibly the others..

```py
import ext.manage

manage.install() # Installs the FruitScript Module.
```

Or the other functions in ext.manage such as:

``manage.uninstall()`` This will uninstall FruitScript.  
``manage.update()`` This will upgrade FruitScript.

This is the ext.external one.

```py
import ext.external
from ext.external import others

print(others.version()) # Prints out the version number.
print(others.github()) # Prints out the github link.
```

### More
If you would like to find out about more, just go to the link down below..its the documentation of course.  
[Link here.](https://github.com/ItzBlueBerries/FruitScript/tree/main/docs/source/docs)
## Authors/Credits

`Fruitsy - Main Programmer & Founder - (Fruitsy#6513, https://github.com/ItzBlueBerries/)`

## LICENSE

Copyright 2021 Fruitsy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

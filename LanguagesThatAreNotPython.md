# Introduction #

This guide covers windows, since if you can get it working on windows you can get it working on any of the easier OSes.

To run the poker framework on Windows, you'll need Python.  In addition to that, follow the instructions for your language of choice as well.  For C++ and Java, the Python framework uses Google's [Protocol Buffers](http://code.google.com/p/protobuf/) to communicate over stdin and stdout with your bot.  The format is simple: 4 bytes of representing the length of the next message, then the next message, terminated with 4 zero bytes.  This works because there is only one kind of message given to the bot on stdin and one used on stdout.

# Running #

## All Languages ##

If you don't have SVN installed, get [TortoiseSVN](http://tortoisesvn.net/) then use it to check out http://poker-armageddon.googlecode.com/svn/trunk/

Download and install:
  * [Python 2.6.1](http://www.python.org/ftp/python/2.6.1/python-2.6.1.msi)

Run 'main.py' in your checked out repository.

## C++ ##

  1. Download and install:
    * [Download Bloodshed C++](http://prdownloads.sourceforge.net/dev-cpp/devcpp-4.9.9.2_nomingw_setup.exe) (the version without MinGW)
    * [MinGW](http://www.mingw.org/wiki/HOWTO_Install_the_MinGW_GCC_Compiler_Suite) select at least the g++ and Make options in the install and use the candidate version (don't use the one that comes with bloodshed)
      * you have to download [g++](http://downloads.sourceforge.net/mingw/gcc-g%2B%2B-3.4.5-20060117-3.tar.gz?use_mirror=mesh) manually
  1. Set Dev-Cpp to use the installed MinGW (add `c:\mingw\bin` to your PATH environment variable)
  1. Build example bot in `example_bots/java/foldbot`, comes with a Dev-Cpp project that should just work out of the box.
  1. Edit main.py to use your bot

## Java ##

  1. Download and install:
    * [Download Netbeans (Java bundle)](http://www.netbeans.org/downloads/index.html) and install it unless you have your own compiler.
    * [Java JDK](http://java.sun.com/javase/downloads/index.jsp)
  1. Build example project in `example_bots/java/foldbot`
  1. Edit main.py to use your bot

# Building the Libraries #

## C++ ##

  1. Run the MSYS link on your desktop.
  1. Put the protobuf sourcecode in `C:\msys\1.0\home\<username>`.  No spaces in the path.
  1. Follow the REAME file instructions for installing on Unix.  configure, make etc.
  1. After the "make install" copy the libprotobuf files to a place where you can include them in your project.

## Java ##

  1. No building required, just use the .class files in {{{protocol/java/lib}}
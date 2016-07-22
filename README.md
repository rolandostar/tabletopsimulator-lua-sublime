# Tabletop Simulator Lua Plugin for Sublime Text


A plugin for Sublime Text to load and write Lua Scripts for Tabletop Simulator.

![Image of Yaktocat](http://i.imgur.com/Dez51kH.png)
Featured Theme is [PlasticCodeWrap](https://github.com/joedf/PlasticCodeWrap)

## Features

1. Get Scripts
2. Send Scripts

That's it. I'll work on stuff like console output and Get Scripts on reload and such but for now this simple plugin will do.

## Quick Installation

You can install this plugin through [Package Control](https://packagecontrol.io/installation)

Step-By-Step:
1. Press “Ctrl + Shift + P” to open the Command Palette
2. Type “Install Package” and select "Package Control: Install Package"
3. Search for “Tabletop Simulator Lua” and press enter
4. [Optional] Search and install for "Folder2Project" v0.1.5 by divinites (You'll need to modify the config to use it)


## Manual Installation

Download the latest release.

These files should be placed into the "Tabletop Simulator Lua" package directory. This can be found at:

`C:\Users\[USERNAME]\AppData\Roaming\Sublime Text 3\Packages\Tabletop Simulator Lua`

## How to Use

Once installed you should see a menu at the top labeled "Tabletop Simulator"

**"Get Lua Scripts" (Ctrl + Alt + Space):**
This will open a connection with the game and request all scripts to be loaded into Sublime.
  
**"Save and Play" (Ctrl + Alt + S):**
This will send all *currently saved* scripts to TTS - I suggest enabling

	"save_on_focus_lost": true
On your Sublime configuration file

## Configuration

The only configuration is to wether open all files on tabs or open the folder where all the files are stored.

![Difference](http://i.imgur.com/7avYSuy.png)

You'll can find this file in (Preferences > Package Settings > Tabletop Simulator > Settings - Default)

	{
		// When getting files from the game should they all be opened?
		"open_all_files": 0

		// Changing this to 1 will try to use the plugin "Folder2Project" by divinites
		// if the plugin is not found it'll create the files but they won't be opened.

		// Files are stored in /Packages/Lua (Preferences > Browse Packages...)
	}

To modify it you'll need to open a new config file (Preferences > Package Settings > Tabletop Simulator > Settings - User)

And change "open_all_files" to 1

	{
		"open_all_files": 1
	}
## About

I created this project since Atom was crashing all the time for me, I have no prior knowledge of Python and was my first time using the Sublime Plugin API so please forgive this hacked up together plugin.

It was created in a day and copy-pasting whatever I found worked all around tutorial sites.

I will appreacciate any contributions and improvements that anyone can come up with.

### Contact

You can find me on [Steam](http://steamcommunity.com/id/rolandostar/) and [Reddit](https://www.reddit.com/user/rolandostar)!

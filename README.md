# Fourhills

Fourhills allows dungeon masters of role-playing games to organise and quickly access
information about their world through a command-line interface. The world, and
related information such as NPC details, monster statistics, and cheatsheets, is
described in a succinct directory structure. The dungeon master then navigates
through the world by navigating through the directory structure, and can view
relevant information by executing Fourhills in the current directory.

Key features:
* Define the world in a concise directory structure
* Put NPCs in world locations, and quickly access their descriptions and common phrases
* Build "battles" at specific locations, allowing NPC and monster stat blocks to be
  displayed with a command
* Write "cheatsheets" with useful commonly-used information (such as beer prices,
  rules for travelling through water environments, etc.) and access them with a command

## Installing Fourhills

1. Make sure you have [Python 3.7 or greater](https://www.python.org/downloads/)
  installed.
2. Optional (but recommended): create a Python virtual environment.
    * Open a terminal and navigate to a suitable location (e.g. near to the directory
        you're creating your world in, or in a subdirectory of your home directory).
    * Execute the following commands:
        ```bash
        virtualenv venv
        source venv/bin/activate  # For Mac/Linux
        venv/Scripts/activate  # For Windows
        ```
3. Install Fourhills:
    ```bash
    pip install .  # Installs all packages and allows 'fourhills' and 'fh' to execute program
    ```
4. Test whether it's working by typing `fh --help`

## Running Fourhills

When you want to run fourhills:
1. Open a terminal
2. If you created a virtual environment, activate it by navigating to the directory
    you created it in and typing:
    ```bash
    source venv/bin/activate  # For Mac/Linux
    venv/Scripts/activate  # For Windows
    ```
3. Navigate into a location within your world. See the "Creating the World" section
    below on how to make one.
4. Run Fourhills:
    ```bash
    fh scene # Display information about the scene at the current location, such as which NPCs and monsters are there, and the total XP for all of them
    fh npcs # Display details of the NPCs at the current location, excluding battle stats
    fh battle # Display battle stats for all monsters and NPCs at the current location
    fh cheatsheet <cheatsheet_name> # Display <cheatsheet_name>. Don't include the .yaml file extension at the end of the cheatsheet name.
    fh cheatsheet --list # List all available cheatsheets. Alias: fh cheatsheet -l
    fh --help # Show help
    fh --version # Show the program version
    ```

All of the top-level commands can also be accessed with a unique prefix, e.g. `fh s`
is an alias for `fh scene`.

This is also true of cheatsheet names. If you have a cheatsheet called
"water_environments.yaml" then you can display it with `fh c w`, as long as there are
no other cheatsheets starting with "w". If there are, you just need to specify enough
characters to differentiate between them; for example, if there is a cheatsheet
called "weight_carrying_limits.yaml" then you could to type `fh c wa` to display the
first one, and `fh c we` to display the second.

## Creating the World

The following sections describe how to create the directory structure and files that
define the world.

You can see an example in the
[ExampleWorld directory](https://github.com/smuj/Fourhills/tree/master/ExampleWorld).

### Directory Structure

Create a top-level directory to store your world, and create an empty file called
"fh_setting.yaml". Then, add the following directories:
* world
* monsters
* npcs
* cheatsheets

The directory structure should look like this:

```
├── fh_setting.yaml
├── cheatsheets
├── monsters
├── npcs
└── world
```

The contents of each directory is covered in the following sections.

### World directory

The "world" directory is a hierachical description of the world. So, if the main
top-level features of your world are a city called Fourhills, a town called Quarterwick,
some woods called The Winding Woods, and an important road called Quarterwick Road,
then you might have the following top-level directories:
* Fourhills/
* Quarterwick/
* TheWindingWoods/
* QuarterwickRoad/

You can create locations within those locations by adding subdirectories. For example,
if Fourhills has a tavern called The Kobold's Lantern, you can create a subdirectory
called TheKoboldsLantern/.

In order to add NPCs or monsters to a location, create a file called scene.yaml in
the directory. This file says which NPCs and monsters are at the location. For
example:
```yaml
npcs:
  - gruumsh_the_lesser
monsters:
  - dryad_assassin
  - cult_fanatic x6
```

This shows that there is an NPC and seven monsters, six of which are the same type
of monster.

NPC and monster names should exactly match a filename in the "npcs" and "monsters"
folders respectively, excluding the file extension. For more information on how to
create NPC and monster files, see the relevant sections below.

You don't have to create a scene.yaml file at every location, and you're free to add
whatever other files you want. Here are some examples of other files you could include:
* A text or markdown file describing what the location looks like
* A text or markdown file about the location's history
* An image file with a map of the location
* A battle grid
* An audio file with some music, to be played during a battle

The Fourhills program won't interact with these files, but by putting them in the right
directory, you can access them easily when you're at that location.

### Monsters directory

The "monsters" directory contains battle stat blocks for monsters.

There's a template containing all the possible options, with comments describing
them, in
[ExampleWorld/monsters/example_monster.yaml](https://github.com/smuj/Fourhills/blob/master/ExampleWorld/monsters/example_monster.yaml).

### NPCs directory

The "npcs" directory contains NPC descriptions.

NPC files can optionally link battle stats for a monster; for example, if an NPC is a
human and you have created a monster file called "human.yaml", you can include
`stats_base: human` in the NPC file.

There's a template containing all the possible options, with comments describing
them, in
[ExampleWorld/npcs/example_npc.yaml](https://github.com/smuj/Fourhills/blob/master/ExampleWorld/npcs/example_npc.yaml).

### Cheatsheets directory

The "cheatsheets" directory contains cheatsheets with useful information that you
might want to access from any location. For example, you might have a cheatsheet
describing rules for how players move in water environments. Rather than copying this
information to all locations with water environments, by turning it into a cheatsheet,
you can access it form anywhere.

There's a template containing all the possible options, with comments describing
them, in
[ExampleWorld/cheatsheets/example_cheatsheet.yaml](https://github.com/smuj/Fourhills/blob/master/ExampleWorld/cheatsheets/example_cheatsheet.yaml).

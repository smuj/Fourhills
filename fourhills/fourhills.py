import sys
from fourhills import Scene

SCENE_FILENAME = "scene.yaml"


def print_usage():
    raise NotImplementedError


def main():
    try:
        scene = Scene.from_file(SCENE_FILENAME)
    except FileNotFoundError:
        print("No scene file at this location")
        sys.exit()
    if len(sys.argv) > 1:
        if sys.argv[1] in ["b", "battle"]:
            scene.display_battle()
        elif sys.argv[1] in ["n", "npc", "npcs"]:
            scene.display_npcs()
        elif sys.argv[1] in ["s", "scene"]:
            scene.display_scene()
        elif sys.argv[1] in ["c", "cs", "cheatsheet"]:
            scene.display_cheatsheet(sys.argv[2])
        else:
            print_usage()
    else:
        scene.display_scene()


if __name__ == "__main__":
    main()

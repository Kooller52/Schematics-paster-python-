from litemapy import Schematic
import versions as ver
import group
import shutil

inp = input("enter the path to the file (.schem,.litematic...) (full or relative to main.py): ")
schem = Schematic.load(inp)
if ver.find(schem.mc_version) != None:
    print(f"Schematic version: {ver.find(schem.mc_version)}")
else:
    print("Failed finding schematic version")
print("Warning! If the schematic contains blocks that are not present in the version on which you will paste the structure, the function will simply not be displayed in the game!")
path0 = input("Enter the path to the world in which you want to place the structure: ")
shutil.copytree("schem", f"{path0}\\datapacks\\schem", dirs_exist_ok=True)
blocks = []
regions = list(schem.regions.values())
for reg in regions:
    for x in reg.xrange():
        for y in reg.yrange():
            for z in reg.zrange():
                blocks.append([[x-reg.x,y-reg.y,z-reg.z], str(reg[x,y,z])])
path = f"{path0}\\datapacks\\schem\\data\\schem\\functions\\schem.mcfunction"
pos = list(map(lambda t: int(t), input("Enter a position for the placement of the schematic (x y z separated by spaces OR commas [DONT WRITE SMTH LIKE \"x, y, z\"!]): ").replace(" ", ",").split(",")))
print("If you are going to insert a large structure with repeating blocks, you should set /gamerule commandModificationBlockLimit 2147483647 (or any big number)(1.19.4+) or dont use group fill mode")
mode = input("Use group fill mode? (recommended) [Y/N]: ")
print("-converting...")
func = open(path, "w")
func.write(f"title @a title \"start\"\n")
func.write(f"fill {pos[0]} {pos[1]} {pos[2]} {pos[0]+schem.width-1} {pos[1]+schem.height-1} {pos[2]+schem.length-1} minecraft:air\n")
if mode.lower() == "n":
    for block in blocks:
        if block[1] != "minecraft:air":
            func.write(f"setblock {block[0][0]+pos[0]} {block[0][1]+pos[1]} {block[0][2]+pos[2]} {block[1]}\n")
else:
    fa, sa = group.findgroups(blocks)
    for ft in fa:
        for ftb in fa[ft]:
            if ft != "minecraft:air":
                func.write(f"fill {ftb[0]+pos[0]} {ftb[1]+pos[1]} {ftb[2]+pos[2]} {ftb[3]+pos[0]} {ftb[4]+pos[1]} {ftb[5]+pos[2]} {ft}\n")
    for st in sa:
        for stb in sa[st]:
            if st != "minecraft:air":
                func.write(f"setblock {stb[0]+pos[0]} {stb[1]+pos[1]} {stb[2]+pos[2]} {st}\n")
func.write(f"title @a title \"done!\"")
print("-generated!")
func.close()
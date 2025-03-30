from collections import defaultdict

def findgroups(blocks):
    types = defaultdict(list)
    for block in blocks:
        pos, blocktype = block
        types[blocktype].append(pos)
    resFill = defaultdict(list)
    resSet = defaultdict(list)
    for blocktype, blocklist in types.items():
        blockset = set(tuple(pos) for pos in blocklist)
        visited = set()

        for block in blocklist:
            x, y, z = block
            if (x, y, z) in visited:
                continue

            minx = maxx = x
            miny = maxy = y
            minz = maxz = z

            can = True
            while can:
                nextx = maxx + 1
                valid = True
                for ycheck in range(miny, maxy + 1):
                    for zcheck in range(minz, maxz + 1):
                        if (nextx, ycheck, zcheck) not in blockset:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    maxx = nextx
                else:
                    can = False
            can = True
            while can:
                nexty = maxy + 1
                valid = True
                for xcheck in range(minx, maxx + 1):
                    for zcheck in range(minz, maxz + 1):
                        if (xcheck, nexty, zcheck) not in blockset:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    maxy = nexty
                else:
                    can = False

            can = True
            while can:
                nextz = maxz + 1
                valid = True
                for xcheck in range(minx, maxx + 1):
                    for ycheck in range(miny, maxy + 1):
                        if (xcheck, ycheck, nextz) not in blockset:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    maxz = nextz
                else:
                    can = False

            if (minx == maxx) and (miny == maxy) and (minz == maxz):
                resSet[blocktype].append((minx, miny, minz))
            else:
                resFill[blocktype].append((minx, miny, minz, maxx, maxy, maxz))

            for xrect in range(minx, maxx + 1):
                for yrect in range(miny, maxy + 1):
                    for zrect in range(minz, maxz + 1):
                        visited.add((xrect, yrect, zrect))

    return [dict(resFill), dict(resSet)]
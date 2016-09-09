import mcpi.minecraft as minecraft
import mcpi.block as block

mc = minecraft.Minecraft.create()

r = 10

cur_x , cur_y , cur_z = mc.player.getPos()

for x in range(r*-1,r):
	for y in range(r*-1, r):
		for z in range(r*-1,r):
			if x**2 + y**2 + z**2 < r**2:
				mc.setBlock(cur_x + x, cur_y + ( y + 20 ) , cur_z - ( z + 20 ) , block.GOLD_BLOCK)
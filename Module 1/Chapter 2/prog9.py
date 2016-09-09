import mcpi.minecraft as minecraft
import mcpi.block as block
import time

mc = minecraft.Minecraft.create()

while 1:
	cur_x, cur_y , cur_z = mc.player.getPos()
	mc.setBlock(cur_x,cur_y-1,cur_z,block.GOLD_BLOCK.id)
	time.sleep(0.1)
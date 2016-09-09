import mcpi.minecraft as minecraft
import mcpi.block as block
mc = minecraft.Minecraft.create()
cur_x , cur_y , cur_z = mc.player.getPos()

for i in range (0 , 15):
	mc.setBlock(cur_x + 1 , cur_y + i , cur_z , block.WOOL.id, i )

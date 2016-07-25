
import sys
import random
import math

class ShareBlockInfo():
	def __init__(self):
		self.block_num = None
		self.overwritten_flag = False

class BlockInfo():
	def __init__(self):
		self.share_blocks = []

def file_add_shares(file_blocks, k, max_blocks):
	block_info = BlockInfo()

	for i in range(0, k):
		rnd_block = random.randint(0, max_blocks)
		share_block = ShareBlockInfo()
		share_block.block_num = rnd_block
		block_info.share_blocks.append(share_block)
	file_blocks.append(block_info)

def overwrite_block(file_blocks, block_num):
	i = 0
	for file_block in file_blocks:
		x = 0
		for share_block in file_block.share_blocks:
			if share_block.block_num == block_num:
				file_blocks[i].share_blocks[x].overwritten_flag = True
			x+=1
		i+=1		
				
def simulate_overwrite_blocks(population_num_blocks, ratio_population_overwritten, file_size_blocks, n, k):

	file_blocks = []

	for i in range(0, file_size_blocks):
		file_add_shares(file_blocks, k, population_num_blocks)

	population_num_blocks_overwritten = int(math.ceil(population_num_blocks * ratio_population_overwritten))
	for i in range(0, population_num_blocks_overwritten):
		rnd_block = random.randint(0, population_num_blocks_overwritten)	
		overwrite_block(file_blocks, rnd_block)

	for file_block in file_blocks:
		num_overwritten = 0
		for share_block in file_block.share_blocks:
			if share_block.overwritten_flag == True:
				num_overwritten+=1
			if num_overwritten > n:
				return 0
	return 1

def engine(population_num_blocks, ratio_population_overwritten, file_size_blocks, n, k, iterations):
	survive_ratio = 0.0
	survive_counter = 0
	for i in range(0, iterations):
		ret = simulate_overwrite_blocks(population_num_blocks, ratio_population_overwritten, file_size_blocks, n, k)
		if ret == 1:
			survive_counter += 1	

	survive_ratio = float(survive_counter) / float(iterations)

	print "{0}, {1}, {2}, {3}, {4}, {5}".format(population_num_blocks, ratio_population_overwritten, file_size_blocks, n, k, survive_ratio)	

def main():

	#
	# TEST 0: VARIABLE - OVERWRITTEN RATIO
	#

	population_num_blocks = 10000 #2147483648
	file_size_blocks = 2048
	n = 3
	k = 6
	iterations = 1000	

	for i in range(1, 10):
		engine(population_num_blocks, i/100.0, file_size_blocks, n, k, iterations)


if __name__ == "__main__":
	main()

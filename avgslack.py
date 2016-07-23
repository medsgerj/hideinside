
import sys
import os
import stat

def main():

	path = sys.argv[1]

	statvfs = os.statvfs(path)

	fs_block_size = statvfs.f_frsize

	num_files = 0
	total_num_files = 0
	total_slack_space_bytes = 0

	for root, dirs, files in os.walk(path):
		for name in files:
			try:
				pathname = os.path.join(root, name)
				file_stats = os.lstat(pathname)
				mode = file_stats.st_mode
			
				if stat.S_ISREG(mode):
					file_size_bytes = file_stats.st_size

					#if file_size_bytes == 0 and file_stats.st_blocks == 0:
					#	print "Zero file: {0}".format(pathname)

					if file_size_bytes % fs_block_size == 0:
						slack_space = 0
					else:
						slack_space = fs_block_size - (file_size_bytes % fs_block_size)
						num_files += 1
					total_num_files += 1
					total_slack_space_bytes += slack_space
			except Exception as e:
				sys.stderr.write("Error accessing {0}\n".format(pathname))

	avg_slack_space_bytes = float(total_slack_space_bytes) / float(num_files)
	perc_slack_space = 100.0 * float(avg_slack_space_bytes) / float(fs_block_size)
	avg_slack_space_true_bytes = float(total_slack_space_bytes) / float(total_num_files)
	perc_slack_space_true = 100.0 * float(avg_slack_space_true_bytes) / float(fs_block_size)

	print "avg_slack_space_bytes={0}, perc_slack_space={1}, num_files={2}, avg_slack_space_true_bytes={3}, perc_slack_space_true={4}, total_num_files={5}".format(avg_slack_space_bytes, perc_slack_space, num_files, avg_slack_space_true_bytes, perc_slack_space_true, total_num_files)

if __name__ == "__main__":
	main()


python runtest.py ../../../fs_tmpfs/testfile 8 | tee mmap_tmpfs_shared_populate.log
python runtest.py ../../../fs_pmfs/testfile 8 | tee mmap_pmfs_shared_populate.log
python runtest.py ../../../fs_default/testfile 8 | tee mmap_ext4_shared_populate.log

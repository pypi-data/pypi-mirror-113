#
# step_2_wd = '/Users/songweizhi/Desktop/tunning_rd2_Oral'
# free_living_ctg_ref_file_with_cigar = '%s/file_in/round2_free_living_ctg_refs_with_cigar.txt' % step_2_wd
#
# mini_ctg_side_cigar_dict = dict()
# for each_read_to_ctg_ref in open(free_living_ctg_ref_file_with_cigar):
#     each_read_to_ctg_ref_split = each_read_to_ctg_ref.strip().split('\t')
#     read_id = each_read_to_ctg_ref_split[0]
#     ctg_refs = each_read_to_ctg_ref_split[1].split(',')
#     for each_ctg_ref in ctg_refs:
#         ctg_ref_id = each_ctg_ref.split('__cigar__')[0]
#         ctg_ref_cigar = each_ctg_ref.split('__cigar__')[1]
#         read_to_ctg_ref_key = '%s__ctg__%s' % (read_id, ctg_ref_id)
#         mini_ctg_side_cigar_dict[read_to_ctg_ref_key] = ctg_ref_cigar
#
# print(mini_ctg_side_cigar_dict)
#
# # S19_13968912.2__ctg__Oral_57___C___NODE_21660_length_2764_cov_1.444444_l
# # S19_13969519.1__ctg__Oral_1___C___NODE_9415_length_5606_cov_0.290929_l
#

done_file = '/Users/songweizhi/Desktop/done.txt'
cmd_file  = '/Users/songweizhi/Desktop/MAG_with_CFP_pcofg_blastn_commands.txt'

done_mag_list = set()
for each in open(done_file):
    done_mag_list.add(each.strip())
print(len(done_mag_list))

for each_line in open(cmd_file):
    mag_id = each_line.strip().split('.ffn -db ')[0].split('/')[-1]
    if mag_id not in done_mag_list:
        print(each_line.strip())




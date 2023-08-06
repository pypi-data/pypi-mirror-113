
class LinkingRecord:

    def __init__(self):

        self.linked_seq_l = ''
        self.linked_seq_r = ''

        self.linked_seq_len_l = 0
        self.linked_seq_len_r = 0

        self.linking_reads_base = []

        self.linking_reads_l = []
        self.linking_reads_r = []

        self.linking_cigar_l = []
        self.linking_cigar_r = []

        self.linking_pos_l = []
        self.linking_pos_r = []

        self.min_dist_to_end_l = []
        self.min_dist_to_end_r = []


def get_min_dist_to_ref_end(cigar_str, cigar_pos, ref_len):
    cigar_aln_len = get_cigar_aln_len(cigar_splitter(cigar_str))
    cigar_dist_to_left = cigar_pos - 1
    cigar_dist_to_right = ref_len - cigar_pos - cigar_aln_len + 1
    min_dist_to_mini_end = min(cigar_dist_to_left, cigar_dist_to_right)
    return min_dist_to_mini_end


def add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                      ref_dict_16s, ref_dict_16s_from,
                                      ref_dict_ctg, ref_dict_ctg_from,
                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                      marker_to_ctg_gnm_Key_connector):

    for each_16s_ref in ref_dict_16s:
        for each_ctg_ref in ref_dict_ctg:
            marker_to_ctg_key = '%s%s%s' % (each_16s_ref, marker_to_ctg_gnm_Key_connector, each_ctg_ref)

            if marker_to_ctg_key not in marker_to_ctg_LinkingRecord_dict:
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key] = LinkingRecord()
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_l = each_16s_ref
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_r = each_ctg_ref
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_len_l = marker_len_dict[each_16s_ref]
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_len_r = ctg_len_dict[each_ctg_ref]

            marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_reads_base.append(qualified_read)

            if ref_dict_16s_from in ['r1', 'shared']:
                marker_side_cigar_r1 = list(MappingRecord_dict[qualified_read].r1_16s_ref_dict[each_16s_ref].values())[0]
                marker_side_cigar_pos_r1 = list(MappingRecord_dict[qualified_read].r1_16s_ref_dict[each_16s_ref].keys())[0]
                marker_side_cigar_r1_min_end_dist = get_min_dist_to_ref_end(marker_side_cigar_r1, marker_side_cigar_pos_r1, marker_len_dict[each_16s_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_l.append(marker_side_cigar_pos_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_l.append(marker_side_cigar_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_l.append(marker_side_cigar_r1_min_end_dist)

            if ref_dict_16s_from in ['r2', 'shared']:
                marker_side_cigar_r2 = list(MappingRecord_dict[qualified_read].r2_16s_ref_dict[each_16s_ref].values())[0]
                marker_side_cigar_pos_r2 = list(MappingRecord_dict[qualified_read].r2_16s_ref_dict[each_16s_ref].keys())[0]
                marker_side_cigar_r2_min_end_dist = get_min_dist_to_ref_end(marker_side_cigar_r2, marker_side_cigar_pos_r2, marker_len_dict[each_16s_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_l.append(marker_side_cigar_pos_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_l.append(marker_side_cigar_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_l.append(marker_side_cigar_r2_min_end_dist)

            if ref_dict_ctg_from in ['r1', 'shared']:
                ctg_side_cigar_r1 = list(MappingRecord_dict[qualified_read].r1_ctg_ref_dict[each_ctg_ref].values())[0]
                ctg_side_cigar_pos_r1 = list(MappingRecord_dict[qualified_read].r1_ctg_ref_dict[each_ctg_ref].keys())[0]
                ctg_side_cigar_r1_min_end_dist = get_min_dist_to_ref_end(ctg_side_cigar_r1, ctg_side_cigar_pos_r1, ctg_len_dict[each_ctg_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_r.append(ctg_side_cigar_pos_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_r.append(ctg_side_cigar_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_r.append(ctg_side_cigar_r1_min_end_dist)

            if ref_dict_ctg_from in ['r2', 'shared']:
                ctg_side_cigar_r2 = list(MappingRecord_dict[qualified_read].r2_ctg_ref_dict[each_ctg_ref].values())[0]
                ctg_side_cigar_pos_r2 = list(MappingRecord_dict[qualified_read].r2_ctg_ref_dict[each_ctg_ref].keys())[0]
                ctg_side_cigar_r2_min_end_dist = get_min_dist_to_ref_end(ctg_side_cigar_r2, ctg_side_cigar_pos_r2, ctg_len_dict[each_ctg_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_r.append(ctg_side_cigar_pos_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_r.append(ctg_side_cigar_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_r.append(ctg_side_cigar_r2_min_end_dist)


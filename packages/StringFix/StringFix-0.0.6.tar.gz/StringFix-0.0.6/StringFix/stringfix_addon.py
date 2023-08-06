##################################################################################
## StringFix-addon                                                              ##
## developed by Seokhyun Yoon (syoon@dku.edu) Oct. 04, 2020                     ##
##################################################################################

import time, re, os, copy, collections, datetime, queue, math, pickle, subprocess
import numpy as np
import pandas as pd
from scipy import optimize 

import stringfix_core as sf

def which( ai, value = True ) :
    wh = []
    a = list(ai)
    for k in range(len(a)): 
        if a[k] == value: 
            wh.append(k) 
    return(wh)

def get_info_from_tr_name( tns ):
    
    abn_e = []
    tpm_e = []
    ifrac = []
    sidx = []
    g_size = []
    n_exons = []
    g_vol = []
    icnt = []
    t_len = []
    strnd = []
    cdng = []
    for k, tn in enumerate(tns):
        hdr = tn.split(' ')
        items = hdr[0].split('_')
        strnd.append( items[2])
        cdng.append( items[3])
        sidx.append( (items[4]) )
        g_size.append( int(items[5]) )
        icnt.append( int(items[6]) )
        val = items[7].split(':')
        abn_e.append( float(val[1]) )
        val = items[8].split(':')
        tpm_e.append( float(val[1]) )
        val = items[9].split(':')
        ifrac.append( float(val[1]) )
        val = items[11].split(':')
        n_exons.append( int(val[1]) )
        val = items[12].split(':')
        g_vol.append( int(val[1]) )
        val = items[13].split(':')
        t_len.append( int(val[1]) )
    
    df = pd.DataFrame()
    
    df['tr_name'] = tns
    df['abn_est'] = abn_e
    df['tpm_est'] = tpm_e
    df['gidx'] = sidx
    df['iidx'] = icnt
    df['g_size'] = g_size
    df['iso_frac'] = ifrac
    df['n_exons'] = n_exons
    df['g_vol'] = g_vol
    df['length'] = t_len
    df['strand'] = strnd
    df['C_or_N'] = cdng
    
    df = df.set_index('tr_name')
    
    return df

def get_performance(trinfo, cvg_th = [80,90,95], f_to_save = None, ref = 0, verbose = False):
    
    #'''
    if ref == 0:
        q_cvg = 'qcvg'
        q_len = 'qlen'
        q_id = 'qid'
        s_start = 'sstart'
        s_end = 'send'
        s_id = 'sid'
    else:
        q_cvg = 'scvg'
        q_len = 'slen'
        q_id = 'sid'
        s_start = 'qstart'
        s_end = 'qend'
        s_id = 'qid'
    #'''
    
    qids = pd.unique(trinfo[q_id])
    sids = pd.unique(trinfo[s_id])
    wgt = np.zeros([len(qids),len(sids)])
    if verbose: print('Matching (%i,%i) ' % (wgt.shape), end='')

    qidx = np.full(trinfo.shape[0],-1,dtype=int)
    for k in range(len(qids)) :
        qid = qids[k]
        wh = which( trinfo[q_id] == qid )
        qidx[wh] = k
        
    if verbose: print('.', end='')
    sidx = np.full(trinfo.shape[0],-1,dtype=int)
    for k in range(len(sids)) :
        sid = sids[k]
        wh = which( trinfo[s_id] == sid )
        sidx[wh] = k
        
    if verbose: print('.', end='')
    for w in range(len(qidx)):
        wgt[int(qidx[w]), int(sidx[w])] = -trinfo[q_cvg][w]

    if verbose: print('_', end='')
    # print(wgt.shape)
    row_idx, col_idx = optimize.linear_sum_assignment(wgt)
    
    if verbose: print('.', end='')
    df_lst = []
    for k in range(len(col_idx)) :
        si = col_idx[k]
        wh = which(sidx == si)
        w = which( qidx[wh] == row_idx[k] )
        if len(w) > 0:
            if len(w) > 1: print('ERROR in get_performance(): Len(w) = %i' % len(w) )
            idx = wh[w[0]]
            df_lst.append(trinfo.iloc[idx])
        
    df_sel = pd.DataFrame(df_lst)
    if f_to_save is not None:
        fname = '%s_blast_result.csv' % f_to_save
        df_sel.to_csv(fname, header=True, index=False, sep='\t')
        # if verbose: print(' %s.' % fname, end='' )
    
    if verbose: print('.', end='')
    cnt = np.zeros(len(cvg_th))
    for k in range(len(cvg_th)):
        th = cvg_th[k]
        wh = which( df_sel[q_cvg]*100 >= th )
        cnt[k] = np.int(len(wh))
        
    if verbose: print(' done.')

    d = {'cvg_th': cvg_th, 'N_recovered': cnt.astype(int), 'precision': np.round(100*cnt/len(sids),1)}
    df_perf = pd.DataFrame(data = d) #, columns = ['cvg_th','n_recovered','precision'])
    
    return(df_perf, df_sel)

    
def run_blast( inpt_fa, ref_fa, path_to_blast = None, trareco = True, ref_info = False, \
                 dbtype = 'nucl', ref = 0, sdiv = 10, mx_ncand = 6, verbose = False):

    #'''
    if ref == 0:
        ref_tr = ref_fa
        inpt_tr = inpt_fa
        
        q_cvg = 'qcvg'
        q_len = 'qlen'
        q_id = 'qid'
        s_start = 'sstart'
        s_end = 'send'
        s_id = 'sid'
    else:
        ref_tr = inpt_fa
        inpt_tr = ref_fa
        
        q_cvg = 'scvg'
        q_len = 'slen'
        q_id = 'sid'
        s_start = 'qstart'
        s_end = 'qend'
        s_id = 'qid'
    #'''
    
    file_names = inpt_tr.split('.')
    fname = ''.join(st for st in file_names[:-1] )

    tn_in = []
    f = open(inpt_tr,'r')
    cand_cnt = 0
    for line in f:
        if line[0] == '>':
            tn_in.append(line[1:-1])
            cand_cnt += 1
    f.close()
    
    tn_ref = []
    f = open(ref_tr,'r')
    ref_cnt = 0
    for line in f:
        if line[0] == '>':
            tn_ref.append(line[1:-1])
            ref_cnt += 1
    f.close()
    # print('Len: %i, Nu= %i' % (len(tn), len(pd.unique(tn))), end='' )
    
    if ref == 0:
        tn = tn_in
        n_max_cands = 1
    else:
        tn = tn_ref
        n_max_cands =  mx_ncand
        tmp = cand_cnt
        cand_cnt = ref_cnt
        ref_cnt = tmp
    
    ## make blast db with input_tr
    if path_to_blast is None:
        cmd = 'makeblastdb -in %s -dbtype %s' % (inpt_tr, dbtype)
    else:
        cmd = '%s/makeblastdb -in %s -dbtype %s' % (path_to_blast, inpt_tr, dbtype)
    res = subprocess.check_output(cmd, shell=True)
    # print(res.decode('windows-1252'))
 
    str_option = '-outfmt "6 qseqid sseqid qlen length slen qstart qend sstart send nident mismatch gapopen qcovs qcovhsp bitscore" -num_threads 4 -max_target_seqs %i' % n_max_cands

    if dbtype == 'nucl': prfx = 'n'
    else: prfx = 'p'
        
    if path_to_blast is None:
        cmd = 'blast%s %s -db %s -query %s -out %s.tblst' % (prfx, str_option, inpt_tr, ref_tr, fname)
    else:
        cmd = '%s/blast%s %s -db %s -query %s -out %s.tblst' % (path_to_blast, prfx, str_option, inpt_tr, ref_tr, fname)
        
    if verbose: print("Running Blast-%s with %i cand. %i ref. ... " % (dbtype[0].upper(),cand_cnt, ref_cnt), end='', flush=True);
    res = subprocess.check_output(cmd, shell=True)
    # print(res.decode('windows-1252'))
    if verbose: print('done.')
    
    os.remove( '%s.%shr' % (inpt_tr, prfx) )
    os.remove( '%s.%sin' % (inpt_tr, prfx) )
    os.remove( '%s.%ssq' % (inpt_tr, prfx) )
   
    colnames = ['qid', 'sid', 'qlen', 'alen', 'slen', 'qstart', 'qend', 'sstart', 'send', \
                'nident', 'mismatch', 'gapopen', 'qcovs', 'qcovhsp', 'bitscore']
    tblst = '%s.tblst' % fname
    df = pd.read_csv(tblst, header = 'infer', names = colnames, sep='\t')
    
    os.remove( '%s' % (tblst) )
    
    if verbose: print('N.cand: %i, N.subject.unique: %i' % (len(tn), len(pd.unique(df['sid']))) )

    df['scvg'] = df['alen']/df['slen']
    df['qcvg'] = df['alen']/df['qlen']
        
    if trareco == True:
        abn_e = []
        tpm_e = []
        ifrac = []
        sidx = []
        g_size = []
        n_exons = []
        g_vol = []
        icnt = []
        strnd = []
        cdng = []
        for k in range(df.shape[0]):
            # s = '>%s_Chr%s:%i-%i_%i_%i_%i_Abn:%4.3f_TPM:%4.2f_IFrac:%3.2f\n' 
            # % (tr.prefix, tr.chr, tr.start, tr.end, tr.gidx, tr.grp_size, tr.icnt, tr.abn, tr.tpm, tr.iso_frac)
            hdr = df[s_id][k].split(' ')
            items = hdr[0].split('_')
            strnd.append( items[2])
            cdng.append( items[3])
            sidx.append( (items[4]) )
            g_size.append( int(items[5]) )
            icnt.append( int(items[6]) )
            val = items[7].split(':')
            abn_e.append( float(val[1]) )
            val = items[8].split(':')
            tpm_e.append( float(val[1]) )
            val = items[9].split(':')
            ifrac.append( float(val[1]) )
            val = items[11].split(':')
            n_exons.append( int(val[1]) )
            val = items[12].split(':')
            g_vol.append( int(val[1]) )
    else:
        abn_e = np.zeros(df.shape[0])
        tpm_e = np.zeros(df.shape[0])
        ifrac = np.zeros(df.shape[0])
        sidx = np.full(df.shape[0], '')
        g_size = np.zeros(df.shape[0])
        n_exons = np.zeros(df.shape[0])
        g_vol = np.zeros(df.shape[0])
        icnt = np.zeros(df.shape[0])
        strnd = np.zeros(df.shape[0])
        cdng = np.zeros(df.shape[0])
        
    #'''
    ref_info = False
    if len(df[q_id][0].split(':')) == 4: 
        ref_info = True
        # print('Ref_info is true')
        
    if ref_info == True:
        gid = []
        cvg = []
        abn_t = []
        tpm_t = []
        for k in range(df.shape[0]):
            items = df[q_id][k].split(':')
            gid.append( items[0] )
            cvg.append( float(items[1]) )
            abn_t.append( float(items[2]) )
            tpm_t.append( float(items[3]) )
    else:
        gid = np.zeros(df.shape[0])
        cvg = np.zeros(df.shape[0])
        abn_t = np.zeros(df.shape[0])
        tpm_t = np.zeros(df.shape[0])

    #'''
    df['exp_cvg'] = cvg
    df['abn_true'] = abn_t
    df['abn_est'] = abn_e
    df['tpm_true'] = tpm_t
    df['tpm_est'] = tpm_e
    df['gidx'] = sidx
    df['iidx'] = icnt
    df['g_size'] = g_size
    df['iso_frac'] = ifrac
    df['n_exons'] = n_exons
    df['g_vol'] = g_vol
    df['strand'] = strnd
    df['C_or_N'] = cdng
        
    b = df[q_cvg] >= 0.8
    df_new = df.loc[b,:]
    df = df_new
    
    full_names = df[q_id] + df[s_id]
    fns = pd.unique(full_names)
    k = 0
    df_lst = []
    for fn in fns:
        wh = which(full_names == fn)
        df_tmp = df.iloc[wh]
        qcvg = np.array( df_tmp[q_cvg] )
        odr = qcvg.argsort()
        df_lst.append(df_tmp.iloc[odr[-1]]) 
        k += 1

    if len(df_lst) > 0:
        df_sel = pd.DataFrame(df_lst)
        #'''
        trinfo = '%s_blast_result.tsv' % fname
        df_sel.to_csv(trinfo, header=True, index=False, sep='\t')
        # if verbose: print('Transcriptome Info. written to \n   %s.' % trinfo )

        df_sel = pd.read_csv(trinfo, sep='\t')
        #'''

        df_perf, df_sel = get_performance(df_sel, f_to_save=fname, ref = ref, verbose=verbose)
        df_perf['precision'] = round(df_perf['N_recovered']*100/cand_cnt,1)
        df_perf['sensitivity'] = round(df_perf['N_recovered']*100/ref_cnt,1)
        if verbose: print(df_perf)
           
        if trareco == True:
            df_tr = get_info_from_tr_name( tn )
            df_tr['detected'] = False
            df_tr.loc[list(df_sel[s_id]),'detected'] = True 
            df_tr[q_len] = 0
            for m, sid in enumerate(df_sel[s_id]):
                df_tr.loc[sid,q_len] = np.round(df_sel.iloc[m].qlen)
            df_tr[s_start] = 0
            # df_tr.loc[list(df_sel['sid']),'scvg'] = df_sel.loc[:,'scvg'] 
            for m, sid in enumerate(df_sel[s_id]):
                df_tr.loc[sid,s_start] = np.round(df_sel.iloc[m].sstart)
            df_tr[s_end] = 0
            # df_tr.loc[list(df_sel['sid']),'scvg'] = df_sel.loc[:,'scvg'] 
            for m, sid in enumerate(df_sel[s_id]):
                df_tr.loc[sid,s_end] = np.round(df_sel.iloc[m].send)
            df_tr = df_tr.reset_index()
        else:
            df_tr = None
            
        return(df_perf, df_sel, df_tr)
    
    else:
        if verbose: print('No tr found. ')
        return(None,None,None)
    

##################################################################################
## Functions to (1) select specific chrm and (2) only coding genes in a GTF
##################################################################################

def sort_gtf_lines_lst(gtf_lines_lst):
    
    chrs = []
    for lines in gtf_lines_lst:
        first_line = lines[0]
        chrs.append(first_line.chr)

    chr_set = list(set(chrs))
    chr_set.sort()
    chrs = np.array(chrs)

    gtf_lst_new = []
    for c in chr_set:
        wh = sf.which(chrs == c)
        ps = np.array( [gtf_lines_lst[w][0].start for w in wh] )
        odr2 = ps.argsort()
        for o in odr2:
            w = wh[o]
            gtf_lst_new.append(gtf_lines_lst[w])
        
    return gtf_lst_new


def select_coding_genes_from_gtf_file(gtf_file, genome_file):

    fns = gtf_file.split('.')[:-1]
    fname = ''
    for k, fn in enumerate(fns):
        if k > 0:
            fname = fname + '.'
        fname = fname + fn
    
    gtf_lines, hdr_lines = sf.load_gtf(gtf_file, verbose = True)
    
    base_cds = sf.get_base_cds_from_gtf_lines(gtf_lines)
    if base_cds < 0:
        print('INFO: No coding information provided in the GTF/GFF.')
    
    gtf_lines_lst = sf.parse_gtf_lines_and_split_into_genes( gtf_lines )
    genome = sf.load_genome(genome_file)
    chrs = genome.keys()

    gtf_lines_lst_new = []
    ccnt = 0
    gcnt = 0
    for k, glines in enumerate(gtf_lines_lst):

        if  glines[0].chr in chrs:
            tr_lines_lst = sf.parse_gtf_lines_and_split_into_genes( glines, 'transcript' )
            lines_new = []

            for lines in tr_lines_lst:
                b = False
                cnt = [0,0]
                for gtfline in lines:
                    if gtfline.feature == 'start_codon':
                        cnt[0] += 1
                    if gtfline.feature == 'stop_codon':
                        cnt[1] += 1
                    if (cnt[0] > 0) & (cnt[1] > 0):
                        b = True
                        ccnt += 1
                        break
                        
                if b: lines_new = lines_new + lines
                gcnt += 1
            
            if len(lines_new) > 0:
                gtf_lines_lst_new.append(lines_new)
            
        if k%100 == 0: print('\rparsing .. %i/%i (%i/%i)' % (k, len(gtf_lines_lst), ccnt, gcnt), end='', flush = True )

    print('\rparsing .. %i/%i (%i/%i)' % (k, len(gtf_lines_lst), ccnt, gcnt), flush = True )
    print('Sorting .. ', end='')
    gtf_lines_lst_new = sort_gtf_lines_lst(gtf_lines_lst_new)
    print('\rSorting .. done')
            
    gtf_lines_new = []
    for lines in gtf_lines_lst_new:
        gtf_lines_new = gtf_lines_new + lines
        
    fname = fname + '_cds.gtf'
    print('Saving .. ', end='')
    sf.save_gtf( fname, gtf_lines_new, hdr_lines )
    print('\rSaving .. done')
    
    return fname
    

def select_chr_from_gtf_file(gtf_file, chrm = '1'):

    fns = gtf_file.split('.')[:-1]
    fname = ''
    for k, fn in enumerate(fns):
        if k > 0:
            fname = fname + '.'
        fname = fname + fn
    
    gtf_lines, hdr_lines = sf.load_gtf(gtf_file, verbose = True)
    
    gtf_lines_lst = sf.parse_gtf_lines_and_split_into_genes( gtf_lines )

    gtf_lines_lst_new = []
    ccnt = 0
    gcnt = 0
    for k, lines in enumerate(gtf_lines_lst):
        b = False
        if lines[0].chr == chrm: 
            b = True
            ccnt += 1
        gcnt += 1
        
        if k%100 == 0: print('\rparsing .. %i/%i (%i/%i)' % (k, len(gtf_lines_lst), ccnt, gcnt), end='', flush = True )
        if b: 
            gtf_lines_lst_new.append(lines)

    print('\rparsing .. done %i/%i (%i/%i)' % (k, len(gtf_lines_lst), ccnt, gcnt), flush = True )
    
    print('Sorting .. ', end='')
    gtf_lines_lst_new = sort_gtf_lines_lst(gtf_lines_lst_new)
    print('\rSorting .. done')
            
    gtf_lines_new = []
    for lines in gtf_lines_lst_new:
        gtf_lines_new = gtf_lines_new + lines
    
    print('Saving .. ', end='')
    fname = fname + '_sel_%s.gtf' % chrm
    sf.save_gtf( fname, gtf_lines_new, hdr_lines )
    print('\rSaving .. done')
    
    return fname
    

##################################################################################
## Functions to handle simulated reads (add trareco header, split fastQ)
##################################################################################

def fasta_add_trareco_header( ref_tr, sim_profile, read_len, suffix = None, cov_th = 0.8 ):
    
    colnames = ['loc', 'tid', 'coding', 'length', 'exp_frac', 'exp_num', 'lib_frac', 'lib_num', \
                'seq_frac', 'seq_num', 'cov_frac', 'chi2', 'Vcoef']
    df_pro = pd.read_csv(sim_profile, sep='\t', header = None, index_col = 1, names = colnames)

    ref = sf.load_fasta(ref_tr)

    df_pro['abn'] = df_pro['seq_num']*read_len/df_pro['length']
    df_pro['tpm'] = df_pro['abn']*1000000/(df_pro['abn'].sum())

    df_idx = np.array(df_pro.index.values.tolist())
    cnt_dup = 0
    for key in list(ref.keys()):
        if (key in df_idx) & (np.sum(df_idx == key) == 1):
            if df_pro.loc[key].cov_frac >= cov_th:
                ref[key].header = '%s cov_frac:%f abn:%f tpm:%f' % (ref[key].header, df_pro.loc[key].cov_frac, df_pro.loc[key].abn, df_pro.loc[key].tpm)
            else:
                ref.pop(key)
        else:
            if df_pro.loc[key].shape[0] > 1: cnt_dup += 1
            ref.pop(key)

    fname, ext = sf.get_file_name(ref_tr)
    if suffix is None:
        fname = fname + '_cov%i.' % int(cov_th*100) + ext
    else:
        fname = fname + '_%s_cov%i.' % (suffix, int(cov_th*100)) + ext

    sf.save_fasta(fname, ref, title = fname)
    

def load_fastq(file_genome, verbose = False ):

    genome = dict()
    f = open(file_genome, 'r')
    scnt = 0
    print('\rLoading fastQ .. ', end='', flush=True)
    cnt = 0
    for line in f :
        if line[0] == '@':
            if cnt == 4:
                genome[scnt] = sf.Genome(hdr, seq, qual)
                scnt += 1
            cnt = 0
            hdr = line[1:-1]
            cnt += 1
        else:
            if cnt == 1:
                seq = line[:-1]
                cnt += 1
            elif cnt == 2:
                if line[0] == '+':
                    idr = line[1:-1]
                    cnt += 1
                else:
                    print('ERROR in fastQ file')
                    break
            elif cnt == 3:
                qual = line[:-1]
                cnt += 1
    if cnt > 0:
        genome[scnt] = sf.Genome(hdr, seq, qual)
        scnt += 1
                
    print('\rLoading fastQ .. done.  Num.Seq = ', scnt, '   ', flush=True)
    f.close()
    return(genome)


def save_fastq( file_genome, genome_dict, verbose = False, title = 'fastQ' ):

    print('Saving %s ..' % title, end='', flush=True)
    # for g in genome_lst :
    Keys = genome_dict.keys()
    f = open(file_genome, 'wt+')
    line_lst = []
    for key in Keys:
        # print('\rSaving %s .. %s' % (title, key), end='                    ')
        g = genome_dict[key]
        s = '@%s\n' % g.header
        line_lst.append(s)
        line_lst.append(g.seq.upper() + '\n')
        line_lst.append('+\n')
        line_lst.append(g.qual + '\n')
        
        if verbose: print('.', end='', flush=True)

    f.writelines(''.join(line_lst))
        
    print('\rSaving %s .. done. (%i)                ' % (title, len(Keys)), flush=True)
    f.close()
    

    
def fasta_sim_read_split( sim_read, dsr = 1 ):
    
    fname, ext = sf.get_path_name(sim_read)

    fa_all = load_fastq(sim_read)
    
    fa1 = {}
    fa2 = {}
    cnt = 0
    cnt_1 = 0
    cnt_2 = 0
    for key in fa_all.keys():
        fa_all[key].header = fa_all[key].header[:-4]
        if cnt%2 == 0:
            if cnt_1%dsr == 0:
                fa_all[key].header = fa_all[key].header.split(' ')[0] + '/1'
                fa1[key] = fa_all[key]
            cnt_1 += 1
        else:
            if cnt_2%dsr == 0:
                fa_all[key].header = fa_all[key].header.split(' ')[0] + '/2'
                fa2[key] = fa_all[key]
            cnt_2 += 1

        cnt += 1

    if dsr == 1:
        fn1 = fname + '_1.' + ext
        fn2 = fname + '_2.' + ext
    else:
        fn1 = fname + ('_ds%i' % dsr) + '_1.' + ext
        fn2 = fname + ('_ds%i' % dsr) + '_2.' + ext
    save_fastq(fn1, fa1)
    save_fastq(fn2, fa2)
    

def fasta_sim_read_downsample( sim_read, dsr = 1 ):
    
    fname, ext = sf.get_path_name(sim_read)

    fa_all = load_fastq(sim_read)
    
    fa = {}
    cnt = 0
    for key in fa_all.keys():
        # fa_all[key].header = fa_all[key].header[:-4]
        if cnt%dsr == 0:
            # fa_all[key].header = fa_all[key].header
            fa[key] = fa_all[key]
        cnt += 1

    fn = fname + ('_ds%i.' % dsr) + ext
    save_fastq(fn, fa)
    
    
##################################################################################
## Functions to add SNV into a genome
##################################################################################

SNV = collections.namedtuple('SNV', 'chr, pos_new, pos_org, type, len, seq_new, seq_org, ex_start, ex_end')

def get_snv_type(pi, pd):
    
    rn = np.random.uniform(100)
    if rn < (pi*100):
        return(1)
    elif rn < (pi+pi)*100:
        return(2)
    else:
        return(0)
    
def rand_nucleotide_except(nts):
    
    nts_out = ''
    for nt in nts:
        while True:
            rn = np.random.randint(0,4,1)[0]
            nt_new = sf.NT_lst[int(rn)]
            if nt_new != nt: 
                nts_out = nts_out + nt_new
                break
                    
    return(nts_out)
        
def rand_nucleotides(num):
    
    num_seq = np.random.randint(0,4,num)
    nt_str = ''.join([sf.NT_lst[n] for n in num_seq])
    return(nt_str)


def save_snv_info_old( file_name, snv_lst, verbose = False ):
    
    f = open(file_name, 'wt+')
    print('Saving SNV info. ', end='')
    step = np.ceil(len(snv_lst)/20)
    for k in range(len(snv_lst)) :
        snv = snv_lst[k]
        s = '%s,%i,%i,%s,%i,%s,%s\n' % \
        (snv.chr, snv.pos_new, snv.pos_org, snv.type, snv.len, snv.seq_new, snv.seq_org )
        f.writelines(s)
        if k%step == 0: print('.',end='')
        
    print(' done. %i snvs.' % len(snv_lst) )
    f.close()

    
def save_snv_info( file_name, snv_lst, verbose = False ):

    df = pd.DataFrame(snv_lst)
    df.to_csv(file_name, index=False, sep='\t')

    
def generate_snv_with_gtf( genome, gtf_lines_sorted, mu = 200, li = 3, ld = 3, lv = 2, pi = 0.1, pd = 0.1 ):
    
    pv = 1 - pi - pd
    print(genome.name, end=' ')
    snv_lst = []
    cur_pos_org = 0
    cur_pos_new = cur_pos_org
    seq_new = ''
    seq_lst = []
    Margin = max(li,max(ld,lv))
    
    step = np.ceil(genome.len/mu/200)
    
    cnt = 0
    for line in gtf_lines_sorted:
        
        # diff = cur_pos_new - cur_pos_org
        Start = line.start
        End = line.end
        L = np.random.randint(0,mu/2,1)[0]
        if cur_pos_org < (line.start-1+L):
            next_pos_org = line.start-1+L
            seq_lst.append(genome.seq[int(cur_pos_org):int(next_pos_org)])
            cur_pos_new += (next_pos_org-cur_pos_org)
            cur_pos_org = next_pos_org
        
        while (cur_pos_org < (line.end-Margin)) & (cur_pos_org > (line.start+Margin)):

            snv_type = get_snv_type(pi, pv)

            if snv_type == 1: # Insertion
                n = np.random.randint(0,li, 1)[0]+1
                seq_frag = rand_nucleotides(n)
                # seq_new = seq_new + seq_frag
                seq_lst.append(seq_frag)
                snv = SNV( genome.name, cur_pos_new+1, cur_pos_org+1, 'I', n, seq_frag, '-', Start, End ) # make it one-base position
                snv_lst.append(snv)
                cur_pos_new += len(seq_frag)

            elif snv_type == 2: # Deletion
                n = np.random.randint(0,ld, 1)[0]+1
                seq_frag = genome.seq[int(cur_pos_org):int(cur_pos_org+n)]
                snv = SNV( genome.name, cur_pos_new+1, cur_pos_org+1, 'D', n, '-', seq_frag, Start, End ) # make it one-base position
                snv_lst.append(snv)
                cur_pos_org += n

            else: # SNP
                n = np.random.randint(0,lv, 1)[0]+1        
                seq_tmp = genome.seq[int(cur_pos_org):int(cur_pos_org+n)]
                seq_frag = rand_nucleotide_except(seq_tmp)
                # seq_new = seq_new + seq_frag
                seq_lst.append(seq_frag)
                snv = SNV( genome.name, cur_pos_new+1, cur_pos_org+1, 'V', n, seq_frag, seq_tmp, Start, End ) # make it one-base position
                snv_lst.append(snv)
                cur_pos_new += n
                cur_pos_org += n

            L = np.random.randint(20,mu,1)[0] # separate SNV at least 20 bases
            next_pos_org = cur_pos_org + L
            if next_pos_org >= line.end: # (genome.len-100):
                # seq_new = seq_new + genome.seq[int(cur_pos_org):]
                seq_lst.append(genome.seq[int(cur_pos_org):(line.end+1)])
                cur_pos_new += ((line.end+1)-cur_pos_org)
                cur_pos_org = (line.end+1)
                break
            else:
                # seq_new = seq_new + genome.seq[int(cur_pos_org):int(next_pos_org)]
                seq_lst.append(genome.seq[int(cur_pos_org):int(next_pos_org)])
                cur_pos_new += (next_pos_org-cur_pos_org)
                cur_pos_org = next_pos_org
            cnt += 1
            if cnt%step == 0: 
                print('\r%s - %i, %i, %i ' % (genome.name, cur_pos_org, genome.len, cur_pos_new), end='')
       
    if cur_pos_org < genome.len:
        seq_lst.append(genome.seq[int(cur_pos_org):])
    
    seq_new = ''.join(seq_lst)
    # suffix = '-L%i-I%i-D%i-V%i' % (mu,li,ld,lv)
    # genome_new = Genome( genome.header + suffix, seq_new )
    genome_new = sf.Genome( genome.header, seq_new )
    print(' done.')
            
    return(genome_new, snv_lst)
    
################################
## Parameters for SNV generation

P_INS = 0.15
P_DEL = 0.15
P_SNP = 1 - P_INS - P_DEL

LI = 3
LD = 3
LV = 2
L_INTER_SNV = 200

################################

def generate_snv(genome, gtf_lines, l_inter_snv = L_INTER_SNV, \
                 li = LI, ld = LD, lv = LV, pi = P_INS, pd = P_DEL):
    
    pv = 1 - pi - pd
    np.random.seed(0)
    print('Generating SNV ',end='')
    Features = sf.get_col(gtf_lines, 2)
    wh = sf.which( Features, 'exon' )
    gtf_exons = [gtf_lines[w] for w in wh] 

    # print(len(Features))
    Chrs = sf.get_col(gtf_exons, 0)
    Chr_names = sorted(set(Chrs))

    snv_lst_all = []
    genome_new = {}
    for Chr in Chr_names:
        
        if Chr in genome.keys():
            wh = sf.which( Chrs, Chr )
            gtf_chr = [gtf_exons[w] for w in wh]
            Pos_start = np.array( sf.get_col(gtf_chr, 3) )
            odr = Pos_start.argsort()

            gtf_chr_sorted = []
            pp = 0
            for k in range(len(gtf_chr)):
                line = gtf_chr[odr[k]]
                gtf_chr_sorted.append(line)
                if line.start < pp: print(line)
                pp = line.start

            gnm, snv_lst = generate_snv_with_gtf( genome[Chr], gtf_chr_sorted, mu = l_inter_snv, \
                                                  li = li, ld = ld, lv = lv, pi = pi, pd = pd )
            snv_lst_all = snv_lst_all + snv_lst
            genome_new[Chr] = gnm
     
    return(genome_new, snv_lst_all, Features)
    
##################################################################################
## Functions for evaluation of SNV detection
##################################################################################

def get_span_lst(rgns_lst_mi, Type = 'M'):
    
    span_lst = []
    for r_m in rgns_lst_mi:
        spn = r_m.get_span()
        spn.type = Type
        span_lst.append( spn )
    return(span_lst)

## Select SNV's that falls within the covered region
def select_snvs( df_snv, span_lst, rgns_lst_mi, Type = 'M', mdev = 12 ):
    
    print('Checking intersection .. ', end='')
    step = np.ceil(df_snv.shape[0]/20)
    
    df_snv['start'] = df_snv['pos_org'] - mdev
    df_snv['end'] = df_snv['pos_org'] + df_snv['len'] + mdev
    df_snv['cvg'] = 0

    b_proc = np.full(df_snv.shape[0], False)
    for k, span in enumerate(span_lst):
        b0 = df_snv['chr'] == span.chr
        b1 = (df_snv['start'] >= span.start) & ((df_snv['start'] <= span.end))
        b2 = (df_snv['end'] >= span.start) & ((df_snv['end'] <= span.end))
        b = b0 & (b1 | b2) & (b_proc == False)
        df_snv_tmp = df_snv[b]
        for m, row in df_snv_tmp.iterrows():
            rgn = sf.region( row.chr, row.start, row.end, Type )
            bb, cc = rgns_lst_mi[k].get_intersection_cvg(rgn) 
            if bb: 
                b_proc[m] = True
                df_snv.loc[m,'cvg'] = cc
                
        # if k%step == 0: print('.',end='')
        if k%10 == 0:    
            print('\rChecking intersection .. %i/%i (%i)' % (k, len(span_lst), np.sum(b_proc)), end='' )

    print('\rChecking intersection .. done. %i -> %i' % (df_snv.shape[0], np.sum(b_proc)) )
    
    df_snv_sel = (df_snv.iloc[b_proc]).copy(deep = True)
    
    return(df_snv_sel)


def matching_snvs( df_snv_sel, df_detected, dev_tol = 3 ):
    
    ## the dataframes mush be sorted according to the position (pos_new, start)
    df_t_all = df_snv_sel
    df_d_all = df_detected

    cnt = 0
    chrms = df_t_all['chr']
    chr_lst = list(set(chrms))
    chr_lst.sort()

    cnt = 0
    N_t = 0
    N_d = 0
    for n, chrm in enumerate(chr_lst):
        
        b1 = (df_t_all['chr'] == chrm)
        b2 = (df_d_all['chr'] == chrm)
    
        if (np.sum(b1) == 0) | (np.sum(b2) == 0):        
            pass
        else:
            
            df_t = df_t_all.loc[b1,:].copy(deep = True)
            df_d = df_d_all.loc[b2,:].copy(deep = True)
            
            n_target = df_t.shape[0]
            n_detected = df_d.shape[0]
            
            N_t += n_target
            N_d += n_detected
            
            # print('\rMatching %s ' % (chrm) , end='')
            cnt_t = 0
            cnt_d = 0
            match = np.full(n_target, -1)
            dist = np.full(n_target, 0)
            
            while True:
                
                if (cnt_d >= n_detected) | (cnt_t >= n_target): break
                print('\rMatching %s, %i/%i .. %i/%i, %i/%i ' % \
                      (chrm, n, len(chr_lst), cnt_t, n_target, cnt_d, n_detected) , end='')

                p_t = df_t.iloc[cnt_t].pos_org
                p_d = df_d.iloc[cnt_d].pos_org
                t_t = df_t.iloc[cnt_t].type
                t_d = df_d.iloc[cnt_d].type
                L_t = max(len(df_t.iloc[cnt_t].seq_org), len(df_t.iloc[cnt_t].seq_new))
                L_d = max(len(df_d.iloc[cnt_d].seq_org), len(df_d.iloc[cnt_d].seq_new))

                if (p_t) > (p_d + L_d + dev_tol):
                    cnt_d += 1
                    if cnt_d >= n_detected: break
                elif (p_t + L_t + dev_tol) < (p_d):
                    cnt_t += 1
                    if cnt_t >= n_target: break
                else:
                    b = True
                    if (t_t == 'V') & (t_d == 'V'):
                        if len(df_t.iloc[cnt_t].seq_new) == len(df_d.iloc[cnt_d].seq_new):
                            if (p_t == p_d) & (df_t.iloc[cnt_t].seq_new == df_d.iloc[cnt_d].seq_new):
                                match[cnt_t] = cnt_d
                                dist[cnt_t] = p_t - p_d
                                cnt_t += 1
                                cnt_d += 1
                                b = False
                            else:
                                pass
                                '''
                                match[cnt_t] = cnt_d
                                dist[cnt_t] = p_t - p_d
                                cnt_t += 1
                                cnt_d += 1
                                b = False
                                '''
                        else:
                            pass
                        
                        if b:
                            cnt_t += 1
                            cnt_d += 1
                            
                    elif (t_t == 'I') & (t_d == 'D'):
                        match[cnt_t] = cnt_d
                        dist[cnt_t] = p_t - p_d
                        cnt_t += 1
                        cnt_d += 1
                        b = False

                    elif (t_t == 'D') & (t_d == 'I'):
                        match[cnt_t] = cnt_d
                        dist[cnt_t] = p_t - p_d
                        cnt_t += 1
                        cnt_d += 1
                        b = False
                    else:
                        # cnt_t += 1
                        # cnt_d += 1
                        if (cnt_d >= n_detected) | (cnt_t >= n_target): break
                        

            b = match >= 0
            wh_t = sf.which(b)
            wh_d = match[wh_t]
            
            if len(wh_t) > 0:
                if cnt == 0:
                    df_t['dist'] = dist
                    df1 = df_t.iloc[wh_t].copy(deep = True)
                    df2 = df_d.iloc[wh_d].copy(deep = True)
                    cnt += 1
                else:
                    df_t['dist'] = dist
                    df1 = pd.concat([df1, df_t.iloc[wh_t].copy(deep = True)])
                    df2 = pd.concat([df2, df_d.iloc[wh_d].copy(deep = True)])
                    cnt += 1
           
    print('\rMatching .. done. ', end = '')
    if cnt > 0:
        df2 = df2.rename( columns = {'chr': 'chr_d', 'type': 'type_d', 'pos_org': 'pos_org_d', \
                                'seq_org': 'seq_org_d', 'seq_new': 'seq_new_d'} )
        sel_col_t = ['chr', 'type', 'pos_org', 'seq_org', 'seq_new', 'dist']
        sel_col_d = ['id', 'chr_d', 'type_d', 'pos_org_d', 'seq_org_d', 'seq_new_d']
        df1.index = pd.Index([k for k in range(df1.shape[0])])
        df2.index = pd.Index([k for k in range(df2.shape[0])])
        df = pd.concat( [df1[sel_col_t], df2[sel_col_d]], axis = 1, sort=False )        
            
        sens = 100*df.shape[0]/N_t
        prec = 100*df.shape[0]/N_d
        print(' N_t: %i, N_d: %i -> %i (sens: %4.1f, prec: %4.1f) ' % \
              (N_t, N_d, df.shape[0], sens, prec))
        return df, prec, sens, df.shape[0], N_d, N_t
    else:
        print(' ')
        return None, 0, 0, 0, 0, 0
            


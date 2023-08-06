import PharmacoDI as pdi

pset = 'GDSC_v1'
pset_dir = '../PharmacoDI_snakemake_pipeline/rawdata'
procdata_dir = '../PharmacoDI_snakemake_pipeline/procdata'
gene_sig_dir = '../PharmacoDI_snakemake_pipeline/rawdata/gene_signatures'
drug_meta_file = '../PharmacoDI_snakemake_pipeline/metadata/drugs_with_ids.csv'
output_dir = '../PharmacoDI_snakemake_pipeline/latest'
drug_meta_file = '../PharmacoDI_snakemake_pipeline/metadata/drugs_with_ids.csv'
gct_file = '../PharmacoDI_snakemake_pipeline/rawdata/gene_signatures/metaanalysis/gene_compound_tissue.csv'

if __name__ == '__main__':
    # Step 1 -- works with all PSets
    #pset_dict = pdi.pset_df_to_nested_dict(pdi.read_pset(pset, pset_dir))
    #pdi.build_all_pset_tables(pset_dict, pset, procdata_dir, gene_sig_dir)

    # Step 2
    #pdi.combine_all_pset_tables(procdata_dir, output_dir, drug_meta_file)

    # Step 3
    # pdi.build_compound_synonym_df(drug_meta_file, output_dir)

    # Step 9
    pdi.build_gene_compound_tissue_df(gct_file, output_dir)

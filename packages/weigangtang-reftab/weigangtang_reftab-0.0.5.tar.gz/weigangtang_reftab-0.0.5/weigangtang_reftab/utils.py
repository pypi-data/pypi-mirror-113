import numpy as np
import pandas as pd

import os, glob, re, string

header_full = ['Link', 'Title', 'Abbr', 'Year', 'Journal', 'Authors', 'Vol', 'Pages', 'Keyword']
header_must = ['Title', 'Year', 'Journal', 'Authors', 'Vol', 'Pages']

def check_pattern(target_string, pattern):
    return bool(re.search(pattern, target_string))

# undone, can not screen out "et al" (no . at end) 
# def is_abbr_format_correct(abbr):
#     last_name_pattern = '[a-zA-Z- ]{2,20}'
#     year_pattern = '[0-9]{4}[a-z]?'
#     is_pattern_1 = check_pattern(abbr, '^{0}(?<!et al\.), {1}$'.format(last_name_pattern, year_pattern)) # one author
#     is_pattern_2 = check_pattern(abbr, '^{0} & {0}, {1}$'.format(last_name_pattern, year_pattern)) # two authors
#     is_pattern_3 = check_pattern(abbr, '^{0} et al\., {1}$'.format(last_name_pattern, year_pattern)) # three or more authors
#     return is_pattern_1 or is_pattern_2 or is_pattern_3

def is_year_format_correct(year):
    return check_pattern(year, '^[0-9]{4}[a-z]?$')

def is_author_format_correct(authors_string):
    author_list = authors_string.split('; ')
    for author in author_list:
        if author != '…':
            if not check_pattern(author, '^[a-zA-Z- ]{2,20},( [A-Z].){1,5}$'):
                return False
    return True

def auto_correct_author_string(author_string_list):
    # remove space at end
    for i, author_string in enumerate(author_string_list):
        while author_string[-1] == ' ': author_string = author_string[:-1]
        author_string_list[i] = author_string
    # add . after name short
    for i, author_string in enumerate(author_string_list):
        author_list = []
        for author in author_string.split('; '):
            author = re.sub(r'([A-Z](?![\.|a-z]))', r'\1.', author) # r must be placed ahead string
            author_list.append(author)
        author_string_list[i] = '; '.join(author_list)
    return author_string_list

def auto_fill_abbr(df):
    abbr_list = []
    for authors, year in df[['Authors', 'Year']].values:
        if is_year_format_correct(year) & is_author_format_correct(authors):
            author_name_list = [item.split(', ')[0] for item in authors.split('; ')] # last name
            n_author = len(author_name_list)
            if n_author == 1: 
                author = author_name_list[0]
            if n_author == 2:
                author = ' & '.join(author_name_list)
            if n_author >= 3:
                author = author_name_list[0] + ' et al.'
            abbr_list.append(', '.join([author, str(year)]))
        else: 
            abbr_list.append('')
    return abbr_list

def auto_fill_link(df):
    link_list = []
    for abbr, journal in df[['Abbr', 'Journal']].values:
        name, year = abbr.split(', ')
        name = name.replace('et al.', 'et al')
        journal = journal + '.pdf'
        link = '_'.join([name, year, journal])
        link_list.append(link)
    return link_list

def read_ref_workbook(workbook_fpath):
    workbook_dict = {}
    workbook = pd.ExcelFile(workbook_fpath)
    for sheet_name in workbook.sheet_names:
        df = pd.read_excel(workbook, sheet_name, index_col=0).astype(str)
        df = df.replace('nan', '')
        workbook_dict.update({sheet_name: df})
    return workbook_dict

# dataframe must have the same header
def merge_ref_workbook(workbook_dict):
    df_list = []
    for sheet_name, df in workbook_dict.items():
        if 'Keyword' not in df.columns:
            df['Keyword'] = sheet_name
        df_list.append(df)
    return pd.concat(df_list, axis=0).sort_index()

def get_pdf_list(readcube_fpath, show_invalid=True):
    fpath_list = glob.glob(readcube_fpath + '/*.pdf')
    fname_list = sorted([os.path.split(fpath)[1] for fpath in fpath_list])

    sel_fname_list = []
    for fname in fname_list:
        if len(fname.split('_'))==3: 
            sel_fname_list.append(fname) 

    if show_invalid:
        unsel_fname_list = sorted(set(fname_list).difference(sel_fname_list))
        if len(unsel_fname_list) > 0:
            print('\033[1mPDF with Non-Paper Format:\033[0m') # print bold
            for fname in unsel_fname_list:
                print(fname)

    return sel_fname_list

def create_df_from_pdf_name(pdf_name_list):
    df = pd.DataFrame(columns=header_full)
    for i, link in enumerate(pdf_name_list):
        name, year, journal = link.split('_')
        name = name.replace('et al', 'et al.')
        abbr = ', '.join([name, year])
        journal = journal[:-4] # remove .pdf from file name
        df.loc[i, ['Abbr', 'Year', 'Journal', 'Link']] = [abbr, year, journal, link]
    df = df.set_index('Link').sort_index()
    return df

def sort_header(df):
    # item not in header are ignored
    sorted_header = [item for item in header_full if item in df.columns]
    return df[sorted_header]

# workbook: Dictionary of DataFrame, e.g. {'Sheet1': df_ref}
# determine the standard format of reference table (in excle)
def save_workbook_to_excel(out_fpath, workbook, hyperlink_base, overwrite=False):

    column_width =  [40, 40, 20, 10, 30, 30, 5, 10, 20]

    text_format = {'font_name': 'Times New Roman', 'font_size': 12}
    header_format = {**text_format, **{'bold': True}}
    url_format = {**text_format, **{'color': 'blue'}}

    exists = os.path.exists(out_fpath)

    if not exists or overwrite:

        writer = pd.ExcelWriter(out_fpath, engine='xlsxwriter')

        hyperlink_base = os.path.abspath(hyperlink_base) + '/' # must add '/' at end, or hyperlink is invalid
        writer.book.set_properties({'hyperlink_base': hyperlink_base})

        for sheet_name, df in workbook.items():

            df = sort_header(df)

            df.to_excel(writer, sheet_name=sheet_name)
            nrow, ncol = df.shape

            worksheet = writer.sheets[sheet_name]

            # set header format
            header = df.reset_index().columns.tolist()
            worksheet.write_row(0, 0, header, writer.book.add_format(header_format))

            # set content format and column width (add one for index column)
            for i in range(ncol+1): 
                worksheet.set_column(i, i, column_width[i], writer.book.add_format(text_format))

            # set url format (overwrite first column)
            for i in range(nrow): 
                worksheet.write_url(i+1, 0, df.index[i], writer.book.add_format(url_format))

        writer.save()

    else: 
        print('Not Allow Overwrite!')

def save_df_to_excel(out_fpath, df_ref, hyperlink_base, overwrite=False):
    workbook = {'': df_ref} # if sheet name = '', the default will be assigned as 'Sheet1'
    save_workbook_to_excel(out_fpath, workbook, hyperlink_base, overwrite)

def save_df_to_latex(out_fpath, df_ref, overwrite=False):

    exists = os.path.exists(out_fpath)

    if not exists or overwrite:

        df_ref = df_ref.copy()

        df_ref['Label'] = ''
        for indx, item in df_ref.iterrows():
            label = item['Abbr']
            label = label.replace(' & ', ' ')
            label = label.replace(',', '')
            label = label.replace('.', '')
            label = label.replace(' ', '-')
            df_ref.loc[indx, 'Label'] = label

        # add a letter for duplicated abbr
        a2z = string.ascii_lowercase
        for target_label in np.unique(df_ref['Label']):
            indx = df_ref['Label'] == target_label
            n_dup = sum(indx)
            if n_dup > 1:
                df_ref.loc[indx, 'Label'] = [target_label+char for char in a2z[:n_dup]]
        df_ref = df_ref.sort_values('Label')

        refs = []
        for indx, item in df_ref.iterrows():
            lines = []
            lines.append('@article{' + item['Label'] + ', ')
            lines.append('\t author = \"{}\", '.format(item['Authors'].replace(';', ' and')))
            lines.append('\t title = \"{}\", '.format(item['Title']))
            lines.append('\t year = \"{}\", '.format(item['Year']))
            lines.append('\t journal = \"{}\", '.format(item['Journal']))
            if item['Vol'] != '-':
                lines.append('\t volume = \"{}\", '.format(item['Vol']))
            if item['Pages'] != '-':
                lines.append('\t pages = \"{}\", '.format(item['Pages']))
            lines.append('}')

            refs.append('\n'.join(lines))

        if exists: os.remove(out_fpath)
        with open(out_fpath, 'a') as f: f.write('\n\n'.join(refs))

    else: 
        print('Not Allow Overwrite!')

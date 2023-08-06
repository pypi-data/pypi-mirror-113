import numpy as np
import pandas as pd

from utils import *

class RefTab():

	# reftab: DataFrame
	def __init__(self, reftab, hyperlink_base):

		header_required = ['Title', 'Year', 'Journal', 'Authors', 'Vol', 'Pages']
		header_optional = ['Abbr', 'Link', 'Keyword']

		assert set(header_required).issubset(reftab.columns)

		self.df = reftab
		self.df['Abbr'] = auto_fill_abbr(self.df)
		self.df.index = auto_fill_link(self.df)
		self.df.index.name = 'Link'
		if 'Keyword' not in self.df.columns: self.df['Keyword'] = ''
		self.df['Keyword'] = self.df['Keyword'].replace('Sheet1', '')

		self.hyperlink_base = os.path.abspath(hyperlink_base) + '/' # must add '/' at end, or hyperlink is invalid

		self.pdf_list = get_pdf_list(self.hyperlink_base, show_invalid=False)

	def update(self, new_reftab):
		self.df = new_reftab
	
	def find_incomplete_ref(self):
		return self.df[self.df.isna().any(axis=1)]

	def find_duplicated_ref(self):
		return self.df[self.df.index.duplicated(keep=False)]

	def find_duplicated_ref_by_abbr(self):
		return self.df[self.df.duplicated('Abbr', keep=False)]

	def find_nolink_ref(self):
		nolink_fname_list = sorted(set(self.df.index).difference(self.pdf_list))
		return self.df.loc[nolink_fname_list, :]

	def find_unlisted_pdf(self):
		unlisted_pdf_list = sorted(set(self.pdf_list).difference(self.df.index))
		return unlisted_pdf_list

	def find_invalid_pdf_name(self):
		invalid_name_pdf_list = [pdf_name for pdf_name in self.pdf_list if len(pdf_name.split('-')) != 3]
		return invalid_name_pdf_list

	def get_unique_keywords(self):
		keyword_list = []
		for keyword in self.df['Keyword']:
			keyword_list += keyword.split(', ')
		return np.unique(keyword_list).tolist()

	def get_unique_ref(self):
		df = self.df.groupby('Link').first()
		merge_keyword = lambda x: ', '.join([i for i in x if i != ''])
		df['Keyword'] = self.df.groupby('Link')['Keyword'].apply(merge_keyword)
		return df

	def subset_ref_by_keyword(self, keyword):
		sel_idx = []
		for keyword_string in self.df['Keyword']:
		    keyword_list = keyword_string.split(', ')
		    sel_idx.append(keyword in keyword_list)
		return  self.df.iloc[sel_idx, :]

	def subset_ref_by_abbr(self, sel_abbr):
		df = self.get_unique_ref()
		df = self.df.drop(columns='Keyword')

		all_abbr = set(df['Abbr'].values)
		sel_abbr = set(np.unique(sel_abbr))

		diff = sorted(sel_abbr.difference(all_abbr))
		if len(diff) > 0:
			print('Not Found Related References:')
			print(*diff, sep='\n')

		union = sorted(sel_abbr.intersection(all_abbr))
		return df[df['Abbr'].isin(union)]

	def save_to_excel(self, out_fpath, overwrite=False, split_by_keyword=False):
		if split_by_keyword:
			wb = {}
			for keyword in self.get_unique_keywords():
				df_sel = self.subset_ref_by_keyword(keyword, drop_keyword_column=True)
				wb.update({keyword: df_sel})
			save_workbook_to_excel(out_fpath, wb, self.hyperlink_base, overwrite) 
		else:
			save_df_to_excel(out_fpath, self.df, self.hyperlink_base, overwrite)

	def save_to_latex(self, out_fpath, overwrite=False): 
		save_df_to_latex(out_fpath, self.df, overwrite)



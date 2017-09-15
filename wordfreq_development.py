#coding=utf8
'''
Anna Bonazzi, 16/08/2017

Script to make a plot of corpus word frequency evolution by language.
Word frequency is taken from the corpus.vrt file, one text at a time. Word variants are found with regex.
Language attributes are taken from the <text> line of every text.
'''
#--------------------------
# VARIABLES FOR USER TO CHANGE:

corpus = '/path/to/corpus.vrt'
#selected_sources = '/path/to/list/of/corpus_sources/as/filter.txt' # !! Comment out if not needed
stats_file = '/path/to/file/to/save/freq_stats.txt'

keyword = 'Nuklear'
output_file = '/path/to/output/filename'+keyword+'.png' # Plot name

regex_fr = '((N|n)ucléaire.?|(A|a)tomique.?)'
regex_de = '((N|n)uklear.*?|(A|a)tom.*?|(K|k)ern(anl.*?|ener.*?|tech.*?|kr.*?))'
regex_it = '((A|a)tomic.*?|(N|n)uclear.*?)'
regex_en = '((A|a)tom.*?|(N|n)uclear.*?)'

# Time window to search
min_year = 2007; max_year = 2017

# Overall plot attributes
myfont = 'DejaVu Sans' # Arial
fontcolor = '#185a92' # Pick colors from http://htmlcolorcodes.com/
# Change other plot attributes from line 192 on

# Frequency measure
frequency = 'permillion' # Options: 'permillion', 'absolute'
#--------------------------
# To time the script
from datetime import datetime
startTime = datetime.now()
import os, glob, re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#--------------------------

# 1) Collects data
fhandle = open (stats_file, 'a')
# Prepares dictionary to save word freq by language
de = {}; fr = {}; it = {}; en = {}
dic = {}
text_counter = 0
all_words = {}
# Temporary text chunk to be analyzed
chunk = []

# List of sources to be searched for specific queries (e.g. media) 
sources = []
try:
	with open (selected_sources, 'r') as f:
		for word in f:
			sources.append(word.strip('\n'))
except:
	pass

# Goes through the corpus one text at at time
with open (corpus, 'r') as f:
	print ('  Searching corpus. Go have some coffee...')
	for line in f:
		if '</text>' not in line:
			if '<' not in line:
				word = line.split("\t")[2] # 0 wordform, 1 pos, 2 lemma
				chunk.append(word) # Fills temporary text chunk with lemmas
			elif '<text' in line:
				chunk.append(line)
		else: # Meets text end
			# Searches for selected lang and class combination
			regex = re.search('.*?class="(.*?)".*?date_published="(.*?)".*?language="(.*?)".*?source="(.*?)".*?', ''.join(chunk))
			if regex:
				cl = regex.group(1); lang = regex.group(3); source = regex.group(4)
				try:
					l = len(selected_sources)
					print (l)
				except:
					sources = []
					sources.append(source)
				
				# Looks only in selected sources
				if source in sources: 
					if '-' in regex.group(2):
						date = regex.group(2)
						# Checks date: right format, right time window
						if len(date.split('-')[0]) == 4 and int(date.split('-')[0]) >= min_year and int(date.split('-')[0]) <= max_year and int(date.split('-')[0]) < 9999:
							if int(date.split('-')[1]) > 7: # Makes half-years
								year = str(date.split('-')[0]) + ".2"
							else:
								year = str(date.split('-')[0]) + ".1"

							#------------------
							# Counts searchword frequency per language or year
							def fill_dic(dic, year, lang, reg):	
								regex2 = re.findall(reg, ' '.join(chunk))
								if regex2:
									if year in dic:
										dic[year] += len(regex2)
									else:
										dic[year] = len(regex2)
								return dic
							#------------------
							if lang == 'fr':
								fr = fill_dic(fr, year, lang, regex_fr)	
							if lang == 'de':
								de = fill_dic(de, year, lang, regex_de)
							if lang == 'en':
								en = fill_dic(en, year, lang, regex_en)
							if lang == 'it':	
								it = fill_dic(it, year, lang, regex_it)			
								
							# Counts words by language
							if lang in all_words:
								all_words[lang] += len(chunk) - 1
							else:
								all_words[lang] = len(chunk) - 1			
			chunk = [] # Resets empty text chunk
			text_counter += 1
			if '00000' in str(text_counter):
				print ("\tText " + str(text_counter))
		
#------------------------------------
# 2) Starts making plot

print ('Starting plot')
# Sorts dictionaries and fills x/y lists
def plot_line(dic, linecolor, lang_tot, lang):
	fhandle.write(keyword + '\t' + lang + '\n')
	# Fills x/y axes
	x = []
	y = []
	xlist = []
	if frequency == 'absolute':
		# Absolute Frequency
		ytitle = 'Absolute Frequenz'
		for i in range (min_year, max_year + 1):
			if str(i + 0.1) in dic:
				xlist.append(str(i))
				freq = dic[str(i + 0.1)]
				y.append(freq)
			else:
				xlist.append(str(i))
				freq = 0
				y.append(freq)
			fhandle.write(str(i + 0.1) + '\t' + str(freq) + '\n')
			if str(i + 0.2) in dic:
				xlist.append(str(i))
				freq = dic[str(i + 0.2)]
				y.append(freq)
			else:
				xlist.append('')
				freq = 0
				y.append(freq)
			fhandle.write(str(i + 0.2) + '\t' + str(freq) + '\n')
		for i in range (1, len(xlist) + 1):
			x.append(i)
	elif frequency == 'permillion':	
		# Frequency per million or per hundred
		ytitle = 'Frequenz per Million\n'
		for i in range (min_year, max_year + 1):
			if str(i + 0.1) in dic:
				xlist.append(str(i))
				freq = float("{:.2f}".format(float(dic[str(i + 0.1)]) * 1000000 / lang_tot))
				y.append(freq)
			else:
				xlist.append(str(i))
				freq = 0
				y.append(freq)
			fhandle.write(str(i + 0.1) + '\t' + str(freq) + '\n')
			if str(i + 0.2) in dic:
				xlist.append('')
				freq = float("{:.2f}".format(float(dic[str(i + 0.2)]) * 1000000 / lang_tot))
				y.append(freq)
			else:
				xlist.append('')
				freq = 0
				y.append(freq)
			fhandle.write(str(i + 0.2) + '\t' + str(freq) + '\n')
		for i in range (1, len(xlist) + 1):
			x.append(i)
				
	
	# Plots the line
	plt.plot(x, y, color=linecolor, linewidth = 3,  marker='o', linestyle='-') # label = 
	
	return xlist, x, y, ytitle
#------------------
	
xlist, x, y, ytitle = plot_line(fr, '#bbcbdb', all_words['fr'], 'fr') # Largest language first
plot_line(de, '#9ebd9e', all_words['de'], 'de')
plot_line(en, '#dd855c', all_words['en'], 'en')
plot_line(it, '#745151', all_words['it'], 'it')

# Set ax ticks
plt.xticks(x, xlist, fontname = myfont, fontsize = '16') # xlist, 
plt.yticks(fontname = myfont, fontsize = '16')

# Get current figure and then add subplot - to do additional format stuff
fig = plt.gcf() 
ax = fig.add_subplot(111)

'''
# Set datapoint labels:
pointlabels = ['60\nMio.', '114.8\nMio.', '166.6    \nMio.', '331.6\n   Mio.     ', '    358\n     Mio.', '  N/A', '457.9\nMio.', '1.03\nMia.']
for i, j in zip(x, y):  
	# Pick element from desired label list through index of current i
	pointlabel = pointlabels[x.index(i)]
	ax.annotate(pointlabel, xy=(i,j), xytext=(-25,15), textcoords='offset points', fontname = myfont, fontsize = '16')
 '''
         
# Set ax labels
#plt.xlabel('Releases', color = fontcolor, fontname = myfont, fontsize = '20', position = (0.5, 0.5))
plt.ylabel(ytitle, color = fontcolor, fontname = myfont, fontsize = '20', position = (-1, 0.5))

# Set title 
plt.title(keyword + '\n', color = fontcolor, fontname = myfont, fontsize = '24')

# Set subtitle (use suptitle - moves up with \n)
plt.suptitle('\n\nEntwicklung je nach Sprache (' + xlist[0] + '-' + xlist[-2] + ')', color = fontcolor, fontname = myfont, fontsize = '16')# , position = (-1, 0.5))

# Set text box
# 1, float(y[1] + 2)
plt.text(1, float(y[1] + 2), 'Grösse der Subkorpora:\n\nFr: '+str(all_words['fr'])+'\nDe: '+str(all_words['de'])+'\nIt: '+str(all_words['it'])+'\nEn: '+str(all_words['en']), fontsize=16, fontname=myfont, color = fontcolor)

# Set legend
leg = plt.legend(loc='best', frameon=False, facecolor = 'r',  labels = ['Fr', 'De', 'En', 'It']) # edgecolor = 'b', # Don't have to specify them unless to change them

# Change all legend 
for text in leg.get_texts():
    text.set_fontsize(16)
    text.set_fontname(myfont)
    text.set_color(fontcolor)
    
# Change legend elements individually
#text = leg.get_texts() # get lines, patches, title, set_frame_on(True|False), set_title
#text[0].set_color('c')

 # Set / edit edge
plt.box(on=True) # Or nothing, to make the box disappear
       
# Set / edit grid
plt.grid()
ax.grid(color='paleturquoise', linestyle='-.', linewidth=0.5) # Requires ax = fig.add_subplot(111)

# Set background
# fig.set_facecolor('c') # Color around the plot
#ax.set_facecolor('#f5ffff') # Needs box to work

# Edit plot size
fig.set_size_inches(12,6.5)# Needs fig = plt.gcf()
plt.tight_layout() # Adjusts subplot params for the subplot(s) to fit in the figure area

# Show plot
#plt.show()
# Save plot
fig.savefig(output_file)
fhandle.close()
#--------------------------
# To time the script
time = datetime.now() - startTime
print ("\n(Script running time: " + str(time) + ")")

import re
import requests
from bs4 import BeautifulSoup
import sys


def getDownloadLink(videoUrl):
	base = "http://downsub.com/?url=" 	
	url = base + videoUrl

	try:
		r = requests.get(url)
		if r.status_code == 200:
			html = r.text
			soup = BeautifulSoup(html, 'lxml')

			for each in soup.find_all('a'):
				if 'index' in each['href']:
					downloadLink = base[0:19] + each['href'][2:]
					return downloadLink
	except:
		print("Error Occured!")
		sys.exit(-1)


def getSubtitles(downloadLink):
	try:
		r = requests.get(downloadLink)
		if r.status_code == 200:
			return r.text
	except:
		print("Error Occured!")
		sys.exit(-1)


def is_time_stamp(l):
	if l[:2].isnumeric() and l[2] == ':':
		return True
	return False


def has_letters(line):
	if re.search('[a-zA-Z]', line):
		return True
	return False


def has_no_text(line):
	l = line.strip()
	if not len(l):
		return True
	if l.isnumeric():
		return True
	if is_time_stamp(l):
		return True
	if l[0] == '(' and l[-1] == ')':
		return True
	if not has_letters(line):
		return True
	return False


def is_lowercase_letter_or_comma(letter):
	if letter.isalpha() and letter.lower() == letter:
		return True
	if letter == ',':
		return True
	return False


def clean_up(lines):
	new_lines = []
	for line in lines[1:]:
		if has_no_text(line):
			continue
		elif len(new_lines) and is_lowercase_letter_or_comma(line[0]):
			new_lines[-1] = new_lines[-1].strip() + ' ' + line
		else:
			new_lines.append(line)

	return new_lines


def convertText(subtitles):
	subtitles = subtitles.split('\n')
	subtitlesText = clean_up(subtitles)
	subtitlesText = '-'.join(subtitlesText)
	return subtitlesText


if __name__ == '__main__':
	f = open('videos.txt', 'r')
	text = f.read()
	text = text.split()

	for videoUrl in text:
		downloadLink = getDownloadLink(videoUrl)
		subtitles = getSubtitles(downloadLink)
		subtitlesText = convertText(subtitles)

		soup = BeautifulSoup(subtitlesText, 'lxml')
		subtitlesText = soup.get_text() 

		file = open('Subtitles/'+videoUrl[-11:]+'.txt', 'w+')
		file.write(subtitlesText)
		file.close()
		print(videoUrl[-11:] + ' Completed!')

	f.close()
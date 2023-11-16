import re


sentence = 'Do I like cats? Yes!!'
template = 'Do I like cats\? Yes\!\!'
tem = re.match(template, sentence)
#print(tem)
import re
text = 'MIKE an entry for mike WILL and here is wills text DAVID and this belongs to david'

subs = ['MIKE','WILL','TOM','DAVID']

res = re.findall(r'({0})\s*(.*?)(?=\s*(?:{0}|$))'.format("|".join(subs)), text)

print(res)
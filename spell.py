import streamlit as st
import re
from collections import Counter
from pprint import pprint

#from functools import filter

def words(text): return re.findall(r'\w+', text.lower())
word_count = Counter(words(open('big.txt').read()))
N = sum(word_count.values())
def P(word): return word_count[word] / N # float

#Run the function:

print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
    
#Run the function:
#pprint( list(edits1('speling'))[:3])
#pprint( list(map(lambda x: (x, P(x)), edits1('speling'))) )
#print( list(filter(lambda x: P(x) != 0.0, edits1('speling'))) )
#print( max(edits1('speling'), key=P) )

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    return set(w for w in words if w in word_count)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
 
print('speling -->', correction('speling'))
# speling spelling

# st.write(correction('speling')) #召喚出上面的＝＝＝＝＝＝prints
st.title("Spellchecker Demo")


fuck = st.selectbox('Choose a word or...',['apple','balloon','lamon','snow','speling','hapy','language'], help='You really need instructions for this?')
if fuck == 'snow':
    st.snow()
if fuck == 'balloon':
    st.balloons()
fuck = st.text_input('Type your own!!', value=fuck, help='Type a word, any word.')
if fuck == correction(fuck):
    st.success("This is a success message!" + correction(fuck), icon="✅")
if fuck != correction(fuck): #check the spell !=是否定
    st.error("Correction:  " + correction(fuck), icon="🚨")

check = st.sidebar.checkbox('Show original word')
if check :
    st.write("Original word:"+ fuck )

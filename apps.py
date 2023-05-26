from flask import Flask,render_template,request,url_for
import numpy as np


import pickle 
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           img=list(popular_df['Image-URL-M'].values),
                           author=list(popular_df['Book-Author'].values),
                           avg_rating=list(popular_df['Mean_Rating'].values),
                           num_rating=list(popular_df['Num_of_Rating'].values),
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend_books():
    book_name=request.form.get('book_name')
    book_name=book_name.title()
    
    index = np.where(pt.index==book_name) [0]
    data=[]
    if len(index)!=0:
        index=index[0]
        book_list=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:11]
        
        for i in book_list:
            item=[]
            match=books[books['Book-Title']==pt.index[i[0]]]
            item.extend(list(match.drop_duplicates('Book-Title')['Book-Title']))
            item.extend(list(match.drop_duplicates('Book-Title')['Book-Author']))
            item.extend(list(match.drop_duplicates('Book-Title')['Image-URL-M']))
            data.append(item)
        
    return render_template('recommend.html',data=data,book=book_name)

                        
if __name__=='__main__':
    app.run(debug=True)
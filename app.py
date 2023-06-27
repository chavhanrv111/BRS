from flask import Flask,render_template,request,url_for,redirect
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('index.html',Books = list(popular_df['Book-Title']),
                                        Num_rating = list(popular_df['Num-Rating']),
                                        Avg_Rating = list(popular_df['Avg-Rating']),
                                        Book_Author = list(popular_df['Book-Author']),
                                        Image = list(popular_df['Image-URL-M']))

@app.route('/about')
def about():    
    return render_template('about.html')

@app.route('/search_book',methods=["POST"])
def search_book():
    book_name = request.form.get('Book_Search')
    # if request.method != 'POST' or request.method != 'GET':
    #     return redirect(url_for('index'))
    try:
        index = np.where(pt.index==book_name)[0][0]
    except Exception:
        return render_template('index.html',search_result = [None,book_name] )

    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[0:13]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        data.append(item)
        
    return render_template('book.html',search_result = data)

if __name__ == '__main__':
    app.run(debug=True)
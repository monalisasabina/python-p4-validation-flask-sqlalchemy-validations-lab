from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self,key,name):

        if not name:
            raise ValueError('Author must have a name')
        
        existing_author = Author.query.filter(Author.name == name).first()

        if existing_author:
            raise ValueError('No two authors have the same name')

        return name
    
    @validates('phone_number')
    def validate_phone_number(self,key,number):

        if len(number) !=10 or not number.isdigit():
            raise ValueError('Author phone number must be in 10 digits')
        
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'



class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self,key,content):
        if len(content) <250:
            raise ValueError('The content should be at least 250 characters long')

        return content
    
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError('The summary must have a maximum of 250 characters')
        
        return summary
    
    @validates('category')
    def validate_category(self,key,category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('The category is either Fiction or Non-Fiction')
        return category

    @validates('title')
    def validate_title(self,key,title):

        clickbait= ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(phrase in title for phrase in clickbait):

            raise ValueError("No clickbait found. The title must contain at least one of the following phrases: 'Won\'t Believe', 'Secret', 'Top', or 'Guess'.")
        
        return title
        
        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

import streamlit as st
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')
    conn.commit()
    conn.close()

# Add a book
def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

# Get all books
def get_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

# Delete a book
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Streamlit UI
def main():
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")
    st.markdown(""" <h1 style='text-align: center; color: #4CAF50;'>📚 Personal Library Manager</h1> """, unsafe_allow_html=True)

    menu = ["Add Book", "View Books", "Delete Book"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
        
        if st.button("Add Book", help="Click to add book"):
            if title and author and year:
                add_book(title, author, year)
                st.success(f"Added '{title}' by {author}")
            else:
                st.warning("Please fill all fields")

    elif choice == "View Books":
        st.subheader("Library Books")
        books = get_books()
        if books:
            for book in books:
                st.markdown(f""" 
                **📖 {book[1]}**  
                *✍️ {book[2]}* (🗓 {book[3]})  
                🆔 {book[0]}
                """)
        else:
            st.info("No books found")

    elif choice == "Delete Book":
        st.subheader("Delete a Book")
        books = get_books()
        book_dict = {f"{book[1]} by {book[2]} ({book[3]})": book[0] for book in books}
        selected_book = st.selectbox("Select Book to Delete", list(book_dict.keys()))
        
        if st.button("Delete", help="Remove selected book"):
            delete_book(book_dict[selected_book])
            st.success(f"Deleted {selected_book}")
            st.experimental_rerun()

if __name__ == "__main__":
    init_db()
    main()
    
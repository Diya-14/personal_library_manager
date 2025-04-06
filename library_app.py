import streamlit as st
from library_manager import LibraryManager, Book
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #e9ecef;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #6c757d;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #5a6268;
        color: white;
    }
    .book-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize library manager
@st.cache_resource
def get_library_manager():
    return LibraryManager()

manager = get_library_manager()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Add Book", "View Library", "Search Books", "Statistics"])

# Main content
st.title("📚 Personal Library Manager")

if page == "Add Book":
    st.header("Add a New Book")
    
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title", placeholder="Enter book title")
            author = st.text_input("Author", placeholder="Enter author name")
            year = st.number_input("Publication Year", min_value=1000, max_value=2100, value=2023)
        
        with col2:
            genre = st.text_input("Genre", placeholder="Enter genre")
            read_status = st.radio("Read Status", ["Read", "Unread"])
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author and genre:
                book = Book(
                    title=title,
                    author=author,
                    year=year,
                    genre=genre,
                    read=(read_status == "Read")
                )
                manager.add_book(book)
                st.success("Book added successfully!")
            else:
                st.error("Please fill in all required fields (Title, Author, Genre)")

elif page == "View Library":
    st.header("Your Library")
    
    books = manager.get_all_books()
    
    if not books:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Display filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_read = st.selectbox("Filter by read status", ["All", "Read", "Unread"])
        
        with col2:
            sort_option = st.selectbox("Sort by", ["Title A-Z", "Title Z-A", "Author A-Z", "Author Z-A", "Year Newest", "Year Oldest"])
        
        with col3:
            st.write("")  # Empty column for layout
        
        # Apply filters and sorting
        filtered_books = books
        
        if filter_read == "Read":
            filtered_books = [book for book in filtered_books if book.read]
        elif filter_read == "Unread":
            filtered_books = [book for book in filtered_books if not book.read]
        
        if sort_option == "Title A-Z":
            filtered_books.sort(key=lambda x: x.title.lower())
        elif sort_option == "Title Z-A":
            filtered_books.sort(key=lambda x: x.title.lower(), reverse=True)
        elif sort_option == "Author A-Z":
            filtered_books.sort(key=lambda x: x.author.lower())
        elif sort_option == "Author Z-A":
            filtered_books.sort(key=lambda x: x.author.lower(), reverse=True)
        elif sort_option == "Year Newest":
            filtered_books.sort(key=lambda x: x.year, reverse=True)
        elif sort_option == "Year Oldest":
            filtered_books.sort(key=lambda x: x.year)
        
        # Display books
        for book in filtered_books:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="book-card">
                        <h4>{book.title}</h4>
                        <p><b>Author:</b> {book.author} | <b>Year:</b> {book.year} | <b>Genre:</b> {book.genre}</p>
                        <p><b>Status:</b> {"✅ Read" if book.read else "📖 Unread"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("Remove", key=f"remove_{book.title}"):
                        manager.remove_book(book.title)
                        st.rerun()

elif page == "Search Books":
    st.header("Search Books")
    
    search_option = st.radio("Search by", ["Title", "Author"])
    search_term = st.text_input(f"Enter {search_option.lower()} to search for")
    
    if search_term:
        results = manager.search_books(search_term, search_option.lower())
        
        if results:
            st.success(f"Found {len(results)} matching book(s)")
            
            for book in results:
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <h4>{book.title}</h4>
                        <p><b>Author:</b> {book.author} | <b>Year:</b> {book.year} | <b>Genre:</b> {book.genre}</p>
                        <p><b>Status:</b> {"✅ Read" if book.read else "📖 Unread"}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching books found")

elif page == "Statistics":
    st.header("Library Statistics")
    
    stats = manager.get_statistics()
    books = manager.get_all_books()
    
    if not books:
        st.info("Your library is empty. Add some books to see statistics!")
    else:
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>Total Books</h3>
                <h2>{stats['total_books']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>Read</h3>
                <h2>{stats['percentage_read']:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            genres = [book.genre for book in books]
            unique_genres = len(set(genres)) if genres else 0
            st.markdown(f"""
            <div class="stats-card">
                <h3>Unique Genres</h3>
                <h2>{unique_genres}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Genre distribution chart
        st.subheader("Genre Distribution")
        if len(set(genres)) > 0:
            genre_counts = pd.Series(genres).value_counts().reset_index()
            genre_counts.columns = ['Genre', 'Count']
            st.bar_chart(genre_counts.set_index('Genre'))
        else:
            st.info("No genre data available")
        
        # Read status pie chart
        st.subheader("Read Status")
        read_counts = pd.Series(["Read" if book.read else "Unread" for book in books]).value_counts().reset_index()
        read_counts.columns = ['Status', 'Count']
        st.bar_chart(read_counts.set_index('Status'))
        
        # Publication year distribution
        st.subheader("Publication Years")
        years = [book.year for book in books]
        if years:
            year_counts = pd.Series(years).value_counts().sort_index().reset_index()
            year_counts.columns = ['Year', 'Count']
            st.line_chart(year_counts.set_index('Year'))
        else:
            st.info("No publication year data available")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d;">
        <p>Personal Library Manager © 2025 | Made with Streamlit| Made by Diya</p>
    </div>
    """, unsafe_allow_html=True)
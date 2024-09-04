from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///music_portfolio.db")


@app.route("/")
def index():
    '''
    Display search bar for searching musicians
    '''
    # Get current search term and lower all letters to be case-insensitive
    search_query = request.args.get("search", "").lower()

    # Perform search query if a search term is provided
    if search_query:
        # Show 50 similar search queries from database
        musicians = db.execute(
            "SELECT * FROM musicians WHERE LOWER(username) LIKE ? LIMIT 50", f"%{search_query}%"
        )
        return render_template("index.html", musicians=musicians, search_query=search_query, searched=True)
    return render_template("index.html")


@app.route("/own_profile")
def own_profile():
    '''
    Show own user's profile and allow to add or delete pieces
    '''
    # Get all user information
    username = session["username"]
    user = db.execute("SELECT * FROM musicians WHERE username = ?", username)

    # Get also pieces of portfolio from user
    if user:
        user = user[0]
        pieces = db.execute("SELECT * FROM pieces WHERE musician_id = ?", user["id"])
        return render_template("own_profile.html", user=user, pieces=pieces)
    else:
        flash("User not found.", "danger")
        return redirect(url_for("index"))


@app.route("/profile/<int:musician_id>")
def profile(musician_id):
    '''
    Link to a musician accessed from the search bar including user information and pieces played
    '''
    # Get all information from a searched user
    musician = db.execute("SELECT * FROM musicians WHERE id = ?", musician_id)
    pieces = db.execute("SELECT * FROM pieces WHERE musician_id = ?", musician_id)

    # Display his information in profile.html
    if musician:
        return render_template("profile.html", musician=musician[0], pieces=pieces)
    else:
        return "Musician not found", 404


@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    Register for the page
    '''

    # POST method
    if request.method == "POST":
        # Gather all information required from registering musician
        name = request.form["name"]
        instrument = request.form["instrument"]
        bio = request.form["bio"]
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        # Validate that passwords match
        if password != confirmation:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("register"))

        # Hash the password
        password_hash = generate_password_hash(password)

        # Store information in database
        try:
            db.execute(
                "INSERT INTO musicians (username, name, instrument, bio, password_hash) VALUES (?, ?, ?, ?, ?)",
                username, name, instrument, bio, password_hash
            )
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists. Please choose another.", "danger")

    # GET method
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Login with username and password
    '''
    # POST method
    if request.method == "POST":
        # Get username and password
        username = request.form["username"]
        password = request.form["password"]

        # Get also information from this user from database
        musician = db.execute("SELECT * FROM musicians WHERE username = ?", username)

        # Check that password is same as the one storred in database
        if musician and check_password_hash(musician[0]["password_hash"], password):
            print("success")
            session["user_id"] = musician[0]["id"]
            session["username"] = musician[0]["username"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "danger")

    # GET method
    return render_template("login.html")


@app.route("/logout")
def logout():
    '''
    Logout with account
    '''
    # Clear session and cookies
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/add_piece", methods=["GET", "POST"])
def add_piece():
    '''
    Adding a piece to the current portfolio
    '''
    # Only allow to add a piece if user is logged in
    if "user_id" not in session:
        flash("You need to log in to add a piece.", "danger")
        return redirect(url_for("login"))

    # POST method
    if request.method == "POST":
        # Collect information regarding new piece
        title = request.form["title"]
        composer = request.form["composer"]
        year = request.form["year"]
        musician_id = session["user_id"]

        # Insert into database
        db.execute("INSERT INTO pieces (title, composer, year, musician_id) VALUES (?, ?, ?, ?)",
                   title, composer, year, musician_id)
        flash("Piece added successfully!", "success")
        return redirect(url_for("profile", musician_id=musician_id))

    # GET method
    return render_template("add_piece.html")


@app.route("/delete_piece/<int:piece_id>", methods=["POST"])
def delete_piece(piece_id):
    '''
    Deleting piece from the current portfolio
    '''
    # Only allow deletion if the user is logged in
    if "user_id" not in session:
        flash("You need to log in to delete a piece.", "danger")
        return redirect(url_for("login"))

    # Get the musician_id of the piece to be deleted
    piece = db.execute("SELECT musician_id FROM pieces WHERE id = ?", piece_id)

    # If piece doesn't exist, show error
    if not piece:
        flash("Piece not found.", "danger")
        return redirect(url_for("index"))

    musician_id = piece[0]["musician_id"]

    # Only allow deletion if the logged-in user is the owner of the piece
    if musician_id != session["user_id"]:
        flash("You do not have permission to delete this piece.", "danger")
        return redirect(url_for("index"))

    # Delete the piece from the database
    db.execute("DELETE FROM pieces WHERE id = ?", piece_id)
    flash("Piece deleted successfully.", "success")

    # Redirect to the user's own profile page after deletion
    return redirect(url_for("own_profile"))



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    '''
    Change information from own user profile
    '''
    # Only allow to edit profile if user is logged in
    if "user_id" not in session:
        flash("You need to log in to edit your profile.", "danger")
        return redirect(url_for("login"))

    # Get user information from database
    musician_id = session["user_id"]
    musician = db.execute("SELECT * FROM musicians WHERE id = ?", musician_id)[0]

    # POST method
    if request.method == "POST":
        # Collect new information regarding the user
        name = request.form["name"]
        instrument = request.form["instrument"]
        bio = request.form["bio"]
        password = request.form["password"]
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Check if new password and confirmation match
        if new_password and new_password != confirmation:
            flash("New password and confirmation do not match.", "danger")
            return render_template("edit_profile.html", musician=musician)

        # Validate current password if new password is provided
        if new_password and not check_password_hash(musician["password_hash"], password):
            flash("Current password is incorrect.", "danger")
            return render_template("edit_profile.html", musician=musician)

        # Update password if a new one is provided and valid
        if new_password:
            password_hash = generate_password_hash(new_password)
            db.execute("UPDATE musicians SET password_hash = ? WHERE id = ?", (password_hash, musician_id))

        # Update other profile details
        db.execute(
            "UPDATE musicians SET name = ?, instrument = ?, bio = ? WHERE id = ?",
            name, instrument, bio, musician_id
        )
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile", musician_id=musician_id))

    # GET method
    return render_template("edit_profile.html", musician=musician)

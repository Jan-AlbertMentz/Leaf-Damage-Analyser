# Import the required libraries
import psycopg2
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

# Method to create a connection object
# It creates a pointer cursor to the database
# and returns it along with Connection object
def create_connection():
    # Connect to the database
    # using the psycopg2 adapter.
    # Pass your database name ,# username , password ,
    # hostname and port number
    conn = psycopg2.connect(dbname='TestImageDB',
                            user='postgres',
                            password='1234',
                            host='localhost',
                            port='5432')
    # Get the cursor object from the connection object
    curr = conn.cursor()
    return conn, curr


def create_table():
    try:
        # Get the cursor object from the connection object
        conn, curr = create_connection()
        try:
            # Fire the CREATE query
            curr.execute("CREATE TABLE IF NOT EXISTS \
            cartoon(cartoonID INTEGER, name TEXT, \
                cartoonImg BYTEA)")

        except(Exception, psycopg2.Error) as error:
            # Print exception
            print("Error while creating cartoon table", error)
        finally:
            # Close the connection object
            conn.commit()
            conn.close()
    finally:
        # Since we do not have to do anything here we will pass
        pass


def write_blob(cartoonID, file_path, name):
    try:
        # Read data from a image file
        drawing = open(file_path, 'rb').read()
        # Read database configuration
        conn, cursor = create_connection()
        try:
            # Execute the INSERT statement
            # Convert the image data to Binary
            cursor.execute("INSERT INTO cartoon\
                           (cartoonID,name,cartoonImg) " +
                           "VALUES(%s,%s,%s)",
                           (cartoonID, name, psycopg2.Binary(drawing)))
            # Commit the changes to the database
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in cartoon table", error)
        finally:
            # Close the connection object
            conn.close()
    finally:
        # Since we do not have to do
        # anything here we will pass
        pass


# Call the create table method
create_table()
# Prepare sample data, of images, from local drive
write_blob(1, "ImagesForDatabase/ImageData.png", "Test1")
write_blob(2, "ImagesForDatabase/ImageWithScar.jpeg", "Test2")
write_blob(3, "ImagesForDatabase/4&8Square.jpg", "Test3")
write_blob(4, "ImagesForDatabase/data1.png", "Test4")
write_blob(5, "ImagesForDatabase/4&8SquareCopy.jpg", "Test5")


# Fetch the image data from the database
def fetch_images():
    try:
        conn, cursor = create_connection()
        cursor.execute("SELECT cartoonImg, name FROM cartoon")
        images = cursor.fetchall()
        conn.close()
        return images
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while fetching images:", error)
        return []


# Display the images in a window
def display_images(images):
    root = tk.Tk()
    root.title("Image Display")

    for idx, (image_data, image_name) in enumerate(images):
        # Convert binary data into image
        image = Image.open(BytesIO(image_data))

        # Resize the image if necessary
        image = image.resize((200, 200), Image.LANCZOS)

        # Convert image to ImageTk format to display in Tkinter
        img_tk = ImageTk.PhotoImage(image)

        # Create a label to display the image and name
        label = tk.Label(root, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.grid(row=idx, column=0)

        name_label = tk.Label(root, text=image_name)
        name_label.grid(row=idx, column=1)

    root.mainloop()

# Main flow
if __name__ == "__main__":
    # Fetch images from the database
    images = fetch_images()

    if images:
        # Display images in a window
        display_images(images)
    else:
        print("No images to display.")
print ("Starting server...")
from app.main import create_app

print ("Creating app instance...")

app = create_app()

if __name__ == "__main__":
    print("Running app now...")
    app.run(debug=True)
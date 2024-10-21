import sys
import json
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Generative AI")
        self.setGeometry(100, 100, 600, 400)

        # Layouts
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Chat Display
        self.chat_display = QtWidgets.QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        self.layout.addWidget(self.chat_display)

        # User Input Field
        self.input_field = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.input_field)

        # Send Button
        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Styling
        self.chat_display.setStyleSheet("font-size: 14px;")
        self.input_field.setStyleSheet("font-size: 14px; padding: 10px;")
        self.send_button.setStyleSheet("font-size: 14px; padding: 10px;")

    def get_gemini_response(self, user_input):
        # api_key = "AIzaSyCzEESbDIwLoIcHf15VVXKfr08qMz1Smas"
        api_key = "AIzaSyAZ6SU9oJhKL-xz2xW1JkLmhQ9-MG5O9H0"  # Replace with your actual API key
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {"parts": [{"text": user_input}]}
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response_json = response.json()
                print(response_json,"test")
                return response_json['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    def send_message(self):
        user_input = self.input_field.text()
        if user_input.strip():
            # Display user message
            self.chat_display.append(f"<b>You:</b> {user_input}")
            
            # Get and display API response
            response = self.get_gemini_response(user_input)
            print(response)
            self.chat_display.append(f"<b>AI:</b> {response}")

            # Clear input field
            self.input_field.clear()
            self.chat_display.moveCursor(QtGui.QTextCursor.End)

def main():
    app = QtWidgets.QApplication(sys.argv)
    chatbot = ChatbotApp()
    chatbot.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

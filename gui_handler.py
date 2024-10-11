import tkinter as tk
from tkinter import scrolledtext
from model_handler import get_response

# GUI application using Tkinter
class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with Max")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=80, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input area
        self.user_input = tk.Entry(root, width=60)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip() == "":
            return

        # Display user message
        self.update_chat_display(f"You: {user_message}\n")

        # Get response from the model
        assistant_response = get_response(user_message)

        # Display assistant message
        self.update_chat_display(f"Max: {assistant_response}\n")

        # Clear user input field
        self.user_input.delete(0, tk.END)

    def update_chat_display(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message)
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApplication(root)
    root.mainloop()
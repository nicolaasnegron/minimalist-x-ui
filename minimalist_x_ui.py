import tkinter as tk  # GUI
from tkinter import ttk # GUI style
import tweepy # X API access
import os # OS access

# Define our application as a Class
class MinimalistUI:
    # Define the constructor
    def __init__(self, root):
        self.root = root # Main window
        self.setup_ui() # Adjust UI
        self.setup_api() # Connect to X API

    def setup_ui(self):
        # Configure UI elements
        self.root.geometry('677x400') # Main window resolution
        self.root.overrideredirect(True)  # Remove default border and title bar
        self.setup_dark_theme()
        self.create_title_bar()
        self.text_input = self.create_text_input()
        self.create_progress_bar()
        self.create_buttons()

    def setup_api(self):
        # Authenticate session w/ X API via OAuth 1.0a
        # Retrieve key, token, and secrets from environmental variables
        self.client = tweepy.Client(
            consumer_key = os.getenv('X_API_KEY'),
            consumer_secret = os.getenv('X_API_SECRET'),
            access_token = os.getenv('X_ACCESS_TOKEN'),
            access_token_secret = os.getenv('X_ACCESS_SECRET'))

        # For debugging API connection
        # print("API setup complete")
        # print("API Key:", os.getenv('X_API_KEY'))
        # print("API Secret:", os.getenv('X_API_SECRET'))
        # print("Access Token:", os.getenv('X_ACCESS_TOKEN'))
        # print("Access Secret:", os.getenv('X_ACCESS_SECRET'))

    def setup_dark_theme(self):
        # Apply dark theme to UI
        self.root.configure(background='#252526')
        style = ttk.Style() # Create a style object to customize ttk widgets
        style.theme_use('alt')

        # Create style configurations for buttons and labels
        button_style = {'background': '#3E3E42', 'foreground': '#FFFFFF',
                        'width': 20}
        label_entry_style = {'background': '#252526', 'foreground': '#FFFFFF'}

        # Unpack button and label style config, set style for progress bar
        style.configure('TButton', **button_style)
        style.configure('TLabel', **label_entry_style)
        style.configure('TEntry', **label_entry_style)
        style.configure('Horizontal.TProgressbar',
                        background='#555555', troughcolor='#3E3E42')

        # Set custom styles for the title bar and close button
        style.configure('Title.TFrame', background='#252526')
        style.configure('Close.TButton', foreground='#D11A2A',
                        background='#333333', font=('Helvetica', 9, 'bold'))
        style.map('TButton',
                  background=[('active', '#334353')])

    def create_text_input(self):
        # Create a frame for text input and success message
        self.input_frame = tk.Frame(self.root, background='#252526')
        self.input_frame.pack(pady=20)

        # Create space to capture User's text input
        self.text_input = tk.Text(self.root, height=12, width=60,
                             background='#252526',
                             foreground='#FEFEFE', wrap='word')
        self.text_input.config(font=('Arial Narrow', 12),
                               undo=True, wrap='word')
        self.text_input.pack()
        self.text_input.bind('<KeyRelease>', self.update_progress)
        return self.text_input

    def create_progress_bar(self):
        # Create progress bar, assign custom style Horizontal.TProgressbar
        style = ttk.Style()
        style.theme_use(
            'alt')
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal',
                                            length=200, mode='determinate',
                                            maximum=280,
                                            style='Horizontal.TProgressbar')
        self.progress_bar.pack(pady=10)

    def create_buttons(self):
        # Create action button to send Tweet
        buttons_frame = tk.Frame(self.root, background='#252526')
        buttons_frame.pack(fill=tk.X, pady=10)
        send_button = ttk.Button(buttons_frame, text="Send Tweet",
                                 command=self.send_tweet)
        send_button.pack(side=tk.LEFT, expand=True, padx=5)

        #         # Update button style when cursor overhead
        def on_enter(e):
            e.widget[
                'style'] = 'Hover.TButton'  # Change to hover style
        def on_leave(e):
            e.widget[
                'style'] = 'TButton'  # Revert to original style

    def create_title_bar(self):
        # Create custom title bar for application window
        title_bar = tk.Frame(self.root, bg='#252526', relief='raised', bd=0,
                             highlightthickness=0)
        title_bar.pack(fill=tk.X)
        title_label = tk.Label(title_bar,
                               text="Hello friend, "
                                    "what would you like to share?",
                               bg='#252526', fg='#FFFFFF')
        title_label.config(font=('Arial Narrow', 12))
        title_label.pack(side=tk.LEFT, padx=15)

        close_button = ttk.Button(title_bar, text="X", style='Close.TButton',
                                  command=self.root.destroy)
        close_button.pack(side=tk.RIGHT, pady=2, padx=5)

        # Implement drag functionality for the title bar
        title_bar.bind('<Button-1>', self.on_title_bar_click)
        title_bar.bind('<B1-Motion>', self.on_title_bar_drag)

    def on_title_bar_click(self, event):
        # Implement click functionality for the title bar
        # Records the initial position of a mouse click on the title bar
        self.offset_x = event.x
        self.offset_y = event.y

    def on_title_bar_drag(self, event):
        # Allows the window to be dragged by the title bar
        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y
        self.root.geometry(f"+{x}+{y}") # Move the window to the new position

    def update_progress(self, event):
        # Limit text entry to <280 characters
        text = self.text_input.get("1.0", tk.END)
        input_length = len(text) - 1
        # Update progress
        self.progress_bar['value'] = input_length
        # Limit the input to 280 character
        if self.progress_bar['value'] > 280:
            self.text_input.delete("1.0+280c", tk.END)

    def send_tweet(self):
        # Retrieve text input and send tweet
        tweet = self.text_input.get("1.0", tk.END).strip()
        if tweet:  # Check if the tweet content is not empty
            try:
                response = self.client.create_tweet(text=tweet)
                print("Tweet successfully sent!", response)
                self.clear_input_and_print_success()
            except tweepy.TweepyException as e:
                print(f"Tweepy Error: {e}")
                self.clear_input_and_print_error()
                raise
            except Exception as e:
                print(f"General Error: {e}")
                self.clear_input_and_print_error()
                raise

    def clear_input_and_print_success(self):
        # Display a success message
        self.success_message = ttk.Label(self.root,
                                    text="Tweet successfully sent!",
                                    foreground="#03A062")
        self.success_message.pack()

    def clear_input_and_print_error(self):
        # Display a failure message
        self.failure_message = ttk.Label(self.root,
                                    text="Tweet failed to send!",
                                    foreground="#D11A2A")
        self.failure_message.pack()
        def clean_up():
            # Optional: remove the success or failure  message after a few sec
            self.success_message.destroy()
            self.failure_message.destroy()
            # Clear the text input area
            self.text_input.delete("1.0", tk.END)
            self.progress_bar['value'] = 0

        self.success_message.after(5000, clean_up)
        self.error_message.after(5000, clean_up)

# The following code block is executed when the script is run directly
if __name__ == "__main__":
    root = tk.Tk()
    app = MinimalistUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import json
import os
import threading
import time
from pathlib import Path
from datetime import datetime


class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 SecureBank - Facial Authentication")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")

        # Data storage
        self.users_file = "users_data.json"
        self.users_data = self.load_users_data()

        # Webcam setup
        self.cap = None
        self.camera_active = False
        self.current_frame = None
        self.current_frame_lock = threading.Lock()
        self.detection_result = None
        self.face_detected = False
        self.capture_requested = False
        self.last_face_locations = []

        # Mode
        self.mode = "preview"  # 'preview', 'register' or 'login'
        self.current_username = None
        self.logged_in_user = None

        # Auto-capture settings
        self.auto_capture = tk.BooleanVar(value=False)
        self.face_stable_count = 0
        self.required_stable_frames = 20

        # Apply custom styles
        self.setup_styles()

        # Create GUI
        self.create_widgets()

        # Start camera preview automatically after a short delay
        self.root.after(500, self.start_preview)

    def setup_styles(self):
        """Configure custom ttk styles"""
        style = ttk.Style()
        style.theme_use("clam")

        # Button styles
        style.configure("Primary.TButton", font=("Helvetica", 11, "bold"), padding=10)
        style.configure("Success.TButton", font=("Helvetica", 11, "bold"), padding=10)
        style.configure("Danger.TButton", font=("Helvetica", 11, "bold"), padding=10)
        style.configure("Capture.TButton", font=("Helvetica", 12, "bold"), padding=15)

    def create_widgets(self):
        """Create main UI components"""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#1f4788", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="🏦 SecureBank Authentication System",
            font=("Helvetica", 22, "bold"),
            fg="white",
            bg="#1f4788",
        )
        title_label.pack(pady=20)

        # Main container
        main_container = tk.Frame(self.root, bg="#f5f6fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Left side - Webcam feed
        left_frame = tk.Frame(main_container, bg="#f5f6fa")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Webcam container with border
        webcam_container = tk.Frame(left_frame, bg="#1f4788", padx=3, pady=3)
        webcam_container.pack(pady=10)

        self.video_label = tk.Label(webcam_container, bg="black", width=640, height=480)
        self.video_label.pack()

        # Capture button (below video)
        self.capture_btn = tk.Button(
            left_frame,
            text="📸 CAPTURE FACE",
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            width=25,
            height=2,
            state=tk.DISABLED,
            command=self.trigger_capture,
        )
        self.capture_btn.pack(pady=10)

        # Face detection indicator
        self.face_indicator = tk.Label(
            left_frame,
            text="👤 No face detected",
            font=("Helvetica", 11),
            fg="#7f8c8d",
            bg="#f5f6fa",
        )
        self.face_indicator.pack()

        # Right side - Controls
        right_frame = tk.Frame(main_container, bg="#ffffff", padx=20, pady=15)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0))

        # Control panel title
        control_label = tk.Label(
            right_frame,
            text="Control Panel",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#1f4788",
        )
        control_label.pack(pady=(0, 15))

        # Username section
        username_frame = tk.Frame(right_frame, bg="#ffffff")
        username_frame.pack(fill=tk.X, pady=5)

        username_label = tk.Label(
            username_frame, text="👤 Username:", font=("Helvetica", 11), bg="#ffffff"
        )
        username_label.pack(anchor=tk.W)

        self.username_entry = ttk.Entry(
            username_frame, width=28, font=("Helvetica", 12)
        )
        self.username_entry.pack(fill=tk.X, pady=5)

        # Action buttons
        button_frame = tk.Frame(right_frame, bg="#ffffff")
        button_frame.pack(pady=15, fill=tk.X)

        self.register_btn = tk.Button(
            button_frame,
            text="📝 Register New User",
            font=("Helvetica", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=22,
            height=2,
            command=self.register_face,
        )
        self.register_btn.pack(pady=5)

        self.login_btn = tk.Button(
            button_frame,
            text="🔓 Login with Face",
            font=("Helvetica", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            width=22,
            height=2,
            command=self.login_face,
        )
        self.login_btn.pack(pady=5)

        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop Camera",
            font=("Helvetica", 11),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            width=22,
            height=2,
            command=self.stop_camera,
        )
        self.stop_btn.pack(pady=5)

        # Auto-capture checkbox
        auto_frame = tk.Frame(right_frame, bg="#ffffff")
        auto_frame.pack(fill=tk.X, pady=5)

        self.auto_capture_check = tk.Checkbutton(
            auto_frame,
            text="🔄 Auto-capture when face stable",
            variable=self.auto_capture,
            font=("Helvetica", 10),
            bg="#ffffff",
        )
        self.auto_capture_check.pack(anchor=tk.W)

        # Separator
        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, pady=15)

        # Status section
        status_frame = tk.Frame(right_frame, bg="#ecf0f1", padx=10, pady=10)
        status_frame.pack(fill=tk.X)

        status_title = tk.Label(
            status_frame,
            text="Status",
            font=("Helvetica", 10, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
        )
        status_title.pack(anchor=tk.W)

        self.status_label = tk.Label(
            status_frame,
            text="✅ Ready - Enter username to begin",
            font=("Helvetica", 10),
            fg="#27ae60",
            bg="#ecf0f1",
            wraplength=220,
            justify=tk.LEFT,
        )
        self.status_label.pack(anchor=tk.W, pady=5)

        # Registered users section
        users_frame = tk.Frame(right_frame, bg="#ffffff")
        users_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        users_header = tk.Frame(users_frame, bg="#ffffff")
        users_header.pack(fill=tk.X)

        users_label = tk.Label(
            users_header,
            text="👥 Registered Users:",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
        )
        users_label.pack(side=tk.LEFT)

        # Delete user button
        self.delete_btn = tk.Button(
            users_header,
            text="🗑️",
            font=("Helvetica", 10),
            bg="#e74c3c",
            fg="white",
            width=3,
            command=self.delete_selected_user,
        )
        self.delete_btn.pack(side=tk.RIGHT)

        # Users listbox with scrollbar
        listbox_frame = tk.Frame(users_frame, bg="#ffffff")
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.users_listbox = tk.Listbox(
            listbox_frame,
            height=6,
            width=28,
            font=("Helvetica", 10),
            yscrollcommand=scrollbar.set,
            selectbackground="#3498db",
        )
        self.users_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.users_listbox.yview)

        self.update_users_list()

        # Exit button
        exit_btn = tk.Button(
            right_frame,
            text="🚪 Exit Application",
            font=("Helvetica", 11),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            width=22,
            height=2,
            command=self.close_app,
        )
        exit_btn.pack(pady=10)

        # Footer
        footer = tk.Label(
            self.root,
            text="🔒 Secure Facial Authentication System | © 2026 SecureBank",
            font=("Helvetica", 9),
            fg="#7f8c8d",
            bg="#f5f6fa",
        )
        footer.pack(side=tk.BOTTOM, pady=5)

        # Update loop
        self.update_video_feed()

    def start_preview(self):
        """Start camera in preview mode (no capture)"""
        self.mode = "preview"
        self.detection_result = None
        self.capture_btn.config(state=tk.DISABLED, bg="#95a5a6", text="📸 CAPTURE FACE")
        self.start_camera()
        self.update_status(
            "📹 Camera preview active\nEnter username and select an action"
        )

    def load_users_data(self):
        """Load user data from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users_data(self):
        """Save user data to JSON file"""
        # Convert numpy arrays to lists for JSON serialization
        data_to_save = {}
        for username, user_data in self.users_data.items():
            data_to_save[username] = {
                "face_embeddings": [
                    emb.tolist() if isinstance(emb, np.ndarray) else emb
                    for emb in user_data["face_embeddings"]
                ]
            }

        with open(self.users_file, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def trigger_capture(self):
        """Trigger face capture from button click"""
        self.capture_requested = True

    def delete_selected_user(self):
        """Delete selected user from the list"""
        selection = self.users_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        selected_text = self.users_listbox.get(selection[0])
        username = selected_text.split(" (")[0]

        if messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete user '{username}'?"
        ):
            if username in self.users_data:
                del self.users_data[username]
                self.save_users_data()
                self.update_users_list()
                self.update_status(f"🗑️ User '{username}' deleted successfully")

    def register_face(self):
        """Register a new user with facial data"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        if username in self.users_data:
            messagebox.showerror("Error", f"User '{username}' already exists")
            return

        self.mode = "register"
        self.current_username = username
        self.detection_result = None
        self.face_stable_count = 0
        self.capture_btn.config(
            state=tk.NORMAL, bg="#3498db", text="📸 CAPTURE TO REGISTER"
        )
        self.update_status(
            f"📸 Registering '{username}'...\nLook at the camera and click CAPTURE"
        )

        if not self.camera_active:
            self.start_camera()

    def login_face(self):
        """Login with facial recognition"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        if username not in self.users_data:
            messagebox.showerror("Error", f"User '{username}' not found")
            return

        self.mode = "login"
        self.current_username = username
        self.detection_result = None
        self.face_stable_count = 0
        self.capture_btn.config(
            state=tk.NORMAL, bg="#27ae60", text="📸 CAPTURE TO VERIFY"
        )
        self.update_status(
            f"🔓 Verifying '{username}'...\nLook at camera and click CAPTURE"
        )

        if not self.camera_active:
            self.start_camera()

    def start_camera(self):
        """Start camera feed in a separate thread"""
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
            camera_thread.start()

    def stop_camera(self):
        """Stop current mode and return to preview"""
        self.mode = "preview"
        self.current_username = None
        self.detection_result = None
        self.face_stable_count = 0
        self.capture_requested = False
        self.capture_btn.config(state=tk.DISABLED, bg="#95a5a6", text="📸 CAPTURE FACE")
        self.update_status(
            "📹 Camera preview active\nEnter username and select an action"
        )

    def fully_stop_camera(self):
        """Completely stop the camera"""
        self.camera_active = False
        time.sleep(0.1)  # Give camera thread time to stop
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.mode = None
        self.face_detected = False

    def camera_loop(self):
        """Main camera loop for capturing and processing frames"""
        frame_count = 0

        while self.camera_active and self.cap is not None:
            ret, frame = self.cap.read()

            if not ret:
                time.sleep(0.01)
                continue

            # Flip for selfie view
            frame = cv2.flip(frame, 1)

            # Only detect faces every 3rd frame for performance
            frame_count += 1
            if frame_count % 3 == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                self.last_face_locations = face_locations

                # Update face detection status
                if face_locations:
                    self.face_detected = True
                    self.face_stable_count += 1
                else:
                    self.face_detected = False
                    self.face_stable_count = 0

            # Use cached face locations for drawing
            face_locations = self.last_face_locations

            # Determine box color based on current state
            if self.detection_result == "Match":
                box_color = (0, 255, 0)  # Green BGR
            elif self.detection_result == "No Match":
                box_color = (0, 0, 255)  # Red BGR
            elif self.face_detected:
                box_color = (0, 255, 255)  # Yellow BGR
            else:
                box_color = (0, 255, 0)  # Default green

            # Draw rectangles around faces
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), box_color, 3)

                # Add label above the box
                if self.detection_result == "Match":
                    label = "ACCESS GRANTED"
                elif self.detection_result == "No Match":
                    label = "ACCESS DENIED"
                else:
                    label = "Face Detected"

                # Draw label background
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.rectangle(
                    frame,
                    (left, top - 30),
                    (left + label_size[0] + 10, top),
                    box_color,
                    -1,
                )
                cv2.putText(
                    frame,
                    label,
                    (left + 5, top - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

            # Handle capture request
            if self.capture_requested and self.mode in ("register", "login"):
                self.capture_requested = False
                if face_locations:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.process_face_capture(rgb_frame, face_locations)
                else:
                    self.root.after(
                        0, lambda: self.update_status("❌ No face detected. Try again.")
                    )

            # Auto-capture logic
            if (
                self.mode in ("register", "login")
                and self.auto_capture.get()
                and self.face_stable_count >= self.required_stable_frames
                and not self.capture_requested
                and self.detection_result is None
            ):
                self.capture_requested = True

            # Store frame for display
            with self.current_frame_lock:
                self.current_frame = frame.copy()

            time.sleep(0.01)  # Small delay to reduce CPU usage

        # Cleanup
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def process_face_capture(self, rgb_frame, face_locations):
        """Process captured face"""
        try:
            # Get face encodings
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if not face_encodings:
                self.root.after(
                    0,
                    lambda: self.update_status("❌ Could not encode face. Try again."),
                )
                return

            if self.mode == "register":
                self.handle_registration(face_encodings[0])
            elif self.mode == "login":
                self.handle_login(face_encodings[0])

        except Exception as e:
            error_msg = str(e)
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Face processing error: {error_msg}"
                ),
            )

    def handle_registration(self, face_encoding):
        """Handle user registration"""
        try:
            username = self.current_username
            if username not in self.users_data:
                self.users_data[username] = {"face_embeddings": [face_encoding]}
            else:
                self.users_data[username]["face_embeddings"].append(face_encoding)

            self.save_users_data()
            self.detection_result = "Success"
            self.root.after(0, self.show_registration_success)

        except Exception as e:
            error_msg = str(e)
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Registration failed: {error_msg}"
                ),
            )

    def handle_login(self, face_encoding):
        """Handle user login"""
        try:
            username = self.current_username
            stored_embeddings = self.users_data[username]["face_embeddings"]

            # Convert stored embeddings back to numpy arrays if needed
            stored_embeddings = [
                np.array(emb) if isinstance(emb, list) else emb
                for emb in stored_embeddings
            ]

            # Compare with stored embeddings
            distances = face_recognition.face_distance(stored_embeddings, face_encoding)
            best_match_distance = min(distances)

            # Threshold for face match (lower is better, typically 0.6 is good)
            if best_match_distance < 0.4:
                self.detection_result = "Match"
                self.root.after(0, self.show_login_success)
            else:
                self.detection_result = "No Match"
                self.root.after(0, self.show_login_failure)

        except Exception as e:
            error_msg = str(e)
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Login verification failed: {error_msg}"
                ),
            )

    def show_registration_success(self):
        """Show registration success message"""
        username = self.current_username
        self.update_status(f"✅ User '{username}' registered successfully!")
        self.update_users_list()
        self.username_entry.delete(0, tk.END)
        messagebox.showinfo(
            "Success",
            f"Welcome {username}!\nYour face has been registered successfully.",
        )
        self.stop_camera()

    def show_login_success(self):
        """Show login success and open dashboard"""
        username = self.current_username
        self.logged_in_user = username
        self.update_status(f"🟢 ACCESS GRANTED - Welcome {username}!")
        self.root.after(500, lambda: self.open_dashboard(username))

    def show_login_failure(self):
        """Show login failure message"""
        self.update_status("🔴 ACCESS DENIED - Face does not match!")
        messagebox.showerror(
            "Access Denied", "Face verification failed.\nPlease try again."
        )
        self.stop_camera()

    def open_dashboard(self, username):
        """Open user dashboard after successful login"""
        self.stop_camera()

        # Create dashboard window
        dashboard = tk.Toplevel(self.root)
        dashboard.title(f"🏦 SecureBank - Welcome {username}")
        dashboard.geometry("600x500")
        dashboard.configure(bg="#f5f6fa")
        dashboard.transient(self.root)
        dashboard.grab_set()

        # Header
        header = tk.Frame(dashboard, bg="#27ae60", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        welcome_label = tk.Label(
            header,
            text=f"🎉 Welcome, {username}!",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#27ae60",
        )
        welcome_label.pack(pady=20)

        # Main content
        content = tk.Frame(dashboard, bg="#f5f6fa", padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Account info
        info_frame = tk.Frame(content, bg="#ffffff", padx=20, pady=20)
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text="📊 Account Information",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#1f4788",
        ).pack(anchor=tk.W)

        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        tk.Label(
            info_frame,
            text=f"🕐 Login Time: {current_time}",
            font=("Helvetica", 11),
            bg="#ffffff",
        ).pack(anchor=tk.W, pady=5)

        tk.Label(
            info_frame,
            text=f"👤 Account Holder: {username}",
            font=("Helvetica", 11),
            bg="#ffffff",
        ).pack(anchor=tk.W, pady=5)

        tk.Label(
            info_frame,
            text="✅ Authentication: Facial Recognition",
            font=("Helvetica", 11),
            bg="#ffffff",
        ).pack(anchor=tk.W, pady=5)

        # Mock banking features
        features_frame = tk.Frame(content, bg="#ffffff", padx=20, pady=20)
        features_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            features_frame,
            text="🏦 Quick Actions",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#1f4788",
        ).pack(anchor=tk.W, pady=(0, 15))

        buttons_frame = tk.Frame(features_frame, bg="#ffffff")
        buttons_frame.pack(fill=tk.X)

        actions = [
            ("💰 View Balance", "#3498db"),
            ("📤 Transfer Money", "#9b59b6"),
            ("📜 Transaction History", "#f39c12"),
            ("⚙️ Account Settings", "#1abc9c"),
        ]

        for i, (text, color) in enumerate(actions):
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Helvetica", 11),
                bg=color,
                fg="white",
                width=18,
                height=2,
                command=lambda t=text: messagebox.showinfo(
                    "Demo", f"{t}\n\nThis is a demo feature."
                ),
            )
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)

        # Balance display (mock)
        balance_frame = tk.Frame(content, bg="#1f4788", padx=20, pady=15)
        balance_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            balance_frame,
            text="Available Balance",
            font=("Helvetica", 11),
            fg="#bdc3c7",
            bg="#1f4788",
        ).pack()

        tk.Label(
            balance_frame,
            text="$12,458.67",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg="#1f4788",
        ).pack()

        # Logout button
        logout_btn = tk.Button(
            content,
            text="🚪 Logout",
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            command=lambda: self.logout(dashboard),
        )
        logout_btn.pack(pady=20)

    def logout(self, dashboard):
        """Logout and close dashboard"""
        self.logged_in_user = None
        dashboard.destroy()
        self.update_status("✅ Logged out successfully")
        self.username_entry.delete(0, tk.END)

    def update_video_label(self, imgtk):
        """Update video feed label"""
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)

    def update_status(self, text):
        """Update status label"""
        self.status_label.config(text=text)

    def update_users_list(self):
        """Update registered users listbox"""
        self.users_listbox.delete(0, tk.END)
        if self.users_data:
            for username in sorted(self.users_data.keys()):
                num_faces = len(self.users_data[username]["face_embeddings"])
                self.users_listbox.insert(tk.END, f"{username} ({num_faces} face(s))")
        else:
            self.users_listbox.insert(tk.END, "No users registered")

    def update_video_feed(self):
        """Update video feed from main thread (called periodically)"""
        # Update video frame
        with self.current_frame_lock:
            if self.current_frame is not None:
                try:
                    rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb_frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.video_label.imgtk = imgtk
                    self.video_label.config(image=imgtk)
                except Exception:
                    pass

        # Update face indicator
        if self.camera_active:
            if self.face_detected:
                self.face_indicator.config(
                    text="✅ Face detected - Ready to capture", fg="#27ae60"
                )
            else:
                self.face_indicator.config(text="👤 No face detected", fg="#e74c3c")
        else:
            self.face_indicator.config(text="📷 Camera starting...", fg="#7f8c8d")

        self.root.after(33, self.update_video_feed)  # ~30 FPS

    def close_app(self):
        """Close application"""
        self.fully_stop_camera()
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
import requests
import numpy as np
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skyfield.api import load, EarthSatellite

# Space-Track API credentials (replace with your own)
USERNAME = "anshistar***@gmail.com"
PASSWORD = "*****"

# Space-Track TLE API endpoint for all debris
SPACE_TRACK_TLE_URL = "https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/>0/ORDINAL/1/format/tle"

# Login to Space-Track and fetch TLE data
session = requests.Session()
login_url = "https://www.space-track.org/ajaxauth/login"

try:
    # Authenticate
    login_data = {"identity": USERNAME, "password": PASSWORD}
    session.post(login_url, data=login_data)

    # Fetch TLE data
    response = session.get(SPACE_TRACK_TLE_URL)
    response.raise_for_status()
    tle_data = response.text.strip().split("\n")

    print("✅ TLE Data Fetched Successfully!")
    print("Preview:", tle_data[:10])  # Print first 10 lines for verification

except requests.exceptions.RequestException as e:
    print(f"❌ Failed to fetch data: {e}")
    exit()

# Step 2: Parse TLE Data
satellites = []
for i in range(0, len(tle_data) - 2, 3):
    try:
        name = tle_data[i].strip()
        tle_1 = tle_data[i + 1].strip()
        tle_2 = tle_data[i + 2].strip()
        satellites.append((name, tle_1, tle_2))
    except IndexError:
        continue  # Skip improperly formatted TLE sets

print(f"✅ Loaded {len(satellites)} space debris objects.")

# Step 3: User Input for Specific Object to Track
norad_id = input("Enter the NORAD ID of the satellite to track: ")

# Ensure matching for both "U" and "A" in the NORAD ID to correctly fetch data
selected_sat = None
for sat in satellites:
    if f"{norad_id}U" in sat[1] or f"{norad_id}A" in sat[1]:  # Match NORAD ID with TLE line 1
        selected_sat = sat
        break

if not selected_sat:
    print(f"⚠️ No matching object found for NORAD ID {norad_id}. Using a test satellite.")
    selected_sat = ("TEST-SAT", 
                    "1 99999U 23001A   24065.50000000  .00000000  00000-0  00000-0 0  9991", 
                    "2 99999  97.5000 122.5000 0001000  90.0000 270.0000 15.00000000 00001")

print(f"📡 Tracking: {selected_sat[0]}")

# Step 4: Compute Positions and Velocities
ts = load.timescale()
x_positions, y_positions, z_positions = [], [], []
vx, vy, vz = [], [], []
labels = []
collision_threshold = 200  # km threshold for alert
collision_alerts = []

# Compute positions of the tracked satellite
test_sat = EarthSatellite(selected_sat[1], selected_sat[2], selected_sat[0], ts)
test_pos = test_sat.at(ts.now()).position.km  # Position of selected satellite

# Compute positions of all debris (limiting to first 100 for efficiency)
for name, tle_1, tle_2 in satellites[:100]:  # Limiting to first 100 debris objects for efficiency
    try:
        satellite = EarthSatellite(tle_1, tle_2, name, ts)
        geocentric = satellite.at(ts.now())

        pos = geocentric.position.km  # (x, y, z) in km
        vel = geocentric.velocity.km_per_s  # (vx, vy, vz) in km/s

        x_positions.append(pos[0])
        y_positions.append(pos[1])
        z_positions.append(pos[2])
        vx.append(vel[0])
        vy.append(vel[1])
        vz.append(vel[2])
        labels.append(name)

        # Collision Detection
        distance = np.linalg.norm(np.array(pos) - np.array(test_pos))
        if distance < collision_threshold:
            collision_alerts.append(f"🚨 Alert! {name} is too close to {selected_sat[0]} (Distance: {distance:.2f} km)")

    except Exception as e:
        print(f"⚠️ Error processing {name}: {e}")
        continue

print("✅ Position and velocity calculations complete!")

# Step 5: Plot the Data in 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot Earth as a sphere
earth_radius = 6371  # Radius of Earth in km
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = earth_radius * np.outer(np.cos(u), np.sin(v))
y = earth_radius * np.outer(np.sin(u), np.sin(v))
z = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='blue', alpha=0.3)

# Plot debris positions in 3D
ax.scatter(x_positions, y_positions, z_positions, color="red", label="Space Debris", s=10)

# Plot velocity vectors (scaled for visibility)
scale_factor = 50  # Adjust this to make vectors larger/smaller
for i in range(len(x_positions)):
    ax.quiver(x_positions[i], y_positions[i], z_positions[i], vx[i] * scale_factor, vy[i] * scale_factor, vz[i] * scale_factor, color="green", length=50)

# Plot Selected Satellite
ax.scatter(test_pos[0], test_pos[1], test_pos[2], color="yellow", marker="*", s=200, label=selected_sat[0])

# Formatting the plot
ax.set_xlabel("X Position (km)")
ax.set_ylabel("Y Position (km)")
ax.set_zlabel("Z Position (km)")
ax.set_title("3D Space Debris Visualization with Collision Alerts")
ax.legend()

plt.show()

# Step 6: Send Email Alert (If Collisions Detected)
def send_email_alert(alerts):
    sender_email = "anshirock****@gmail.com"  # Replace with your email
    sender_password = "****"  # Use app password if using Gmail
    receiver_email = "anshiag*****@gmail"  # Replace with recipient

    subject = "🚨 Space Debris Collision Alert!"
    body = "\n".join(alerts)

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# Trigger Email if Collision Detected
if collision_alerts:
    send_email_alert(collision_alerts)
else:
    print("✅ No collisions detected. No email sent.")

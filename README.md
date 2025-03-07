# Space-Debris-Monitor
The Space Debris Monitoring System is a cutting-edge tool designed to help space organizations track and prevent potential satellite-debris collisions. By fetching real-time data from the Space-Track API, the system monitors satellite trajectories and space debris in Earth's orbit. If a satellite is on a collision course with debris, the system sends an immediate alert via email, providing real-time notifications for swift action. Additionally, the system offers a dynamic 3D visualization of satellites and debris, helping organizations better understand and visualize the situation.

### Key Features:
- **Real-Time Data Fetching:** Fetches live data from the Space-Track API to track satellites and space debris in Earth's orbit.
- **Collision Alerts:** Sends automatic email alerts if a satellite is at risk of colliding with space debris.
- **3D Visualization:** Provides an interactive 3D graph to visualize the positions of satellites and debris, helping to improve situational awareness.
- **Safety for Space Missions:** Ideal for space organizations, ensuring the safety of satellite missions by preventing debris collisions.
- **Customizable Alerts:** Alerts can be customized for different satellite orbits, debris sizes, and collision thresholds.

### Technologies Used:
- **Space-Track API:** Fetches real-time space debris and satellite data.
- **Backend:** Python 
- **Email Notifications:** SMTP 
- **3D Visualization:** Matplotlib
  
### How It Works:
1. **Real-Time Data Fetching:**
   The system pulls real-time data on satellites and space debris from the Space-Track API. The API provides critical information such as object trajectories, speed, and size, which are essential for predicting potential collisions.

2. **Collision Prediction:**
   By analyzing the position and trajectory of satellites and debris, the system predicts possible collisions based on a predefined threshold. When a collision is detected or is likely to happen, an alert is triggered.

3. **Email Alerts:**
   When a collision risk is identified, the system sends an automated email notification to the configured recipients. This helps space organizations take immediate action to avoid potential damage or destruction of satellites.

4. **3D Visualization:**
   The system generates a 3D interactive graph that plots the positions of satellites and debris in real-time. This visualization helps space organizations monitor the current situation and assess the risk of collision more effectively.

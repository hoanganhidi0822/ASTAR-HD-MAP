import glob
import math
import os

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Bán kính Trái Đất (m)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # Khoảng cách tính bằng mét

def project_point_on_line(p, a, b):
    """ Chiếu điểm P lên đoạn thẳng AB """
    px, py = p
    ax, ay = a
    bx, by = b

    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    ab_length_squared = abx**2 + aby**2

    # Hệ số t cho vị trí chiếu
    t = (apx * abx + apy * aby) / ab_length_squared
    t = max(0, min(1, t))  # Giữ t trong [0,1] để nằm trên đoạn AB

    # Tọa độ chiếu vuông góc
    projected_x = ax + t * abx
    projected_y = ay + t * aby

    return projected_x, projected_y

def find_nearest_waypoints(input_lat, input_lon, base_folder="D:/Documents/Researches/2024_Project/Astar/MAP/"):
    txt_files = glob.glob(f"{base_folder}/THUAN/*.txt") + glob.glob(f"{base_folder}/NGHICH/*.txt")
    
    nearest_file = None
    nearest_waypoint_1 = None
    nearest_waypoint_2 = None
    min_distance_1 = float("inf")
    min_distance_2 = float("inf")
    
    for file in txt_files:
        with open(file, "r") as f:
            waypoints = []
            for line in f:
                line = line.strip()
                if not line:  # Bỏ qua dòng trống
                    continue
                try:
                    lat, lon = map(float, line.split(","))
                    waypoints.append((lat, lon))
                except ValueError:
                    print(f"⚠️ Bỏ qua dòng không hợp lệ trong {file}: {line}")
        
        # Tìm 2 waypoint gần nhất
        for i in range(len(waypoints) - 1):
            lat1, lon1 = waypoints[i]
            lat2, lon2 = waypoints[i + 1]

            d1 = haversine(input_lat, input_lon, lat1, lon1)
            d2 = haversine(input_lat, input_lon, lat2, lon2)

            if d1 < min_distance_1:
                min_distance_2 = min_distance_1
                nearest_waypoint_2 = nearest_waypoint_1
                
                min_distance_1 = d1
                nearest_waypoint_1 = (lat1, lon1)
                nearest_file = os.path.basename(file)
            
            if d2 < min_distance_1:
                min_distance_2 = min_distance_1
                nearest_waypoint_2 = nearest_waypoint_1
                
                min_distance_1 = d2
                nearest_waypoint_1 = (lat2, lon2)
                nearest_file = os.path.basename(file)

    if nearest_waypoint_1 and nearest_waypoint_2:
        # Chiếu tọa độ hiện tại lên đoạn thẳng nối giữa 2 waypoint gần nhất
        projected_point = project_point_on_line((input_lat, input_lon), nearest_waypoint_1, nearest_waypoint_2)

        # Tính khoảng cách từ điểm chiếu đến tọa độ hiện tại
        projected_distance = haversine(input_lat, input_lon, projected_point[0], projected_point[1])

        # Chỉ trả về nếu khoảng cách < 1.5m
        if projected_distance < 1.5:
            return nearest_file, nearest_waypoint_1, nearest_waypoint_2, projected_point, projected_distance
        else:
            return None, None, None, None, None

    return None, None, None, None, None  # Không tìm thấy waypoint phù hợp

# Nhập tọa độ cần kiểm tra
input_lat, input_lon = 10.8530754633,106.7714831150

# Gọi hàm tìm waypoint gần nhất
file_name, waypoint1, waypoint2, projected_point, projected_distance = find_nearest_waypoints(input_lat, input_lon)

if file_name and waypoint1 and waypoint2:
    print(f"2 Waypoints gần nhất: {waypoint1}, {waypoint2} trong file: {file_name}")
    print(f"Tọa độ chiếu vuông góc: {projected_point}")
    print(f"Khoảng cách từ tọa độ hiện tại đến điểm chiếu: {projected_distance:.3f} m")
else:
    print("Không tìm thấy waypoint phù hợp (khoảng cách chiếu vuông góc > 1.5m).")

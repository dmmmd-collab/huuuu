import requests
import json
import time
import os
import random
from urllib.parse import urlparse, parse_qs

# Bản đồ (mapping) để chuyển đổi room_id thành tên phòng
room_names_map = {
    "1": "Nhà Kho",
    "2": "Phòng họp",
    "3": "Phòng giám đốc",
    "4": "Phòng trò chuyện",
    "5": "Phòng giám sát",
    "6": "Văn phòng",
    "7": "Phòng tài vụ",
    "8": "Phòng nhân sự",
}

# --- CÁC HÀM XỬ LÝ DỮ LIỆU ---
def fetch_data(url, headers):
    """
    Lấy dữ liệu từ một URL API và xử lý lỗi.
    """
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and data.get('code') == 0:
                return data['data']
            else:
                print(f"Lỗi API: Mã lỗi không phải 0. Phản hồi: {data}")
                return None
        else:
            print(f"Lỗi kết nối API: Mã lỗi HTTP {response.status_code}. Phản hồi: {response.text}")
            return None
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Lỗi trong quá trình kết nối hoặc phân tích dữ liệu: {e}")
        return None

def analyze_data(headers, asset_mode):
    """
    Phân tích dữ liệu từ API và tính toán tỉ lệ an toàn.
    """
    url_recent_10 = f"https://api.escapemaster.net/escape_game/recent_10_issues?asset={asset_mode}"
    url_recent_100 = f"https://api.escapemaster.net/escape_game/recent_100_issues?asset={asset_mode}"
    
    data_10 = fetch_data(url_recent_10, headers)
    data_100 = fetch_data(url_recent_100, headers)

    if data_10 is None or data_100 is None or not data_10:
        return None, [], "Chưa có thông tin", {}, {}

    current_issue_data = data_10[0]
    current_issue_id = current_issue_data.get('issue_id')
    
    killed_room_id = str(current_issue_data.get('killed_room_id'))
    current_killed_room_name = room_names_map.get(killed_room_id, "Chưa có thông tin")
    
    # Tính toán tỉ lệ từ 10 ván gần nhất
    killed_counts_10 = {str(i): 0 for i in range(1, 9)}
    for item in data_10:
        if isinstance(item, dict) and item.get('killed_room_id') is not None:
            killed_room_id_str = str(item['killed_room_id'])
            # Đảm bảo room_id nằm trong danh sách hợp lệ
            if killed_room_id_str in killed_counts_10:
                killed_counts_10[killed_room_id_str] += 1
    survival_rates_10 = {room_names_map.get(room_id): (100 - (count / 10) * 100) for room_id, count in killed_counts_10.items()}
    
    # Tính toán tỉ lệ từ 100 ván gần nhất
    survival_rates_100 = {}
    room_killed_stats_100 = data_100.get('room_id_2_killed_times', {})
    for room_id in room_names_map.keys():
        room_name = room_names_map.get(room_id)
        count = room_killed_stats_100.get(room_id, 0)
        killed_rate = (count / 100) * 100
        survival_rates_100[room_name] = 100 - killed_rate
    
    # Tính tỉ lệ an toàn cuối cùng bằng cách kết hợp tỉ lệ 10 ván và 100 ván
    final_survival_rates = {}
    for room_id in room_names_map.keys():
        room_name = room_names_map.get(room_id)
        rate_10 = survival_rates_10.get(room_name, 100)
        rate_100 = survival_rates_100.get(room_name, 100)
        
        # Công thức tỉ lệ kết hợp có trọng số 70/30
        weighted_rate = (rate_10 * 0.7) + (rate_100 * 0.3)
        final_survival_rates[room_name] = weighted_rate

    # Lọc ra các phòng có tỉ lệ an toàn chấp nhận được
    filtered_rooms = {room: rate for room, rate in final_survival_rates.items() if rate > 93.5}
    # Sắp xếp các phòng đã lọc theo thứ tự tỉ lệ an toàn giảm dần
    sorted_filtered_rates = sorted(filtered_rooms.items(), key=lambda item: item[1], reverse=True)
            
    return current_issue_id, sorted_filtered_rates, current_killed_room_name, survival_rates_10, survival_rates_100

def clear_screen():
    """Xóa màn hình console."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- VÒNG LẶP CHÍNH VÀ HIỂN THỊ ---
if __name__ == "__main__":
    user_id = "4456176"
    user_secret_key = "fb3e0927d8fa74dbc14378f14bc376dee8d47a9ee17089247d2b88112104fdf7"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "User-Id": user_id,
        "User-Secret-Key": user_secret_key
    }

    while True:
        clear_screen()
        print("="*50)
        print("         CHỌN CHẾ ĐỘ CHƠI")
        print("="*50)
        print("1. WORLD (Đồng xu vàng)")
        print("2. USDT (Đồng xu bạc)")
        print("3. BUILD (Đồng xu kim cương)")
        print("4. Thoát")
        print("="*50)
        
        choice = input("Vui lòng nhập lựa chọn của bạn (1-4): ")
        if choice == '1':
            asset_mode = "WORLD"
            break
        elif choice == '2':
            asset_mode = "USDT"
            break
        elif choice == '3':
            asset_mode = "BUILD"
            break
        elif choice == '4':
            print("Đã thoát chương trình.")
            exit()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            time.sleep(2)
    
    pending_prediction_issue_id = None
    pending_prediction_room_name = None
    
    total_games_played = 0
    total_wins = 0
    current_win_streak = 0
    
    while True:
        current_issue_id, sorted_filtered_rates, current_killed_room_name, survival_rates_10, survival_rates_100 = analyze_data(headers, asset_mode)

        if current_issue_id is None:
            clear_screen()
            print("Không thể lấy dữ liệu từ API. Đang thử lại...")
            time.sleep(5)
            continue
        
        if pending_prediction_issue_id is not None and str(pending_prediction_issue_id) == str(current_issue_id):
            clear_screen()
            print("="*50)
            print(f"            KẾT QUẢ KÌ {pending_prediction_issue_id} [{asset_mode}]")
            print("="*50)
            
            if pending_prediction_room_name:
                print(f"AI đã chọn phòng: **{pending_prediction_room_name}**")
                print(f"Sát thủ đã chọn phòng: **{current_killed_room_name}**\n")
                
                total_games_played += 1
                
                if current_killed_room_name and current_killed_room_name != pending_prediction_room_name:
                    print("🎉 Chúc mừng bạn đã thắng!")
                    total_wins += 1
                    current_win_streak += 1
                else:
                    print("😅 Rất tiếc, bạn đã thua.")
                    current_win_streak = 0
            else:
                print("AI đã không chọn phòng trong kì trước, không có kết quả để tính.")
            
            pending_prediction_issue_id = None
            pending_prediction_room_name = None
            
            time.sleep(5) 

        clear_screen()
        print("="*50)
        prediction_issue_id = str(int(current_issue_id) + 1)
        print(f"            DỰ ĐOÁN TỈ LỆ THẮNG | KÌ {prediction_issue_id} [{asset_mode}]")
        print("="*50)

        win_rate = (total_wins / total_games_played) * 100 if total_games_played > 0 else 0
        print(f"--- THỐNG KÊ BOT ---")
        print(f"Tổng số ván chơi: {total_games_played}")
        print(f"Tổng số ván thắng: {total_wins}")
        print(f"Chuỗi thắng liên tiếp: {current_win_streak}")
        print(f"Tỉ lệ thắng: {win_rate:.2f}%\n")
        
        # --- LOGIC DỰ ĐOÁN MỚI ĐÃ ĐƯỢC TỐI ƯU ---
        best_room_name_for_next = None
        best_room_rate = 0.0

        if sorted_filtered_rates:
            # Lấy tỉ lệ cao nhất từ danh sách đã sắp xếp
            highest_rate = sorted_filtered_rates[0][1]
            
            # Tìm tất cả các phòng có tỉ lệ cao nhất đó (trường hợp hòa)
            tied_rooms = [room_tuple[0] for room_tuple in sorted_filtered_rates if room_tuple[1] == highest_rate]
            
            if len(tied_rooms) > 1:
                # Nếu có nhiều phòng hòa nhau, áp dụng tiêu chí phụ: 
                # Chọn phòng có tỉ lệ sống sót cao nhất trong 10 ván gần nhất
                best_room_for_tie_breaker = None
                best_rate_10 = -1.0
                for room_name in tied_rooms:
                    rate_10 = survival_rates_10.get(room_name, 0)
                    if rate_10 > best_rate_10:
                        best_rate_10 = rate_10
                        best_room_for_tie_breaker = room_name
                best_room_name_for_next = best_room_for_tie_breaker
            else:
                # Nếu chỉ có một phòng tốt nhất, chọn phòng đó
                best_room_name_for_next = tied_rooms[0]

            best_room_rate = highest_rate

        if best_room_name_for_next:
            print(f"🥇 AI chọn phòng: **{best_room_name_for_next}** - Tỉ lệ sống sót: **{best_room_rate:.2f}%**\n")
        else:
            print(f"❌ AI không chọn phòng trong kì này.\n")
        
        print(f"🔪 Sát thủ đã chọn phòng: **{current_killed_room_name}**\n")
        
        print("--- TOP phòng an toàn nhất (< 93.5%) ---")
        if sorted_filtered_rates:
            for i, (room_name, rate) in enumerate(sorted_filtered_rates, 1):
                rate_10 = survival_rates_10.get(room_name, 100)
                rate_100 = survival_rates_100.get(room_name, 100)
                print(f"[{i}] {room_name}: {rate:.2f}% (Từ 10 ván: {rate_10:.2f}%, Từ 100 ván: {rate_100:.2f}%)")
        else:
            print("Chưa có đủ phòng để xếp hạng.")

        print("="*50 + "\n")
        
        pending_prediction_issue_id = prediction_issue_id
        pending_prediction_room_name = best_room_name_for_next
        
        countdown_up = 1
        while True:
            time.sleep(1)
            print(f"Đang chờ dữ liệu kì mới từ API... {countdown_up} giây", end='\r')
            countdown_up += 1
            new_issue_id, _, _, _, _ = analyze_data(headers, asset_mode)
            if new_issue_id and new_issue_id != current_issue_id:
                print("\n🎉 Đã có dữ liệu kì mới! Đang xử lý...")
                break

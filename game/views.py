from django.shortcuts import render, redirect

# 初始球隊資訊，包括名稱、球員、原始球員、分數等
teams = {
    'team1': {'name': '', 'players': ['', ''], 'original_players': ['', ''], 'score': 0, 'name_locked': False, 'players_locked': False},
    'team2': {'name': '', 'players': ['', ''], 'original_players': ['', ''], 'score': 0, 'name_locked': False, 'players_locked': False},
}

# 根據得分交換球員順序的函式
def swap_players_based_on_score():
    # 球隊1
    # 如果球隊1的得分為奇數，交換球員順序
    if teams['team1']['score'] % 2 == 1:  
        teams['team1']['players'] = [teams['team1']['original_players'][1], teams['team1']['original_players'][0]]
    # 如果球隊1的得分為偶數，使用原始順序
    else:  
        teams['team1']['players'] = [teams['team1']['original_players'][0], teams['team1']['original_players'][1]]

    # 球隊2
    # 如果球隊2的得分為奇數，交換球員順序
    if teams['team2']['score'] % 2 == 1:  
        teams['team2']['players'] = [teams['team2']['original_players'][1], teams['team2']['original_players'][0]]
    # 如果球隊2的得分為偶數，使用原始順序
    else:  
        teams['team2']['players'] = [teams['team2']['original_players'][0], teams['team2']['original_players'][1]]
def swap_teams():
    # 交換球隊名稱
    temp_name = teams['team1']['name']
    teams['team1']['name'] = teams['team2']['name']
    teams['team2']['name'] = temp_name

    # 交換球隊球員
    temp_original_players1 = teams['team1']['original_players']
    teams['team1']['original_players'] = teams['team2']['original_players']
    teams['team2']['original_players'] = temp_original_players1

    # 交換球隊分數
    temp_score = teams['team1']['score']
    teams['team1']['score'] = teams['team2']['score']
    teams['team2']['score'] = temp_score

    # 交換後重設球員列表
    teams['team1']['players'] = teams['team1']['original_players'][:]
    teams['team2']['players'] = teams['team2']['original_players'][:]
def reset_teams():
    teams['team1']['name'] = ''
    teams['team1']['players'] = ['', '']
    teams['team1']['original_players'] = ['', '']
    teams['team1']['name_locked'] = False
    teams['team1']['players_locked'] = False
    teams['team1']['score'] = 0  # 將分數歸零

    teams['team2']['name'] = ''
    teams['team2']['players'] = ['', '']
    teams['team2']['original_players'] = ['', '']
    teams['team2']['name_locked'] = False
    teams['team2']['players_locked'] = False
    teams['team2']['score'] = 0  # 將分數歸零
def process_form_submission(request):
    if not teams['team1']['name_locked'] and not teams['team1']['players_locked']:
        team1_name = request.POST.get('team1_name')
        player1 = request.POST.get('player1')
        player2 = request.POST.get('player2')
        if team1_name and player1 and player2:
            teams['team1']['name'] = team1_name
            teams['team1']['players'] = [player1, player2]
            teams['team1']['original_players'] = [player1, player2]
            teams['team1']['name_locked'] = True
            teams['team1']['players_locked'] = True

    if not teams['team2']['name_locked'] and not teams['team2']['players_locked']:
        team2_name = request.POST.get('team2_name')
        player3 = request.POST.get('player3')
        player4 = request.POST.get('player4')
        if team2_name and player3 and player4:
            teams['team2']['name'] = team2_name
            teams['team2']['players'] = [player3, player4]
            teams['team2']['original_players'] = [player3, player4]
            teams['team2']['name_locked'] = True
            teams['team2']['players_locked'] = True

    teams['team1']['score'] = int(request.POST.get('team1_score', 0))
    teams['team2']['score'] = int(request.POST.get('team2_score', 0))

    swap_players_based_on_score()  # 根據得分交換球員順序
# 首頁視圖
def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'swap_teams':
            swap_teams()
            
        elif action == 'reset_names':
            reset_teams()
            
        else:
            process_form_submission(request)

    return render(request, 'game/index.html', {'teams': teams})

# 重置分數的視圖
def reset_scores(request):
    teams['team1']['score'] = 0
    teams['team2']['score'] = 0
    return redirect('index')

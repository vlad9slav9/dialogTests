
def test_correct_login(login_page):
    event_page = login_page.do_login("devyt9", "12332145")
    event_page.assert_user_profile_button_visible()
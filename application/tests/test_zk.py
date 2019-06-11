import time
def test_zk_app_get_children(get_zk_children):
            
    assert get_zk_children == 11

def test_zk_app_lost_children(get_zk_children):
    
    assert get_zk_children == 8

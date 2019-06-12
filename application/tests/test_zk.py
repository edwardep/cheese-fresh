import time
import pytest
def test_zk_app_get_children(mock_zk_storage, mock_zk_app, utility):
    utility.mock_zk_create_storage_nodes(mock_zk_storage, 10)

    assert len(utility.mock_zk_get_children(mock_zk_app)) == 10


def test_zk_app_lost_children(mock_zk_storage, mock_zk_app, utility):
    utility.mock_zk_create_storage_nodes(mock_zk_storage, 10)
    # delete some nodes
    utility.mock_zk_delete_storage_nodes(mock_zk_storage, 3)

    assert len(utility.mock_zk_get_children(mock_zk_app)) == 7

@pytest.mark.xfail
def test_zk_app_storage_down(mock_zk_storage, mock_zk_app, utility):
    '''
        Create 4 storage nodes -> delete 3 of them -> assert len(children) == 0 (1 node ALIVE)
        Create 1 storage node  -> assert len(children) == 2
    '''
    utility.mock_zk_create_storage_nodes(mock_zk_storage, 4)
    # delete some nodes
    utility.mock_zk_delete_storage_nodes(mock_zk_storage, 3)

    # if len < 2 return 0
    assert len(utility.mock_zk_get_children(mock_zk_app)) == 0

    if not mock_zk_storage.exists('/storage/child'):
        mock_zk_storage.create('/storage/child', b"1000")

    assert len(utility.mock_zk_get_children(mock_zk_app)) == 2
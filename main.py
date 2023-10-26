from sql_table import DZEN_db_create, delete_repeat
from main_page_users_parcing import main_page_users_parcing

def main():
    DZEN_db_create()
    main_page_users_parcing()
    delete_repeat()
    
if __name__ == '__main__':
    main()
    
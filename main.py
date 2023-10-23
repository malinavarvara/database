from sql_table import DZEN_db_create
from main_page_users_parcing import main_page_users_parcing

def main():
    DZEN_db_create()
    main_page_users_parcing()
    
if __name__ == '__main__':
    main()
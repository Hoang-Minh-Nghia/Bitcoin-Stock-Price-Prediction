import requests
from bs4 import BeautifulSoup
import csv
import os
import subprocess
import sys

if len(sys.argv) > 1:
    input_name = sys.argv[1]
else:
    print("Failed to run script.")

def craw_data(name):

    link = 'https://simplize.vn/co-phieu/'
    url = link + name.strip()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pe_value = soup.find_all('span', class_='css-1y6ypva')
        data = [item.text.strip() for item in pe_value]
    
#        print("Vốn hóa", data[0].replace(',', '').replace('T', '000000000'))
#        print("P/E", data[1])
#        print("EPS", data[2].replace(',', ''))
#        print("Khối lượng giao dịch", data[3].replace(',', ''))
#        print("P/B", data[4])
#        print("Giá trị sổ sách", data[5].replace(',', ''))
#        print("Số lượng cổ phiếu lưu hành", data[6].replace(',', ''))
#        print("EV/EBITDA", data[7])        
        capitalization = data[0].replace(',', '').replace('T', '000000000')
        p_e = data[1]
        eps = data[2].replace(',', '')
        volume = data[3].replace(',', '')
        p_b = data[4]
        book_value = data[5].replace(',', '')
        n_o_shares = data[6].replace(',', '')
        EV_EBITDA = data[7]

        price_value = soup.find('p', class_='css-19r22fg')
#        print("Giá",price_value.text.strip().replace(',', ''))
        # Mở file CSV để ghi
        price_stock = price_value.text.strip().replace(',', '')

        with open('result.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, capitalization, p_e, eps, volume, p_b, book_value, n_o_shares, EV_EBITDA, price_stock])
    else:
        print('Lỗi khi tải trang:',name , response.status_code)


def search_stock(name):
    
    dir_field = "group_field"
    for filename in os.listdir(dir_field):

        file_path = os.path.join(dir_field, filename)

        if os.path.isfile(file_path):
            try:
                # Mở file và đọc nội dung
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Đọc từng dòng trong file
                    for line_number, line in enumerate(file, start=1):
                        if name in line:
                            print(f"'{name}' in '{filename}'")
                            return filename
            except Exception as e:
                print(f"Can't to read file'{file_path}': {e}")

def build_csv(name_stock):
    # Các giá trị riêng lẻ
    name = "name"
    capitalization = "capitalization"
    p_e = "P/E"
    eps = "EPS"
    volume = "volume"
    p_b = "P/B"
    book_value = "book_value"
    n_o_shares = "n_o_shares"
    EV_EBITDA = "EV/EBITDA"
    price_stock = "price"

    # Mở file CSV để ghi
    with open('result.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["name","capitalization", "p_e", "eps", "volume", "p_b", "book_value", "n_o_shares", "n_o_shares", "price"])


    list_company = search_stock(name_stock)
    full_dir= "group_field/" + list_company

    with open(full_dir, 'r') as file:
        content = file.readlines()

    print("Generating csv file...")
    for line in content:
        craw_data(line.strip())
    print("Completed to genera csv file")

def main():

    build_csv(input_name)
    
    print("Value prediction in progress")
    result = subprocess.run(['python3', 'predict_price.py', input_name], capture_output=True, text=True)
    print(result.stdout)
    print("Mã lỗi:", result.returncode)
if __name__ == "__main__":
    main()

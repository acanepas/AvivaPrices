from multiprocessing import process
from pandas.core.construction import is_empty_data
import requests
import pandas as pd
from lxml import html
from urllib.parse import urlencode
import multiprocessing


df = pd.read_csv('fund_names.csv')
df.fund_name = df.fund_name.str.replace("Aviva Pensions","")

#df_len = len(df.fund_name)


#fundname = df.fund_name[2]

#BaseUrl = f"https://markets.ft.com/data/search?query={fundname}"
#print(urlencode(dict(query=fundname)))


def get_fund_code(fundName):
    query_url = urlencode(dict(query=fundName))
    BaseUrl = f"https://markets.ft.com/data/search?{query_url}"
    #BaseUrl = f"https://markets.ft.com/data/search?query={fundName}"
    
    xpath_noresult = "//div[@data-module-name='ResultsApp']/p/text()"
    page = requests.get(BaseUrl, timeout=10)
    
    htmlDoc = html.fromstring(page.content)
    
    no_result = htmlDoc.xpath(xpath_noresult)
    
    if is_empty_data(no_result):
       html_table =  pd.read_html(BaseUrl)[0]
       return html_table.Symbol
    else:
        return "No Result"
    


def get_all_codes(df):
    

    
    fund_list = pd.DataFrame([])

    for index, fundNm in df.iterrows():
        temp_df = pd.DataFrame.from_dict({'fundName':fundNm,'Symbol':get_fund_code(fundNm)})
        fund_list = fund_list.append(temp_df, ignore_index=True)
        print(index)
    
    return fund_list

def test_proc(i):
    fundNm = df.fund_name[i]
    return  (fundNm,
             get_fund_code(fundNm)[0]
             )

   




if __name__ == '__main__':
    
    
    df = pd.read_csv('fund_names.csv')
    df.fund_name = df.fund_name.str.replace("Aviva Pensions","")
    l = len(df.fund_name)
    # processes = []
    
    # for i in range(1):
    #         process = multiprocessing.Process(target=test_proc, args = (df.fund_name[i],))
    #         print(i)
    #         processes.append(process)
    #         process.start()
    #         process.join()
        

    
    
      #  for index, fundNm in df.iterrows():
      
    


    # #print(get_all_codes(df.fund_name[0:2]))
    pool = multiprocessing.Pool()
    r = pool.map(test_proc,range(230))
    print(r)
    
    final_list = pd.DataFrame(r)
    print(final_list)

    final_list.to_csv('funds_symbol.csv' , index=False)
    

    
    # processes = []

    # for _ in range(4):
    #     p = multiprocessing.Process(target=get_number, args = [1,2,3,4])
    #     p.start()
    #     processes.append(p)
        
    # for process in processes:
    #     process.join()
        


        









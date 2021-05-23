# %%
import pandas as pd
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from pandas import DataFrame

def get_kcal(height,sex):

    if sex == 'man':
        m_k = height**2 * 22 * 35
        m_k = round(m_k,-2)
        m_k = int(m_k)
        return m_k
    elif sex == 'woman':
        w_k = height**2 * 21 * 35
        w_k = round(w_k,-2)
        w_k = int(w_k)
        return w_k
    
def kcal_goonn(kcal, kcal_df):
    return kcal_df[kcal_df['에너지 (kcal)'] == my_kcal]

def add_today(wantlist, returnlist,n):
    a = list(zip(wantlist[0][0],wantlist[1][0],wantlist[2][0]))
    b = list()
    returnlist = list()
    
    # 오늘 먹은 식품군 or 영양소 별로 합친 list 만들기
    for q,w,e in a:
        b.append(q+w+e)
        
    # 소수점 자리 1자리 고정   
    for i in range(n):
        returnlist.append(round(b[i],1))
    
    return returnlist

def substract_today(main,be_substracted,returnlist,n):
    aa = list(zip(main,be_substracted))
    bb = list()
    returnlist = list()
    
    for a,b in aa:
        bb.append(1-b)
        
    for i in range(n):
        returnlist.append(round(bb[i],1))
        
    return returnlist

def elbow(x):
    sse = []
    for i in range(1,11):
        km = KMeans(n_clusters=i, init='k-means++', random_state = 0, algorithm = 'auto')
        km.fit(x)
        sse.append(km.inertia_)
        
    plt.plot(range(1,11),sse,marker='o')
    plt.xlabel('num of clusters')
    plt.ylabel('SSE')
    plt.show()
    
def k_means(data,k) :
    data_copy = data.copy()
    food = data_copy['음식명']
    data_copy = data_copy.drop(['음식명'],axis=1)
    col_n = list(data_copy.columns)
    
    for co in col_n:
        data_copy[co] = (data_copy[co] - data_copy[co].min())/(data_copy[co].max()-data_copy[co].min())
    
    feature = data_copy[col_n]
    
    model = KMeans(n_clusters=k,algorithm='auto',random_state=0)
    model.fit(feature)
    predict = pd.DataFrame(model.predict(feature))
    predict.columns=['predict']
    
    output = pd.concat([food,feature,predict],axis=1)
    
    return output,model

def watch_cluster(df,k,cluster_number) :
    output,model = k_means(df,k)
    df_cluster = output[output['predict'] == cluster_number]
    
    return df_cluster

def get_same_cluster(element,lack_element,k):
    output,model = k_means(element,k)
    lack_element_d = [lack_element]
    s=model.predict(lack_element_d)
    s = list(s)
    s = s[0]
    output_b = watch_cluster(element,k,s)
    return output_b

def recommend_foodd(goon,lack_goon,k_g,nutrient,lack_nutrient,k_n):
    lack_goon_max_value = max(lack_goon)
    lack_goon_max_index = lack_goon.index(lack_goon_max_value)
    same_goon = get_same_cluster(goon,lack_goon,k_g)
    same_nutrient = get_same_cluster(nutrient,lack_nutrient,k_n)
    g=same_goon['음식명'].values.tolist()
    n=same_nutrient['음식명'].values.tolist()
    tmp = list(set(g).intersection(n))
    if len(tmp) == 0:
        max_lack_goon = same_goon.columns[lack_goon_max_index+1]
        output = []
        output.append(same_goon[same_goon[max_lack_goon] == same_goon[max_lack_goon].max()]['음식명'])
        lack_nutrient_max_value = max(lack_nutrient)
        lack_nutrient_max_index = lack_nutrient.index(lack_nutrient_max_value)
        max_lack_nutrient = same_nutrient.columns[lack_nutrient_max_index+1]
        output.append(same_nutrient[same_nutrient[max_lack_nutrient] == same_nutrient[max_lack_nutrient].max()]['음식명'])
        return output
    return tmp

def back_scailing(scailed_list, rcmd_list,n):
    a = list(zip(scailed_list,rcmd_list))
    b = list()
    returnlist = []
    for q , w in a:
        b.append(q*w)
    for i in range(n):
        returnlist.append(round(b[i],1))
    return returnlist

def make_plot(back_scailed_list, std_list,col,n):
    x = np.arange(n)
    plt.rcParams['font.family'] = 'STIXSizeOneSym'
    plt.bar(x, std_list, color = "red")
    plt.bar(x, back_scailed_list, color = "springgreen")
    plt.xticks(x, col)
    plt.title("기준 대비 섭취량")
    plt.show()

def deep_diet1(height,sex,weight,eaten):
    kcal_df = pd.read_csv("/Users/chanju/github/project/deepdiet/이찬주/gooon.csv",encoding='CP949')
    kcal_df = kcal_df.drop(['Unnamed: 5','Unnamed: 7'],axis=1)
    my_kcal = get_kcal(height,sex)
    kcal_goon = kcal_goonn(my_kcal, kcal_df)
    kcal_goon = kcal_goon[['곡류','채소류','과일류','고기.생선 달걀.콩류','우유 유제품류','유지 당류']]
    goon_list = kcal_goon.values.tolist()
    goon_list = [y for x in goon_list for y in x]
    std_nutrient = [my_kcal, 300, 51, (weight*0.91), 600]


    for i in range(5):
        std_nutrient[i] = float(std_nutrient[i])
    
    min_max_user =  goon_list + std_nutrient
    
    df = pd.read_csv("/Users/chanju/github/project/deepdiet/이찬주/database.csv")
    #df =df.drop(['Unnamed: 2','Unnamed: 4','Unnamed: 9','Unnamed: 11','Unnamed: 13','Unnamed: 15','Unnamed: 17','Unnamed: 19','Unnamed: 21','Unnamed: 23'],axis=1)
    df = df.rename({'영양소 함량':'곡류','Unnamed: 6':'재료량','Unnamed: 7':'과일','Unnamed: 8':'육류','Unnamed: 10':'우유','Unnamed: 12':'유지','영양소 함량.1':'에너지 (kcal)','Unnamed: 16':'탄수화물 (g)', 'Unnamed: 18':'지질 (g)','Unnamed: 20':'단백질 (g)','Unnamed: 22':'칼슘 (mg)'},axis=1)
    df= df.dropna()
    cols=['곡류','채소','과일','육류','우유','유지','칼로리','탄수화물','지질','단백질','칼슘']

    for idx,co in enumerate(cols):
        df[co] = ((df[co] - 0)/(min_max_user[idx]-0))
    
    col2 = ['음식명','곡류','채소','과일','육류','우유','유지']
    goon = df[col2]
    
    col4 = ['음식명','칼로리','탄수화물','지질','단백질','칼슘']
    nutrient = df[col4]
    
    col = ['곡류','고기.생선 달걀.콩류','채소류','과일류','우유 유제품류','유지 당류']
    recmd_goon = kcal_goon[col].values.tolist()
    
    col3 = ['곡류','채소','과일','육류','우유','유지']
    eaten_goon=[]
    # 오늘 먹은 식품군들을 한 개의 list로 만들기 
    for food in eaten:
        eaten_goon.append(goon[goon['음식명'] == food][col3].values.tolist())
    
    eaten_goon_add = []
    eaten_goon_add = add_today(eaten_goon,eaten_goon_add,6)
    
    lack_goon = []
    lack_goon = substract_today(recmd_goon[0],eaten_goon_add,lack_goon,6)
    
    col5 = ['칼로리','탄수화물','지질','단백질','칼슘']
    eaten_nutrient = []
    for food in eaten:
        eaten_nutrient.append(nutrient[nutrient['음식명']== food][col5].values.tolist())
    eaten_nutrient_add = []
    eaten_nutrient_add = add_today(eaten_nutrient,eaten_nutrient_add,5)
    lack_nutrient = []
    lack_nutrient = substract_today(std_nutrient,eaten_nutrient_add,lack_nutrient,5)
    
    same_goon = get_same_cluster(goon,lack_goon,5)
    same_nutrient = get_same_cluster(nutrient,lack_nutrient,4)
    goon_d = goon.drop(['음식명'],axis=1)
    nutrient_d = nutrient.drop(['음식명'],axis=1)
    
    recommend_food = recommend_foodd(goon,lack_goon,5,nutrient,lack_nutrient,4)
    
    back_scailded_goon = back_scailing(lack_goon, goon_list,6)
    plot_goon = make_plot(back_scailded_goon,goon_list,col3,6)
    back_scailed_nutrient = back_scailing(lack_nutrient,std_nutrient,5)
    plot_nutrient = make_plot(back_scailed_nutrient,std_nutrient,col5,5)
    return recommend_food , plot_goon , plot_nutrient

deep_diet1(1.8,'man',80,['팥빵','피자','유부초밥'])


# %%

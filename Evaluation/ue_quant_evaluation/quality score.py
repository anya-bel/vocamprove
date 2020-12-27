def human_evaluation(results):   
    n_tot=len(set(df['dimension']))
    D_sum = 0
    c=0
    for Dim in set(dimension):
        df_Dim = df.loc[df["dimension"]==Dim]
        factors = (set(df_Dim['factor']))
        for n in factors:
            Dim_j = 0
            factor_o = 0
            factor_u = 0
            df_f = df_Dim.loc[df_Dim['factor'] == n]
            for row in df_f.iterrows():
                r = dict(zip(header,list(row[1])))
                factor_o += (r['q_weight'])*(r['avg'])
                factor_u += r['q_weight']
            p = r['f_weight']
            factor_n = (factor_o/factor_u)
            Dim_j += p*factor_n
        D_sum += (1-(Dim_j/100))**2
    D = sqrt(D_sum)
    # The real system quality is then computed
    Q = (1-(D/sqrt(n_tot)))*100
    return(Q)

path = "/content/drive/MyDrive/Uni_Projects/Vocamprove/eva.csv"
df = pd.read_csv(path)
df = df.T
df = df.reset_index(drop=True)
df = df.drop(0)
df = df.astype(str).astype(int)

q_weight = [0.5,0.5, 0.2,0.2,0.2,0.2,0.2, 0.25,0.25,0.25,0.25, 1, 0.5,0.5, 1,1,1,1, 0.25,0.25,0.25,0.25, 1]
factor = [1,1,2,2,2,2,2,3,3,3,3,4,5,5,6,7,8,9,10,10,10,10,11]
f_weight = [1 for i in range(len(q_weight))]
dimension = [1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3]


df['avg']= df.mean(numeric_only=True, axis=1)*20
df['q_weight']=q_weight
df['factor']=factor
df['f_weight']=f_weight
df['dimension']=dimension

header = list(df)

if __name__ == "__main__":
	human_evaluation(df)

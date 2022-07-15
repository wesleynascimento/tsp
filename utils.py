def pegaMatriz():
    vet=[]
    mat=[]
    lin=[]
    num=""
    arq=open("cam.txt","r")
    for x in arq:
        lin=x.strip("\n")
        lin=x.split(" ")
        vet.append(lin)
    for i in vet:
        lin=[]
        for j in i:
            if j!=" " or j!="" or j!='"':
                num+=j
            if j=='"':
                num=""
            elif j!="":
                numInt=int(float(num))
                #print(num)
                lin.append(numInt)
                num=""
        mat.append(lin)
    return mat
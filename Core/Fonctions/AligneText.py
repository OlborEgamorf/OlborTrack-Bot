def aligne(s1, s2):
    n1, n2 = len(s1), len(s2)
    sc = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    for i in range(1,n1+1):
        sc[i][0] = -i
    for j in range(1,n2+1):
        sc[0][j] = -j
    for i in range(1,n1+1):
        for j in range(1,n2+1):
            if s1[i-1] == s2[j-1]:
                signe=1
            else:
                signe=-1
            sc[i][j]=max(-1+sc[i-1][j],-1+sc[i][j-1],signe+sc[i-1][j-1])
    return sc[n1][n2]
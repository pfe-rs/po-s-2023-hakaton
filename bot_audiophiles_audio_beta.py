from random import randrange
import time


def act(row: int, column: int, team: int, turn: int, mycash: int, opcash: int, map:list[list[tuple[int, int, int, int, int]]])->int:


    #map[x][y] (cpu, ram, stampa, pripadnost timu, broj virusa)
    cpu = 0
    ram = 1
    stampa = 2
    tim = 3
    virus = 4

    nas_cpu = map[row][column][cpu]
    nas_ram = map[row][column][ram]
    nas_stampa = map[row][column][stampa]
    nas_tim = map[row][column][tim]
    nas_virus = map[row][column][virus]
    

    # naivna strategija
    ## sure potezi:
    ### preuzmi neutralne koji nemaju antiviruse
    ### preuzmi neutralne koje moze u jednom potezu
    ### ako nema cpu, ne proizvodi viruse sigurno
    ### pre nego sto probas da preuzmes cvorove okolo, moras da imas viruse kod sebe(duhh)
    ### nekako smisliti no glupi potezi, tjst da ne pokusa 4 cvora da napadne jedan koji ce preuzeti sigurno
    #### napraviti mozda novu mapu koju updejtujemo mi tako da se akcije nasih cvorova ne bi sudarale
    ### ako je u blizini high value meta(valjda stampac samo) da je nekako okruzi i preuzme
    ### high cpu cvorovi bi trebali da proizvode i distributiraju sto vise svoje viruse okolo, cpu blizu vrednosti rama, onda to
    ### izbeci nekako waste virusa
    ### mozda best move strategija gde imamo listu najboljih poteza pa izbacujemo sta necemo a pomeramo okolo da skontamo sta je najbolje
    
    # obavezno proveriti za ivice terena da ne bi breakovao kod



    # funkcije za:
    # napad na polje 
    # pravljenje virusa
    # nadji optimalno polje
    # stampa


    ## IMPORTANT
    # if no virusi dont attack, make virusi, if no cpu, then print moneyy



    okolni_cvorovi = []
    okolni_tumacenje = []
    if row != 0:
            okolni_cvorovi.append(map[row-1][column])
            okolni_tumacenje.append(1)
    if row != len(map) - 1 :
            okolni_cvorovi.append(map[row+1][column])
            okolni_tumacenje.append(3)
    if column != 0:
            okolni_cvorovi.append(map[row][column-1])
            okolni_tumacenje.append(4)
    if column != len(map[0]) - 1 :
            okolni_cvorovi.append(map[row][column+1])
            okolni_tumacenje.append(2)

    nasi=0

    for i in range(0,len(okolni_cvorovi)):

        if okolni_cvorovi[i][tim] == nas_tim:
                nasi += 1
    


    
    
    if nas_stampa > 0 and nasi == len(okolni_cvorovi) : ##  ako moze da stampa, ima da stampa 
        # ako moze da stampa onda 
        #print("stampam")
        return 5
    
    if nas_virus == 0 and nas_cpu!= 0: ## ako nema virusa i moze da proizvodi onda proizvodi
        print("proizvodnja")
        return 0


    for i in range(0, len(okolni_cvorovi)):
        if okolni_cvorovi[i][stampa] > 0: # trazi stampace medju okolnim cvorovima
            if okolni_cvorovi[i][tim] == nas_tim: #stampac pripada nama
                #napad na drugo:
                ez = 16
                napadni = 0
                for j in range (0,len(okolni_cvorovi)): # 
                    if okolni_cvorovi[j][tim] != nas_tim:
                        if okolni_cvorovi[j][virus] <= ez:
                            ez = okolni_cvorovi[j][virus]
                            napadni = j
                if nasi == len(okolni_cvorovi)-1 and nas_cpu > 0 and nas_virus < nas_ram:
                        # ovde je dobro valjda 
                        return 0
                out = napad (napadni, okolni_tumacenje)

            if okolni_cvorovi[i][tim] != nas_tim: #stampac nam ne pripada
                # napad na stampac:
                
                out = napad (i, okolni_tumacenje) 
            
            return out

    ez = 16
    napadni = 0
    
    ima_neutralnih = False
    ## trazi najslabiju metu
    for i in range(0,len(okolni_cvorovi)):
        if okolni_cvorovi[i][tim] != nas_tim: # ne salji nasima 
            ima_neutralnih =True
            if okolni_cvorovi[i][virus] <= ez:
                ez = okolni_cvorovi[i][virus]
                napadni = i
                
    if nasi != len(okolni_cvorovi):
        ima_neutralnih = True
    
    
    if ima_neutralnih:
        # print("hej")
        return napad(napadni, okolni_tumacenje)



    if nasi == len(okolni_cvorovi) and nas_cpu > 0 and nas_virus < nas_ram:
            print("proizvodnja")
            return 0
    
    ez = 16
    for i in range(0,len(okolni_cvorovi)): ## 
        if okolni_cvorovi[i][virus] <= ez:

            ez = okolni_cvorovi[i][virus]
            napadni = i
    return napad(napadni, okolni_tumacenje)
    




def napad(koji_cvor: int, okolni_tumacenje: list):

    # print(okolni_cvorovi)
    # print(okolni_tumacenje)
    # print(koji_cvor)
    # okolni_cvorovi[koji_cvor]
    return okolni_tumacenje[koji_cvor]
    
   
#def stari_napad
    # napad(i) ## kada nemaju svi cvorovi onda ce se sjebati ovo
    # koji cvor je indeks iz liste okolni_cvorovi
    # if koji_cvor == 0: return koji_cvor + 1 # gore
    # if koji_cvor == 1: return koji_cvor + 1 # desno
    # if koji_cvor == 2: return koji_cvor + 1 # dole
    # if koji_cvor == 3: return koji_cvor + 1 # levo
    # :facepalm:
    #return koji_cvor + 1


    # except:
        
    #     roll = True
    #     while roll:    
    #         out = randrange(6)
    #         roll = False
    #         if out == 1 and row == 0: ## nemoj gore ako gore nema nicega
    #             roll = True
    #         if out == 2 and column == len(map[0])-1: ## nemoj udesno ako desno nema nicega
    #             roll = True
    #         if out == 3 and row == len(map)-1: ## nemoj dole ako dole nema nicega
    #             roll = True
    #         if out == 4 and column == 0: # nemoj ulevo ako nema levo nicega
    #             roll = True
    #         if out >= 1 and out <= 4 and map[row][column][4] == 0: ## ako random pokusa da napadne a nema viruse
    #             roll = True
    #         if out == 5 and map[row][column][2] == 0: # ako pokusa da stampa a nema mogucnosti stampanja
    #             roll = True
            
    #         if nas_virus == 0 and nas_cpu!= 0: ## ako nema virusa a moze da proizvodi onda proizvodi
    #             return 0
            
            
                      
        # return out



    


# 0-proizvodnja virusa
#1-pomeranje gore
#2-pomeranje desno 
#3-pomeranje dole
#4-pomeranje levo
#5-stampa


# pygame ekran tumacenje
# prva brojka je trenutna kolicina virusa, druga brojka je ram valjda, + treca brojka je cpu, zeleni 



    # roll = True
    # while roll:    
        # out = randrange(6)
        # roll = False
        # if out == 0
        # if out == 1 and row == 0:
        #     roll = True
        # if out == 2 and column == len(map[0])-1:
        #     roll = True
        # if out == 3 and row == len(map)-1:
        #     roll = True
        # if out == 4 and column == 0:
        #     roll = True
        # if out >= 1 and out <= 4 and map[row][column][4] == 0:
        #     roll = True
        # if out == 5 and map[row][column][2] == 0:
        #     roll = True
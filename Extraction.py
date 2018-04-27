


def check_if_outil(file,c):

    with open(file,mode="r") as outil:
        for x in outil:
            if x==c+'\n':
               return True
    return False




def exctraction(main_file,carac_file,outil_file,mot_recherche):
    first_previous_word,sec_previous_word,first_after_word,sec_after_word=0,0,0,0
    with open(main_file,mode='r') as mainf:
        for i in mainf:
            line= i.split(" ")
            #suppression des caractaires vide
            line=[x  for x in line if x and x not in (',')]
            for f in range(len(line)):
                if line[f].__contains__(mot_recherche):
                    #verifier si il existes au moins 2 mot avant
                    if f>1:
                        #verifier si les mot ne sont pas des mot outil
                        sec_previous_word=check_if_outil(outil_file,line[f-2])
                        first_previous_word=check_if_outil(outil_file,line[f-1])
                        if first_previous_word and sec_previous_word :
                            #le 1er mot d'avant et le second sont des mot outil
                            if f - 4 >= 0:
                                print(line[f - 4])
                            if f-3>=0:
                                print(line[f-3])

                        elif first_previous_word:
                            #seul le 1er mot d'avant est un mot outil
                            if f - 3 >= 0:
                                print(line[f - 3])
                            print(line[f-2])
                        elif sec_previous_word:
                            #seul le 2eme mot d'avant est un mot outil
                            if f-3>=0:
                                print(line[f-3])
                            print(line[f-1])

                        else:
                            #aucun des 2 mot n'est un mot outil
                            print(line[f-2],line[f-1])


                    elif f>0:
                        #il existe seulement un mot avant
                        print(line[f-1])

                    #verifier que il existe au moins 2 mot apres
                    if f<=len(line)-2:
                        first_after_word=check_if_outil(outil_file,line[f+1])
                        sec_after_word=check_if_outil(outil_file,line[f+2])
                        #verifier si les 2 mots apres sont des mots outil
                        if first_after_word and sec_after_word :
                            if f+4<len(line):
                                print(line[f+3])
                                print(line[f+4])
                            elif f+3<len(line):
                                print(line[f+3])
                        elif first_after_word:
                            if f+3<len(line[f+3]):
                                print(line[f+2])
                                print(line[f+3])
                            else:
                                print(line[f+2])
                        elif sec_after_word:
                            if f+3<len(line):
                                print(line[f+1])
                                print(line[f+3])
                            else:
                                print(line[f+1])
                        else:
                            print(line[f+1],line[f+2])


                    elif f<len(line)-1:
                        #il y'a un seul mot apres
                        print(line[f+1])





if __name__=="__main__":
    exctraction("/home/xpack/Desktop/ift3335/interest-original.txt","/home/xpack/Desktop/ift3335/carac.txt"
                        ,"/home/xpack/Desktop/ift3335/mot_outil.txt","interest")


import re
import os 

#fonction qui traite les caractaires speciaux dans les mots
def replace(text):
    if re.search("[!,.?;:/*]",text):
        #return re.sub("[!,.?;:/*]","X",text)
        return "X"
    if re.search("['{}[]()| ]",text):
        #return '\{}'.format(text)
        return"NULL"
    if re.search("[%]",text):
        return "PERCENT"
    if re.search("[====]",text):
        return "NULL"
    if re.search("[$]",text):
        return "NULL"


    return text


def check_if_outil(file,c):

    with open(file,mode="r") as outil:
        for x in outil:
            if x==c+'\n':
               return True
    return False

#une fonction qui retourne un dictionaire contenant tout les mots et leurs types
#example 'yields':NNS
def get_types(file):
    types=dict()
    with open(file, mode='r') as mainf:
        for i in mainf:
            line = i.split(" ")
            line = [x for x in line if x and x not in (",") and x!=""]
            line = [ x for x in line if not x.__contains__("[") and not x.__contains__("]")
                    and not x.__contains__("===") ]
            for c in line:

                index=c.find("/")
                if index!=-1:
                    types[c[0:index]]=replace(c[index+1:])
                else:
                    types[c]="NULL"
        return types


#fonction qui genere les types des mots d'avant et xeux d'apres
#example NNS,NNS,NP,NULL,5
def extraction_des_types(main_file,types_file,mot_recherche):
    words_list = []
    all_words = get_types(types_file)
    with open(main_file, mode='r') as mainf:
        for i in mainf:
            line = i.split(" ")
            # suppression des caractaires vide
            line = [x for x in line if x and x not in (',') and not x.__contains__("===")]

            for f in range(len(line)):

                if line[f].__contains__(mot_recherche) and line[f][-2] == "_" and re.search("[0-9]", line[f][-1]):
                    words_list.append([line[f]])

                    if f > 1:
                        words_list[-1].append(all_words[line[f-2]])
                        words_list[-1].append(all_words[line[f-1]])
                    elif f==1:
                        words_list[-1].append(all_words[line[f-1]])
                        words_list[-1].append("NULL")
                    else:
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")

                    if f < len(line) - 3:
                        words_list[-1].append(all_words[line[f+1]])
                        words_list[-1].append(all_words[line[f+2]])
                    elif f == len(line) - 3:
                        words_list[-1].append(all_words[line[f+1]])
                        words_list[-1].append("NULL")
                    else:
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")
    return words_list, all_words




def extraction_avec_stop_words(main_file,mot_recherche):
    words_list = []
    all_words=dict()
    with open(main_file, mode='r') as mainf:
        for i in mainf:
            line = i.split(" ")
        # suppression des caractaires vide
            line = [x for x in line if x and x not in (',')]

            for f in range(len(line)):
                if line[f] != "" and line[f] != "''" and line[f] != "\n" and line[f] != " ":

                    # ajouter le mot dans le dictionaire de mots
                    if replace(line[f]) != "NULL" and not all_words.__contains__(line[f]):
                        all_words[replace(line[f])] = True
                if line[f].__contains__(mot_recherche) and line[f][-2] == "_" and re.search("[0-9]", line[f][-1]):
                    words_list.append([line[f]])
                    if f > 1:
                        words_list[-1].append(replace(line[f-2]))
                        words_list[-1].append(replace(line[f-1]))
                    elif f==1:
                        words_list[-1].append(replace(line[f-1]))
                        words_list[-1].append("NULL")
                    else:
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")

                    if f < len(line) - 3:
                        words_list[-1].append(replace(line[f+1]))
                        words_list[-1].append(replace(line[f+2]))
                    elif f == len(line) - 3:
                        words_list[-1].append(replace(line[f+1]))
                        words_list[-1].append("NULL")
                    else:
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")
    return words_list, all_words




def exctraction(main_file,carac_file,outil_file,mot_recherche):
    words_list=[]
    all_words=dict()
    prev2,prev1,next1,next2=dict(),dict(),dict(),dict()
    first_previous_word,sec_previous_word,first_after_word,sec_after_word=0,0,0,0
    with open(main_file,mode='r') as mainf:
        for i in mainf:
            line= i.split(" ")
            #suppression des caractaires vide
            line=[x  for x in line if x and x not in (',')]

            for f in range(len(line)):

                if line[f] !=""  and line[f]!="''" and line[f]!="\n" and line[f]!=" ":

                    #ajouter le mot dans le dictionaire de mots
                    if replace(line[f])!="NULL" and not all_words.__contains__(line[f]):
                        all_words[replace(line[f])]=True
                if line[f].__contains__(mot_recherche) and line[f][-2]=="_" and re.search("[0-9]",line[f][-1]):
                    #verifier si il existes au moins 2 mot avant
                    words_list.append([line[f]])
                    if f>1:
                        #verifier si les mot ne sont pas des mot outil
                        sec_previous_word=check_if_outil(outil_file,line[f-2])
                        first_previous_word=check_if_outil(outil_file,line[f-1])

                        if first_previous_word and sec_previous_word :
                            #le 1er mot d'avant et le second sont des mot outil
                            if f - 4 >= 0:
                                words_list[-1].append(replace(line[f-4]))
                                words_list[-1].append(replace(line[f - 3]))
                            elif f-3>=0:
                                words_list[-1].append("NULL")
                                words_list[-1].append(replace(line[f-3]))
                            else:
                                words_list[-1].append("NULL")
                                words_list[-1].append("NULL")
                        elif first_previous_word:
                            #seul le 1er mot d'avant est un mot outil
                            if f - 3 >= 0:
                                words_list[-1].append(replace(line[f-3]))
                            words_list[-1].append(replace(line[f-2]))
                            if f-3<0:
                                words_list[-1].append("NULL")
                        elif sec_previous_word:
                            #seul le 2eme mot d'avant est un mot outil
                            if f-3>=0:
                                words_list[-1].append(replace(line[f-3]))
                            else:
                                words_list[-1].append("NULL")
                            words_list[-1].append(replace(line[f-1]))

                        else:
                            #aucun des 2 mot n'est un mot outil
                            words_list[-1].append(replace(line[f-2]))
                            words_list[-1].append(replace(line[f-1]))


                    elif f>0:
                        #il existe seulement un mot avant
                        words_list[-1].append("NULL")
                        words_list[-1].append(replace(line[f-1]))
                    else:
                        #il existe aucun mot avant
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")

                    #verifier que il existe au moins 2 mot apres
                    if f<len(line)-3:
                        first_after_word=check_if_outil(outil_file,line[f+1])
                        sec_after_word=check_if_outil(outil_file,line[f+2])
                        #verifier si les 2 mots apres sont des mots outil
                        if first_after_word and sec_after_word :
                            if f+4<len(line)-1:
                                words_list[-1].append(replace(line[f+3]))
                                words_list[-1].append(replace(line[f+4]))
                            elif f+3<len(line)-1:
                                words_list[-1].append(replace(line[f+3]))
                                words_list[-1].append("NULL")
                            else:
                                words_list[-1].append("NULL")
                                words_list[-1].append("NULL")
                        elif first_after_word:
                            if f+3<len(line[f+3])-1:
                                words_list[-1].append(replace(line[f+2]))
                                words_list[-1].append(replace(line[f+3]))
                            else:
                                words_list[-1].append("NULL")
                                words_list[-1].append(replace(line[f+2]))
                        elif sec_after_word:
                            if f+3<len(line)-1:
                                words_list[-1].append(replace(line[f+1]))
                                words_list[-1].append(replace(line[f+3]))
                            else:
                                words_list[-1].append(replace(line[f+1]))
                                words_list[-1].append("NULL")
                        else:
                            words_list[-1].append(replace(line[f+1]))
                            words_list[-1].append(replace(line[f+2]))

                    elif f<len(line)-1:
                        #il y'a un seul mot apres
                        words_list[-1].append(replace(line[f+1]))
                        words_list[-1].append("NULL")
                    else:
                        #il y'a aucun mot apres
                        words_list[-1].append("NULL")
                        words_list[-1].append("NULL")

    #la liste qui contient tout les mot de gauche et ceux de droite
    return words_list,all_words





def creer_fichier(list_mot,tout_mots,nom_fichier):
    file= open(os.getcwd() + "/" + nom_fichier+".arff","w")
    file.write("@RELATION interest \n\n")
    file.write("@ATTRIBUTE previousWord2 {")
    text=parse_text(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE previousWord1 {")
    text=parse_text(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE nextWord1 {")
    text=parse_text(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE nextWord2 {")
    text=parse_text(tout_mots)
    file.write(text+"}\n")

    file.write("@ATTRIBUTE class {1,2,3,4,5,6} \n")
    file.write("@DATA\n")
    for l in list_mot:
        for x in range(1,len(l)):
            file.write(l[x]+",")
        if l[0][-1]=="s":print(l[0])
        file.write(l[0][-1]+"\n")

    file.close()


def parse_text(tout_mots):
    text = ""
    tout_mots = list(set(tout_mots))
    for key in tout_mots:

        text += key + ","
    text = text[0:-1]
    return text+",NULL"


#generer le fichier des types
def creer_fichier_types(list_mot,tout_mots,nom_fichier):
    file= open(os.getcwd() + "/" +  nom_fichier + ".arff","w")
    file.write("@RELATION interest \n\n")
    file.write("@ATTRIBUTE previousWord2 {")
    text=parse_types(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE previousWord1 {")
    text=parse_types(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE nextWord1 {")
    text=parse_types(tout_mots)
    file.write(text+"}\n")
    file.write("@ATTRIBUTE nextWord2 {")
    text=parse_types(tout_mots)
    file.write(text+"}\n")

    file.write("@ATTRIBUTE class {1,2,3,4,5,6} \n")
    file.write("@DATA\n")
    for l in list_mot:
        for x in range(1,len(l)):
            file.write(l[x]+",")
        if l[0][-1]=="s":print(l[0])
        file.write(l[0][-1]+"\n")

    file.close()

def parse_types(tout_mots):
    text = ""
    t=[]
    print(tout_mots)
    for key,val in tout_mots.items():
        t.append(tout_mots[key])
    t=list(set(t))
    for x in t:
        text+=x+","
    text = text[0:-1]
    return text

if __name__=="__main__":
	dir_path = os.getcwd()
	fichier_original= dir_path + "/interest-original.txt"
	mots_outil= dir_path + "/mot_outil.txt"
	fichier_des_types= dir_path + "/carac.txt"
	list_mots,all_words=exctraction(fichier_original,fichier_des_types,mots_outil,"interest")
	mots,tout_mots=extraction_avec_stop_words(fichier_original,"interest")
	creer_fichier(list_mots,all_words,"file1")
	creer_fichier(mots,tout_mots,"file2")
	list_types,all_types=extraction_des_types(fichier_original,fichier_des_types,"interest")
	creer_fichier_types(list_types, all_types, "file3")
from time import strftime
months = ["SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "pagumen"]
#months=['5','6','7','8','9','10','11','12','13','1','2','3','4']
#ኣዋርሕ = ["መስከረም", "ጥቅምቲ", "ሕዳር", "ታሕሳስ", "ጥሪ", "የካቲት", "መጋቢት", "ሚያዝያ", "ጉንበት", "ሰነ", "ሓምለ", "ነሓሰ", "ጳጉሜን"]
ኣዋርሕ=['1','2','3','4','5','6','7','8','9','10','11','12','13']
ethiopianyear=0
ethiopiandate=0
gregorianDate=0
gregorianYear=0
def Ethiopian_to_gergorian(ethiopiandate,ethiopianMonth,ethiopianyear):
    is_month_from_sep_upto_december=False
    if ((ethiopianyear + 5500) % 4==0):
        
        if (ethiopianMonth == 1) :
            
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 11 <= 30):
                gregorianDate = ethiopiandate + 11;
                gregorianMonth = months[0];
            else :
                gregorianDate = (ethiopiandate + 11) % 30;
                gregorianMonth = months[1];
            
        
        if (ethiopianMonth == 2):
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 11 <= 31):
                gregorianDate = ethiopiandate + 11;
                gregorianMonth = months[1];
            else:
                gregorianDate = (ethiopiandate + 11) % 31;
                gregorianMonth = months[2];
        if (ethiopianMonth == 3): 
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 10 <= 30):
                gregorianDate = ethiopiandate + 10;
                gregorianMonth = months[2];
            else:
                gregorianDate = (ethiopiandate + 10) % 30;
                gregorianMonth = months[3];

        if (ethiopianMonth == 4):
            if (ethiopiandate + 10 <= 31) :
                is_month_from_sep_upto_december=True;
                gregorianDate = ethiopiandate + 10;
                gregorianMonth = months[3];
            else:
                gregorianDate = (ethiopiandate + 10) % 31;
                gregorianMonth = months[4];
        if (ethiopianMonth == 5) :
            if (ethiopiandate + 9 <= 31) :
                gregorianDate = ethiopiandate + 9;
                gregorianMonth = months[4];
            else:
                gregorianDate = (ethiopiandate + 9) % 31;
                gregorianMonth = months[5];
        if (ethiopianMonth == 6):
            if (ethiopiandate + 8 <= 29):
                gregorianDate = ethiopiandate + 8;
                gregorianMonth = months[5];
            else:
                gregorianDate = (ethiopiandate + 8) % 29;
                gregorianMonth = months[6];
        if (ethiopianMonth == 13 & ethiopiandate <= 6):
            gregorianDate = ethiopiandate + 5
            gregorianMonth = months[0]
    else:    
        if (ethiopianMonth == 1):
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 10 <= 30) :
                gregorianDate = ethiopiandate + 10;
                gregorianMonth = months[0];
            else:
                gregorianDate = (ethiopiandate + 10) % 30;
                gregorianMonth = months[1];
        if (ethiopianMonth == 2) :
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 10 <= 31) :
                gregorianDate = ethiopiandate + 10;
                gregorianMonth = months[1];
            else:
                gregorianDate = (ethiopiandate + 10) % 31;
                gregorianMonth = months[2];
        if (ethiopianMonth == 3) :
            is_month_from_sep_upto_december=True;
            if (ethiopiandate + 9 <= 30) :
                gregorianDate = ethiopiandate + 9;
                gregorianMonth = months[2];
            else:
                gregorianDate = (ethiopiandate + 9) % 30;
                gregorianMonth = months[3];
        if (ethiopianMonth == 4) :
            if (ethiopiandate + 9 <= 31) :
                is_month_from_sep_upto_december=True;
                gregorianDate = ethiopiandate + 9;
                gregorianMonth = months[3];
            else:
                gregorianDate = (ethiopiandate + 9) % 31;
                gregorianMonth = months[4];

        if (ethiopianMonth == 5) :
            if (ethiopiandate + 8 <= 31) :
                gregorianDate = ethiopiandate + 8;
                gregorianMonth = months[4];
            else:
                gregorianDate = (ethiopiandate + 8) % 31;
                gregorianMonth = months[5];
        if (ethiopianMonth == 6) :
            if (ethiopiandate + 7 <= 28) :
                gregorianDate = ethiopiandate + 7;
                gregorianMonth = months[5];
            else:
                gregorianDate = (ethiopiandate + 7) % 28;
                gregorianMonth = months[6];
        if (ethiopianMonth == 13 & ethiopiandate <= 5) :
            gregorianDate = ethiopiandate + 5;
            gregorianMonth = months[0];
        if (ethiopianMonth == 7) :
            if (ethiopiandate + 9 <= 31) :
                gregorianDate = ethiopiandate + 9;
                gregorianMonth = months[6];
            else:
                gregorianDate = (ethiopiandate + 10) % 31;
                gregorianMonth = months[7];
        if (ethiopianMonth == 8) :
            if (ethiopiandate + 8 <= 30) :
                gregorianDate = ethiopiandate + 8;
                gregorianMonth = months[7];
            else:
                gregorianDate = (ethiopiandate + 8) % 30;
                gregorianMonth = months[8];
        if (ethiopianMonth == 9) :
            if (ethiopiandate + 8 <= 31) :
                gregorianDate = ethiopiandate + 8;
                gregorianMonth = months[8];
            else:
                gregorianDate = (ethiopiandate + 8) % 31;
                gregorianMonth = months[9];
        if (ethiopianMonth == 10) :
            if (ethiopiandate + 7 <= 30) :
                gregorianDate = ethiopiandate + 7;
                gregorianMonth = months[9];
            else:
                gregorianDate = (ethiopiandate + 7) % 30;
                gregorianMonth = months[10];
        if (ethiopianMonth == 11) :
            if (ethiopiandate + 7 <= 31) :
                gregorianDate = ethiopiandate + 7;
                gregorianMonth = months[10];
            else:
                gregorianDate = (ethiopiandate + 7) % 31;
                gregorianMonth = months[11];
        if (ethiopianMonth == 12) :
            if (ethiopiandate + 6 <= 31) :
                gregorianDate = ethiopiandate + 6;
                gregorianMonth = months[11];
            else:
                gregorianDate = (ethiopiandate + 6) % 31;
                gregorianMonth = months[0];
    
    if (is_month_from_sep_upto_december==True):
        gregorianYear = ethiopianyear + 7;
    else:
        gregorianYear = ethiopianyear + 8;
    #Gergorian_result=(str(gregorianDate) + "/" + str(gregorianMonth) + "/" + str(gregorianYear) + " ዓ.ም.ፈ")
    Gergorian_result=(str(gregorianDate) + "/" + str(gregorianMonth) + "/" + str(gregorianYear))
    return(Gergorian_result)

def Gergorian_to_Ethiopian(gregorianDate,gregorianMonth,gregorianYear):
    is_month_from_sep_upto_december=False

    if (gregorianYear % 4==0):
   
        if (gregorianMonth == 9) :               #//september
            if (gregorianDate <= 5) :
                ethioMonth = ኣዋርሕ[11];
                ethiodate = (31 + gregorianDate) - 6;
            if (gregorianDate >= 6 & gregorianDate <= 11) :
                ethioMonth = ኣዋርሕ[12];
                ethiodate = gregorianDate - 5;
            if (gregorianDate >= 12 & gregorianDate <= 30) :
                is_month_from_sep_upto_december=True;
                ethioMonth = ኣዋርሕ[0];
                ethiodate = gregorianDate - 11;
        if (gregorianMonth == 10) :             #//october
            is_month_from_sep_upto_december=True;
            if (gregorianDate <= 11) :
                ethioMonth = ኣዋርሕ[0];
                ethiodate = (30 + gregorianDate) - 11;
            if (gregorianDate >= 12 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[1];
                ethiodate = gregorianDate - 11;
        if (gregorianMonth == 11):          #//november
            is_month_from_sep_upto_december=True;
            if (gregorianDate <= 10) :
                ethioMonth = ኣዋርሕ[1];
                ethiodate = (31 + gregorianDate) - 11;
            if (gregorianDate >= 11 & gregorianDate <= 30) :
                ethioMonth = ኣዋርሕ[2];
                ethiodate = gregorianDate - 10;
        if (gregorianMonth == 12) :       #//december
            if (gregorianDate <= 10) :
                ethioMonth = ኣዋርሕ[2];
                ethiodate = (30 + gregorianDate) - 10;
            if (gregorianDate >= 11 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[3];
                ethiodate = gregorianDate - 10;
        if (gregorianMonth == 1) :              #//january
            if (gregorianDate <= 9) :
                ethioMonth = ኣዋርሕ[3];
                ethiodate = (31 + gregorianDate) - 10;
            if (gregorianDate >= 10 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[4];
                ethiodate = gregorianDate - 9;
        if (gregorianMonth == 2) :          #//february
            if (gregorianDate <= 8) :
                ethioMonth = ኣዋርሕ[4];
                ethiodate = (31 + gregorianDate) - 9;
            if (gregorianDate >= 9 & gregorianDate <= 29) :
                ethioMonth = ኣዋርሕ[5];
                ethiodate = gregorianDate - 8;
        if (gregorianMonth == 3) :       #//additional
            if (gregorianDate <= 9) :
                ethioMonth = ኣዋርሕ[5];
                ethiodate = (29 + gregorianDate) - 8;
            
    else: 
        if (gregorianMonth == 9) :          # //september
            if (gregorianDate <= 5) :
                ethioMonth = ኣዋርሕ[11];
                ethiodate = (31 + gregorianDate) - 6;
            if (gregorianDate >= 6 & gregorianDate <= 10) :
                ethioMonth = ኣዋርሕ[12];
                ethiodate = gregorianDate - 5;
            if (gregorianDate >= 11 & gregorianDate <= 30) :
                is_month_from_sep_upto_december=True;
                ethioMonth = ኣዋርሕ[0];
                ethiodate = gregorianDate - 10;
        if (gregorianMonth == 10):     #//october
            is_month_from_sep_upto_december=True;
            if (gregorianDate <= 10) :
                ethioMonth = ኣዋርሕ[0];
                ethiodate = (30 + gregorianDate) - 10;
            if (gregorianDate >= 11 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[1];
                ethiodate = gregorianDate - 10;
        if (gregorianMonth == 11) :       #//november
            is_month_from_sep_upto_december=True;
            if (gregorianDate <= 9) :
                ethioMonth = ኣዋርሕ[1];
                ethiodate = (31 + gregorianDate) - 10;
            if (gregorianDate >= 10 & gregorianDate <= 30) :
                ethioMonth = ኣዋርሕ[2];
                ethiodate = gregorianDate - 9;
        if (gregorianMonth == 12) :    #//december
            is_month_from_sep_upto_december=True;
            if (gregorianDate <= 9) :
                ethioMonth = ኣዋርሕ[2];
                ethiodate = (30 + gregorianDate) - 9;
            if (gregorianDate >= 10 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[3];
                ethiodate = gregorianDate - 9;
        if (gregorianMonth == 1) :    #//jan
            if (gregorianDate <= 8) :
                is_month_from_sep_upto_december=True;
                ethioMonth = ኣዋርሕ[3];
                ethiodate = (31 + gregorianDate) - 9;
            if (gregorianDate >= 9 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[4];
                ethiodate = gregorianDate - 8;

        if (gregorianMonth == 2) :    # //feb
            if (gregorianDate <= 7) :
                ethioMonth = ኣዋርሕ[4];
                ethiodate = (31 + gregorianDate) - 8;
            
            if (gregorianDate >= 8 & gregorianDate <= 28) :
                ethioMonth = ኣዋርሕ[5];
                ethiodate = gregorianDate - 7;
            
        
        if (gregorianMonth == 3) :      #//add  feb
            if (gregorianDate <= 8) :
                ethioMonth = ኣዋርሕ[5];
                ethiodate = (29 + gregorianDate) - 7;
            if (gregorianDate >= 10 & gregorianDate <= 31) :
                    ethioMonth = ኣዋርሕ[6];
                    ethiodate = gregorianDate - 9;
        

            # if (gregorianMonth == 3) :    #//mar
                
                
            
        if (gregorianMonth == 4) :    #//ap
            if (gregorianDate <= 8) :
                ethioMonth = ኣዋርሕ[6];
                ethiodate = (31 + gregorianDate) - 9;
            
            if (gregorianDate >= 8 & gregorianDate <= 30) :
                ethioMonth = ኣዋርሕ[7];
                ethiodate = gregorianDate - 8;
            
        
        if (gregorianMonth == 5) :   #//may
            if (gregorianDate <= 8) :
                ethioMonth = ኣዋርሕ[7];
                ethiodate = (30 + gregorianDate) - 8;
            
            if (gregorianDate >= 9 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[8];
                ethiodate = gregorianDate - 8;
            
        
        if (gregorianMonth == 6) :     #//jun
            if (gregorianDate <= 7) :
                ethioMonth = ኣዋርሕ[8];
                ethiodate = (31 + gregorianDate) - 8;
            
            if (gregorianDate >= 7 & gregorianDate <= 30) :
                ethioMonth = ኣዋርሕ[9];
                ethiodate = gregorianDate - 7;
            
        
        if (gregorianMonth == 7) : #//july
            if (gregorianDate <= 7) :
                ethioMonth = ኣዋርሕ[9];
                ethiodate = (30 + gregorianDate) - 7;
            
            if (gregorianDate >= 7 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[10];
                ethiodate = gregorianDate - 7;
            
        
        if (gregorianMonth == 8) :  #//august
            if (gregorianDate <= 6) :
                ethioMonth = ኣዋርሕ[10];
                ethiodate = (31 + gregorianDate) - 7;
            
            if (gregorianDate >= 7 & gregorianDate <= 31) :
                ethioMonth = ኣዋርሕ[11];
                ethiodate = gregorianDate - 6;
    if (is_month_from_sep_upto_december==True): 
        ethioyear = gregorianYear - 7;
    else:
        ethioyear = gregorianYear - 8;
    #ethiopian_result=(str(ethiodate) + "/" + str(ethioMonth )+ "/" + str(ethioyear )+ " ዓ.ም")
    ethiopian_result=(str(ethiodate) + "/" + str(ethioMonth )+ "/" + str(ethioyear ))
    return(ethiopian_result)
#print(Ethiopian_to_gergorian(4,3,2017))
#print(Gergorian_to_Ethiopian(13,11,2024))
#print(Gergorian_to_Ethiopian(int(strftime('%d')),int(strftime('%m')),int(strftime('%Y'))))

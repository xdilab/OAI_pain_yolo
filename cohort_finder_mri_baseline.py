import pandas as pd

from pain_Param import *
from pain_Libraries import *

def main():

    # todo: enrollees.txt ::
    enrollees = pd.read_csv(descript_base_dir + "Enrollees.txt", sep="|")
    enrollee_col = ["ID", "P02HISP", "P02RACE", "P02SEX", "V00CHRTHLF", "V00COHORT", "V00IMAGESC", "V00IMAGESE"]
    enrollees= enrollees[enrollee_col]
    print("enrollees .unique().shape:", enrollees['ID'].unique().shape)

    # todo: AllClinical.txt :: womac pain scores
    # todo: ['V00WOMKPR', 'V00WOMKPL', 'V01WOMKPR', 'V01WOMKPL', 'V03WOMKPR', 'V03WOMKPL', 'V05WOMKPR', 'V05WOMKPL', 'V06WOMKPR', 'V06WOMKPL']
    allclinical_pain_col = [] #
    for visit in [0]:# 0,1,3,5,6,8,10 # 0-> base, 1->12m, 3->24m, 5->36, 6->48 # ,1,3,5,6
        visit_str = "{0:0=2d}".format(visit)
        womac00 = pd.read_csv(descript_base_dir + "AllClinical"+visit_str+".txt",sep="|")
        needed = ["V" + visit_str + "WOMKPR", "V" + visit_str + "WOMKPL"] # V00WOMKPR & V00WOMKPL
        womac00 = womac00[["ID"] + needed]
        print("WOMKP "+visit_str+" .unique().shape:", womac00["ID"].unique().shape )

        allclinical_pain_col.extend(needed)
        enrollees = enrollees.merge(womac00, suffixes=('', '_duplicate'), on='ID', how='left')

    # todo: Outcomes99.txt
    outcomes99 = pd.read_csv(descript_base_dir + "Outcomes99"  + ".txt", sep="|")
    dict ={"id":"ID"}
    outcomes99.rename(columns=dict,inplace=True)
    outcomes99 = outcomes99[["ID", "V99ELKBLRP", "V99ERKBLRP",    # left knee, knee replacement seen on baseline OAI x-ray (calc)
                             "V99ELKDAYS", "V99ERKDAYS",    # days between enrollment visit and follow-up knee replacement
                             "V99ELKLOA", "V99ERKLOA", # V99ELKLOA Num 8 VISIT. Outcomes: left knee, last visit with OA (KLG>=2) (calc)
                             "V99ELXNOA","V99ERXNOA", # V99ELXNOA Num 8 VISIT. Outcomes: left knee, last visit KL < 2 (calc)
                             "V99ELKVSAF", "V99ERKVSAF"]]# V99ELKVSAF Num 8 VISIT. Outcomes: left knee, closest OAI contact after follow-up knee replacement (calc)
    print("outcomes99 .unique().shape:", outcomes99['ID'].unique().shape)
    enrollees = enrollees.merge(outcomes99, suffixes=('', '_duplicate'), on='ID', how='left')

    # todo: BMI:: Clinical_FNIH.txt !!!!!!!!!!!!!!
    # todo: ONLY 600 patient !!!
    Clinical_FNIH = pd.read_csv(descript_base_dir + "Clinical_FNIH" + ".txt", sep="|")
    Clinical_FNIH = Clinical_FNIH[["ID", "P01BMI"]]
    print("Clinical_FNIH .unique().shape:",  Clinical_FNIH['ID'].unique().shape)
    # enrollees = enrollees.merge(Clinical_FNIH, suffixes=('', '_duplicate'), on='ID', how='left')

    # todo: age:: SubjectChar00.txt
    SubjectChar00 = pd.read_csv(descript_base_dir + "SubjectChar00" + ".txt", sep="|")
    SubjectChar00 = SubjectChar00[["ID", "V00AGE"]]
    print("SubjectChar00 unique patients:", SubjectChar00['ID'].unique().shape)
    # enrollees = enrollees.merge(SubjectChar00, suffixes=('', '_duplicate'), on='ID', how='left')

    # todo: age:: MeasInventory.csv
    MeasInventory = pd.read_csv(descript_base_dir + "MeasInventory" + ".csv", sep=",")
    dict ={"id":"ID"}
    MeasInventory.rename(columns=dict,inplace=True)
    MeasInventory = MeasInventory[["ID", "V00AGE","V00XRKLR","V00XRKLL"]] #  V00XRKLL Num 8 LADDER. Baseline KL Grade Left
    print("MeasInventory .unique().shape:", MeasInventory['ID'].unique().shape)
    enrollees = enrollees.merge(MeasInventory, suffixes=('', '_duplicate'), on='ID', how='left')

    # todo: MRI00.txt

    # todo: Duplicates :: if any
    duplicate = [x for x in enrollees.columns if "_duplicate" in x]
    print("Duplicated columns after join:", duplicate)



    # TODO: Filtering Criterias
    print("\nFiltering Criterias")
    enrollees = enrollees.replace('.: Missing Form/Incomplete Workbook', np.nan)
    print( ((enrollees.isna().sum()).to_frame()).T)
    # progression and incident Cohort
    enrollees = enrollees[enrollees["V00COHORT"] != '3: Non-exposed control group']
    print("Cohorts:", enrollees.V00COHORT.unique().T,enrollees.shape)
    # : (1) age, gender, race, and ***BMI*** at baseline;
    enrollees.dropna(subset=["V00AGE", "P02SEX", "P02RACE", "P02HISP"], how='any', inplace=True)
    print("demo:", enrollees['ID'].unique().shape)
    # (2) grade of knee OA at baseline
    enrollees.dropna(subset=["V00XRKLR","V00XRKLL"], how='any', inplace=True)
    enrollees = enrollees[((enrollees["V00XRKLR"] != ".A: Not Expected") & (enrollees["V00XRKLL"] != ".A: Not Expected"))]
    enrollees = enrollees[(( enrollees["V00XRKLR"] != ".T: Technical Problems") & (enrollees["V00XRKLL"] != ".T: Technical Problems") )]
    print("KL grade:", enrollees['ID'].unique().shape)
    # womac normilized to 0 to 100
    right_joint= [x for x in allclinical_pain_col if "WOMKPR" in x]
    left_joint = [x for x in allclinical_pain_col if "WOMKPL" in x]
    # enrollees.dropna(subset=allclinical_pain_col, how='any', inplace=True) # 3784 -> 1347
    enrollees = enrollees[  ~ (enrollees[right_joint].isna().any(axis=1) &  enrollees[left_joint].isna().any(axis=1))   ] # 3795 -> 1354
    print("WOMKP: ", enrollees['ID'].unique().shape)
    # print("min womkp:", enrollees[allclinical_pain_col].min().to_frame().T)
    # print("max womkp:", enrollees[allclinical_pain_col].max().to_frame().T)
    for x in allclinical_pain_col:
        enrollees[x] = enrollees[x] # * 5
    # •	TKR in either knee at baseline # "V99ELKBLRP", "V99ERKBLRP"
    enrollees = enrollees[enrollees["V99ELKBLRP"]!="1: Yes"]
    enrollees = enrollees[enrollees["V99ERKBLRP"] != "1: Yes"]
    print("TKA-baseline: ", enrollees['ID'].unique().shape)

    # todo: select 500


    base_col = ["P02HISP", "P02RACE", "P02SEX", "V00AGE","V00WOMKPR" , "V00WOMKPL", "V00XRKLR","V00XRKLL" ] # baseline KL grade
    selected = pd.DataFrame()
    print(enrollees[base_col].head(2))
    rand_knee = np.random.choice(range((enrollees.shape[0])),replace=False, size=enrollees.shape[0])
    enrollees["left_eligible"] = (rand_knee%2==1)
    enrollees["right_eligible"] = (rand_knee%2==0)#(~rand_knee)
    print(enrollees[["left_eligible","right_eligible"]].head(2))


    if subset_identifier == "_500_maleFemale":
        selected = selected.append(enrollees[enrollees.P02SEX=="1: Male"].sample(n=250,random_state=7)) # , ignore_index=True
        selected = selected.append(enrollees[enrollees.P02SEX!= "1: Male"].sample(n=250, random_state=5))
    elif subset_identifier == "_500_painScore":
        male = enrollees[enrollees.P02SEX == "1: Male"]
        female = enrollees[enrollees.P02SEX != "1: Male"]
        n=  30 # 30        # selected = selected.append(male[    ((male.V00WOMKPR == 0.0 )&( male.right_eligible))|(( male.V00WOMKPL == 0.0 )&( male.left_eligible))  ].sample(n=n, random_state=7))  # , ignore_index=True
        selected = selected.append(male[((male.V00WOMKPR == 0.0) & (male.right_eligible)) ].sample(n=n, random_state=7))
        selected = selected.append(male[((male.V00WOMKPL == 0.0) & (male.left_eligible))].sample(n=n, random_state=8))
        # selected = selected.append(male[    ((male.V00WOMKPR != 0.0 )&( male.right_eligible))|(( male.V00WOMKPL != 0.0 )&( male.left_eligible) )  ].sample(n=(250-n), random_state=5))
        selected = selected.append(male[    (( male.V00WOMKPL != 0.0 )&( male.left_eligible) )  ].sample(n=(125-n), random_state=5))
        selected = selected.append(male[    ((male.V00WOMKPR != 0.0 )&( male.right_eligible))  ].sample(n=(125-n), random_state=6))

        # selected = selected.append(female[  ((female.V00WOMKPR == 0.0 )&( female.right_eligible))|(( female.V00WOMKPL == 0.0 )&( female.left_eligible))   ].sample(n=n, random_state=12))  # , ignore_index=True
        selected = selected.append(female[  (( female.V00WOMKPL == 0.0 )&( female.left_eligible))   ].sample(n=n, random_state=12))
        selected = selected.append(female[  ((female.V00WOMKPR == 0.0 )&( female.right_eligible)) ].sample(n=n, random_state=13))
        # selected = selected.append(female[  ((female.V00WOMKPR != 0.0 )&( female.right_eligible))|(( female.V00WOMKPL != 0.0 )&( female.left_eligible))    ].sample(n=(250 - n), random_state=14))
        selected = selected.append(female[ (( female.V00WOMKPL != 0.0 )&( female.left_eligible))    ].sample(n=(125 - n), random_state=15))
        selected = selected.append(female[  ((female.V00WOMKPR != 0.0 )&( female.right_eligible))   ].sample(n=(125 - n), random_state=14))
    elif subset_identifier == "_overall":
        selected = enrollees
    else:
        print("Error in subset!")
        exit()

    print(selected[selected.right_eligible]['V00WOMKPR'].value_counts().sort_index().to_frame().T)
    print(selected[selected.left_eligible]['V00WOMKPL'].value_counts().sort_index().to_frame().T)
    print(selected['P02SEX'].value_counts().sort_index().to_frame().T)
    print(selected['right_eligible'].value_counts().sort_index().to_frame().T)
    print(selected.shape)
    # print(selected.head(10))

    if True: # plot
        fig = plt.figure(figsize=(8, 9), dpi=80)
        axes = [plt.subplot2grid((4, 2), (i, j), rowspan=1, colspan=1) for i in range(4) for j in range(2)]
        for i, col in enumerate(base_col):
            print(col,end=" ")
            if col in [ "V00AGE","V00WOMKPR" , "V00WOMKPL"]:
                y=10
                if col in ["V00WOMKPR" , "V00WOMKPL"]:
                    y = np.linspace(0,18,19) #  [x for x in range(21)]#20 # len(set(selected[col].value_counts()))
                if subset_identifier == "_500_painScore":
                    if col == "V00WOMKPL": sns.histplot(data=selected[selected.left_eligible], x=col, bins=y, ax=axes[i]) #selected[selected.left_eligible][col].plot.hist(ax=axes[i])
                    elif col == "V00WOMKPR": sns.histplot(data=selected[selected.right_eligible], x=col, bins=y, ax=axes[i]) #selected[selected.right_eligible][col].plot.hist(ax=axes[i])
                    else: sns.histplot(data=selected, x=col, bins=y, ax=axes[i]) #selected[col].plot(kind='hist', bins=y, ax=axes[i])
                else:
                    sns.histplot(data=selected, x=col, bins=y, ax=axes[i])#selected[col].plot(kind = 'hist',bins=y, ax=axes[i]) # value_counts(). .value_counts() .sort_index() #  selected[rnd_itr]
            elif col in ["P02HISP", "P02RACE", "P02SEX", "V00XRKLR","V00XRKLL" ]:
                if subset_identifier == "_500_painScore":
                    if col =="V00XRKLL": sns.countplot(data=selected[selected.left_eligible], x=col,  ax=axes[i]) #selected[selected.left_eligible][col].value_counts().sort_index().plot(kind='bar', ax=axes[i])
                    elif col =="V00XRKLR": sns.countplot(data=selected[selected.right_eligible], x=col, ax=axes[i]) #selected[selected.right_eligible][col].value_counts().sort_index().plot(kind='bar',  ax=axes[i])
                    else: sns.countplot(data=selected, x=col, ax=axes[i]) #selected[col].value_counts().sort_index().plot(kind='bar',  ax=axes[i])
                else:
                    sns.countplot(data=selected, x=col, ax=axes[i]) #selected[col].value_counts().sort_index().plot(kind='bar',  ax=axes[i])  # value_counts(). .value_counts() .sort_index() #  selected[rnd_itr]
            axes[i].set_title(col) # ax0.legend(['train_acc', 'val_acc', 'train_loss', 'val_loss'])
            axes[i].set_ylabel('Frequency')
        for ax in axes:
            for tick in ax.get_xticklabels():
                tick.set_rotation(35)
        fig.tight_layout()
        plt.tight_layout()

    # •	Excluded if partial knee replacement, TKR at baseline, not matched,
    # •	Matched on age, BMI, sex, ethnicity (baseline confounding var.)

    selected.to_csv( "./subset/enrollees"+subset_identifier + ".csv", index=True)
    plt.savefig("./subset/enrollees"+subset_identifier + ".png")
    # plt.show()

if __name__ == '__main__':
    main()
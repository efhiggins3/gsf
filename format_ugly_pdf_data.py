import PyPDF2
import re

pdfFileObject = open('/Users/ehiggins/Downloads/all_students_printed.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)

p_number = 13
#for p_number in range(6,13):
blob = pdfReader.getPage(p_number).extractText()
#
#ScaleScore NN SN IN NormalCurveEquivalent%ileStanine%ileStanine%ileStanine
#Koopman, Amon 701n/an/a979969n/a
#Winter, Nina 701n/an/a979969n/a
#
heading = "ScaleScore NN SN IN NormalCurveEquivalent%ileStanine%ileStanine%ileStanin" # e left off purposely
data_start = blob.find(heading)
data_blob = blob[data_start + len(heading):]
data_split = re.split(r"([^\s\-][A-Z])", data_blob)
#name_pattern = re.compile("([^\d]+)\s[\d|NR]{2}")
name_pattern = re.compile("([^\d]+)\s[\d{2}|NR]")
name_w_initial_pattern = re.compile("([^\d]+\s[A-Z])[\d|NR]{2}")
has_initial = re.compile("\s[A-Z]$")
scale_score_pattern = re.compile("\s([\dNR]{2,3})")
scale_score_w_initial_pattern = re.compile("([\d]{3})")
digits2 = re.compile("(\d{2})")
digits1 = re.compile("(\d{1})")
#
#
# NOTE: ONLY RESET SCORES IF THE PAGE IS A NEW PAGE. FOR CLASSES THAT RUN OVER, DO NOT RESET
prior_nn_score = 100
prior_nn_stanine = 10
prior_sn_score = 100
prior_sn_stanine = 10
prior_in_score = 100
prior_in_stanine = 10
#
for i in range(len(data_split)):
    f = data_split[i]
    prior_f = data_split[i-1]
    pprior_f = data_split[i-2]
    if i < len(data_split)-1:
        next_f = data_split[i+1]
    else:
        next_f = ""
    if len(data_split[i]) < 10:
        continue
    if next_f == "NR":
        full_line = prior_f[1:] + data_split[i] + next_f + data_split[i+2] # For "NR" = not rated
    elif len(f) > 10:
        full_line = prior_f[1:] + data_split[i]
    else:
        full_line = pprior_f[1:] + pprior_f + data_split[i] # For McWilliams: "aM"+"cW"+illiams"
    # Flipped these for pages 10 onwards
    try:
        name = name_w_initial_pattern.findall(full_line)[0]
    except IndexError:
        name = name_pattern.findall(full_line)[0]
    try:
        scale_score = scale_score_w_initial_pattern.findall(full_line)[0]
    except IndexError:
        scale_score = scale_score_pattern.findall(full_line)[0]
    #
    # NN #'s
    #
    #nn_score = 'n/a'
    #nn_stanine = 'n/a'
    #nn = nn_score + nn_stanine
    #
    #
    #TEST IF NAME ENDS IN MIDDLE INITIAL
    if bool(has_initial.search(name)):
        initial_increment = 0
    else:
        initial_increment = 1
    start_at = len(name + scale_score) + initial_increment
    #
    #
    next_chunk = full_line[start_at:start_at+3]
    if next_chunk == 'n/a':
        nn_score = 'n/a'
        nn_stanine = 'n/a'
    else:
        nn_score = next_chunk[:2]
        nn_stanine = next_chunk[-1:]
        if int(nn_score) > int(prior_nn_score):
            nn_score = next_chunk[:1]
            nn_stanine = next_chunk[1:2]
    nn = str(nn_score) + str(nn_stanine)
    prior_nn_score = nn_score
    prior_nn_stanine = nn_stanine
    #
    # SN #'s
    #
    start_at = len(name + scale_score + nn) + initial_increment
    next_chunk = full_line[start_at:start_at+3]
    if next_chunk == 'n/a':
        sn_score = 'n/a'
        sn_stanine = 'n/a'
    else:
        sn_score = next_chunk[:2]
        sn_stanine = next_chunk[-1:]
        if int(sn_score) > int(prior_sn_score):
            sn_score = next_chunk[:1]
            sn_stanine = next_chunk[1:2]
    sn = str(sn_score) + str(sn_stanine)
    prior_sn_score = sn_score
    prior_sn_stanine = sn_stanine
    #
    # IN #'s
    #
    start_at = len(name + scale_score + nn + sn) + initial_increment
    next_chunk = full_line[start_at:start_at+3]
    if next_chunk == 'n/a':
        in_score = 'n/a'
        in_stanine = 'n/a'
    else:
        in_score = next_chunk[:2]
        in_stanine = next_chunk[-1:]
        if int(in_score) > int(prior_in_score):
            in_score = next_chunk[:1]
            in_stanine = next_chunk[1:2]
    sn = str(in_score) + str(in_stanine)
    prior_in_score = in_score
    prior_in_stanine = in_stanine
    #
    #
    #
    print(name + "," + scale_score + "," +
          str(nn_score) + "," + str(nn_stanine) + "," +
          str(sn_score) + "," + str(sn_stanine) + "," +
          str(in_score) + "," + str(in_stanine) + "," +
          str(p_number))

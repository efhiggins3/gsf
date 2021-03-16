from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

read_file_loc = '/Users/ehiggins/Desktop/gsf/formatted_data.csv'
data_in = open(read_file_loc, 'r')

# Read each line of data
header = data_in.readline().rstrip()
line = data_in.readline().rstrip()
while line:
    fields = line.split('\t')
    last_name = fields[0]
    first_name = fields[1]
    grade = fields[2]
    level = int(grade)-1
    ReadingCompScaledScore = fields[3]
    Comparison = fields[4]
    ReadingCompPercentile = fields[5]
    ReadingCompStanine = fields[6]
    MathName = fields[7]
    MathScaledScore = fields[8]
    MathCompPercentile = fields[9]
    MathCompStanine = fields[10]
    StudentId = fields[11]
    #
    canvas = Canvas('/Users/ehiggins/Desktop/gsf/output/'+grade+"_"+StudentId+".pdf")
    canvas.setPageSize(size=(2034, 1056))
    canvas.drawImage("/Users/ehiggins/Desktop/gsf/template.png", 0, 0, 2034, 1056)
    #canvas.create_text(574, 133, fill="darkblue", font=("Purisa italic bold", 12), text= "Foo Bar")
    #
    # Student Name
    canvas.setFont('Helvetica-Bold', 28)
    canvas.drawString(571, 916, last_name + ", " + first_name)
    #
    # Scaled Score
    canvas.setFont('Helvetica', 31)
    canvas.drawString(765, 307, ReadingCompScaledScore)
    canvas.drawString(765, 267, MathScaledScore)
    #
    # Percentile
    canvas.drawString(920, 307, ReadingCompPercentile)
    canvas.drawString(920, 267, MathCompPercentile)
    #
    # Stanine
    canvas.drawString(1054, 307, ReadingCompStanine)
    canvas.drawString(1054, 267, MathCompStanine)
    canvas.drawString(164, 267, MathName)
    #
    # Grade
    canvas.setFont('Helvetica-Bold', 29)
    canvas.setFillColorRGB(255,255,255)
    canvas.drawString(1635, 835, grade)
    canvas.drawString(1768, 835, str(level))
    if Comparison == 'Independent':
        canvas.drawString(910, 464, Comparison)
    else:
        canvas.drawString(940, 464, Comparison)
    #
    #canvas.showPage()
    canvas.save()
    print(last_name + ", " + first_name + ", grade " + grade)
    line = data_in.readline().rstrip()

data_in.close()

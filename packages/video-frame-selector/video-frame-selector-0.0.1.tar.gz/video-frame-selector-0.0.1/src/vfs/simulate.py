import os
from time import sleep


input_dir = "/home/fracpete/development/projects/waikato-datamining/video-frame-selector/test/analysis/input"
output_dir = "/home/fracpete/development/projects/waikato-datamining/video-frame-selector/test/analysis/output"
tmp_dir = "/home/fracpete/development/projects/waikato-datamining/video-frame-selector/test/analysis/tmp"

content = """file,x0,y0,x1,y1,x0n,y0n,x1n,y1n,label,label_str,score
{FILE},1325.572,345.08112,1585.4998,460.26697,0.4259550197571899,0.1585850715637207,0.5094793559959431,0.2115197462194106,0,{LABEL1},0.04
{FILE},1402.7565,1205.6069,1472.7654,1287.2013,0.4507572203491525,0.5540473040412454,0.4732536570884881,0.5915447122910443,0,{LABEL2},0.04
{FILE},1893.0239,208.97534,2501.9468,551.60785,0.6082981766649261,0.09603646222282858,0.8039674734395084,0.2534962541916791,0,{LABEL1},0.9
{FILE},1893.0239,208.97534,2501.9468,551.60785,0.6082981766649261,0.09603646222282858,0.8039674734395084,0.2534962541916791,0,{LABEL2},0.9
"""

while True:
    any = False
    for f in os.listdir(input_dir):
        if not f.endswith(".jpg"):
            continue

        name = f.replace(".jpg", ".csv")
        any = True

        img_in_file = os.path.join(input_dir, f)
        img_out_file = os.path.join(output_dir, f)
        csv_tmp_file = os.path.join(tmp_dir, name)
        csv_out_file = os.path.join(output_dir, name)

        os.rename(img_in_file, img_out_file)
        with open(csv_tmp_file, "w") as cf:
            c = content.replace("{FILE}", f)
            c = c.replace("{LABEL1}", "goat")
            c = c.replace("{LABEL2}", "human")
            cf.write(c)
            cf.write("\n")
        os.rename(csv_tmp_file, csv_out_file)

    if not any:
        sleep(1)

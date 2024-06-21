class Config():

    resize_h = 800
    
    resize_w = 640
    
    model_path = "/home/kullanici1/CCAIv2/src/cases/point_detection/cephalometric/src/models/cephalometric_landmark_model.pth"

    model_point_names = {"A point": 0, "Anterior Nasal Spina (ANS)": 1, "Articulare (Ar)": 2, "B point": 3,
                         "Basion (Ba)": 4, "Columella (Cm)": 5, "Glabella (G’)": 6, "Gnathion (Gn)": 7,
                         "Gnathion Soft Tissue (Gn’)": 8, "Gonion (Go)": 9, "Hinge Axis (HA)": 10, "L6o": 11,
                         "Labiale inferior (Li)": 12, "Labrale superior (Ls)": 13, "Md1c": 14, "Md1r": 15, "Md6d": 16,
                         "Md6m": 17, "Menton (Me)": 18, "Mx1c": 19, "Mx1r": 20, "Mx6d": 21, "Mx6m": 22,
                         "Nasal Dorsum": 23, "Nasion (N)": 24, "Orbitale (Or)": 25, "Pogonion (Pg)": 26,
                         "Porion (Po)": 27, "Posterior Nasal Spina (PNS)": 28, "Pronasale (Pn)": 29,
                         "Pterygoid (Pt)": 30, "Ramus (Ra)": 31, "Sella (S)": 32, "Soft Tissue A point (A’)": 33,
                         "Soft Tissue B point (B’)": 34, "Soft Tissue Nasion (N’)": 35, "Soft tissue Menton (Me’)": 36,
                         "Soft tissue Pogonion (Pg’)": 37, "Stomion inferius (Si)": 38, "Stomion superius (Ss)": 39,
                         "Subnasale (Sn)": 40, "U6o": 41}

    planes = {"SN plane": ["Nasion (N)", "Sella (S)"], "MD plane": ["Gonion (Go)", "Menton (Me)"],
              "RD plane": ["Articulare (Ar)", "Gonion (Go)"], "FH plane": ["Orbitale (Or)", "Porion (Po)"],
              "N-Ba plane": ["Nasion (N)", "Basion (Ba)"], "S-Ba plane": ["Sella (S)", "Basion (Ba)"],
              "S-Ar plane": ["Sella (S)", "Articulare (Ar)"], "S-Gn plane": ["Sella (S)", "Gnathion (Gn)"],
              "NA plane": ["Nasion (N)", "A point"], "NB plane": ["Nasion (N)", "B point"],
              "N-Pog plane": ["Nasion (N)", "Pogonion (Pg)"],
              "PD plane": ["Anterior Nasal Spina (ANS)", "Posterior Nasal Spina (PNS)"],
              "Pt-Gn plane": ["Pterygoid (Pt)", "Gnathion (Gn)"], "Upper incisor plane": ["Mx1c", "Mx1r"],
              "Lower incisor plane": ["Md1c", "Md1r"], "Occlusal plane": ["Mid Md1c-Mx1c", "Mid L6o-U6o"],
              "Steiner's S plane": ["Columella (Cm)", "Soft tissue Pogonion (Pg’)"],
              "Go-Gn plane": ["Gonion (Go)", "Gnathion (Gn)"], "Go-N plane": ["Gonion (Go)", "Nasion (N)"],
              "A-B plane": ["A point", "B point"]}

    angles = {"SNA Angle": ["SN plane", "NA plane"], "SNB Angle": ["SN plane", "NB plane"],
              "ANB Angle": ["NA plane", "NB plane"], "Sella Angle": ["SN plane", "S-Ar plane"],
              "FMA Angle": ["FH plane", "MD plane"], "Articular Angle": ["S-Ar plane", "RD plane"],
              "Gonial Angle": ["RD plane", "MD plane"], "SN-GoMe Angle": ["SN plane", "MD plane"],
              "Cranial Base Angle": ["SN plane", "S-Ba plane"], "Ramus Plane Angle": ["SN plane", "RD plane"],
              "Upper Incisor-SN Angle": ["Upper incisor plane", "SN plane"],
              "Lower Incisor-MD Angle": ["Lower incisor plane", "MD plane"],
              "Between the Incisors Angle": ["Upper incisor plane", "Lower incisor plane"],
              "Saddle Angle": ["SN plane", "S-Ar plane"], "Upper Gonial Angle": ["RD plane", "Go-N plane"],
              "Lower Gonial Angle": ["Go-N plane", "Go-Gn plane"],
              "Convexity Angle (DOWNS)": ["A-B plane", "N-Pog plane"]}

    measurements = {"Wits Appraisal": {"measurement_points": ["A processed point", "B processed point"],
                                       "measure_type": "hypotenuse"},
                    "Li-SL": {"measurement_points": ["Labiale inferior (Li)", "Li processed point"],
                              "measure_type": "hypotenuse"},
                    "Ls-SL": {"measurement_points": ["Labrale superior (Ls)", "Ls processed point"],
                              "measure_type": "hypotenuse"},
                    "Overjet": {"measurement_points": ["Md1c", "Mx1c"], "measure_type": "horizontal"},
                    "Overbite": {"measurement_points": ["Md1c", "Mx1c"], "measure_type": "vertical"},
                    "Ant. Cranial Base": {"measurement_points": ["Sella (S)", "Nasion (N)"],
                                          "measure_type": "hypotenuse"},
                    "Post. Cranial Base": {"measurement_points": ["Sella (S)", "Articulare (Ar)"],
                                           "measure_type": "hypotenuse"},
                    "Ramus Height": {"measurement_points": ["Articulare (Ar)", "Gonion (Go)"],
                                     "measure_type": "hypotenuse"},
                    "Mandibular Body": {"measurement_points": ["Gonion (Go)", "Gnathion (Gn)"],
                                        "measure_type": "hypotenuse"},
                    "Post. Face Height": {"measurement_points": ["Sella (S)", "Gonion (Go)"],
                                          "measure_type": "hypotenuse"},
                    "Ant. Face Height": {"measurement_points": ["Nasion (N)", "Gnathion (Gn)"],
                                         "measure_type": "hypotenuse"},
                    "Upper Face Height": {"measurement_points": ["Nasion (N)", "Anterior Nasal Spina (ANS)"],
                                          "measure_type": "vertical"},
                    "Lower Face Height": {"measurement_points": ["Anterior Nasal Spina (ANS)", "Gnathion (Gn)"],
                                          "measure_type": "vertical"},
                    "Face Height": {"measurement_points": ["Nasion (N)", "Gnathion (Gn)"], "measure_type": "vertical"},
                    "PoGonion": {"measurement_points": ["Porion (Po)", "Gonion (Go)"], "measure_type": "hypotenuse"}}

    ratios = {"Upper Face Height Ratio": ["Upper Face Height", "Face Height"],
              "Lower Face Height Ratio": ["Lower Face Height", "Face Height"]}

    spline_points = [["Glabella (G’)", "Soft Tissue Nasion (N’)", "Nasal Dorsum", "Pronasale (Pn)", "Columella (Cm)",
                      "Subnasale (Sn)", "Soft Tissue A point (A’)", "Labrale superior (Ls)", "Stomion superius (Ss)"],
                     ["Stomion inferius (Si)", "Labiale inferior (Li)", "Soft Tissue B point (B’)",
                      "Soft tissue Pogonion (Pg’)", "Gnathion Soft Tissue (Gn’)", "Soft tissue Menton (Me’)"],
                     ["Pogonion (Pg)", "Gnathion (Gn)", "Menton (Me)", "Gonion (Go)", "Ramus (Ra)", "Articulare (Ar)"]]

    analysis_types = {"Bjork-Jarabak Analysis": {
        "angle_results": ["Saddle Angle", "Articular Angle", "Gonial Angle", "Upper Gonial Angle",
                          "Lower Gonial Angle"],
        "measurement_results": ["Ant. Cranial Base", "Post. Cranial Base", "Ramus Height", "Mandibular Body",
                                "Post. Face Height", "Ant. Face Height"],
        "ratio_results": ["Upper Face Height Ratio", "Lower Face Height Ratio"]},
                      "Skeletal Factors - Anterior/Posterior": {
                          "angle_results": ["SNA Angle", "SNB Angle", "ANB Angle", "Convexity Angle (DOWNS)"],
                          "measurement_results": ["Wits Appraisal", "PoGonion"]},
                      "Wits Analysis": {"measurement_results": ["Wits Appraisal"]}}

    analysis_report_dict = {}
    analysis_report_dict.update({"calibration_points": {"calibration_point_xy": [], "calibration_measure": None},
                                 "results": {"cephalometric_landmarks": [], "angle_results": {},
                                             "measurement_results": {}, "ratio_results": {}, "spline_points": {},
                                             "planes": {}, "analysis_types": {}}})

    cephalometric_landmarks = {}
    cephalometric_landmarks.update({"coordinates": [], "label": None, "marking_type": "point"})
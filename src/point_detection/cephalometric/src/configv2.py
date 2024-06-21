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

    angles = {"SNA Angle": {"angle_plants": ["SN plane", "NA plane"], "description": "", "type": "Deg", "mean": 82.0,
                            "sd": 2.0},
              "SNB Angle": {"angle_plants": ["SN plane", "NB plane"], "description": "", "type": "Deg", "mean": 80.0,
                            "sd": 2.0},
              "ANB Angle": {"angle_plants": ["NA plane", "NB plane"], "description": "", "type": "Deg", "mean": 2.0,
                            "sd": 2.0},
              "Sella Angle": {"angle_plants": ["SN plane", "S-Ar plane"], "description": "", "type": "Deg", "mean": "",
                              "sd": ""},
              "FMA Angle": {"angle_plants": ["FH plane", "MD plane"], "description": "", "type": "Deg", "mean": "",
                            "sd": ""},
              "Articular Angle": {"angle_plants": ["S-Ar plane", "RD plane"], "description": "S-Ar-Go", "type": "Deg",
                                  "mean": 143.0, "sd": 5.0},
              "Gonial Angle": {"angle_plants": ["RD plane", "MD plane"], "description": "Ar-Go-Gn", "type": "Deg",
                               "mean": 130.0, "sd": 5.0},
              "SN-GoMe Angle": {"angle_plants": ["SN plane", "MD plane"], "description": "", "type": "Deg", "mean": "",
                                "sd": ""},
              "Cranial Base Angle": {"angle_plants": ["SN plane", "S-Ba plane"], "description": "", "type": "Deg",
                                     "mean": "", "sd": ""},
              "Ramus Plane Angle": {"angle_plants": ["SN plane", "RD plane"], "description": "", "type": "Deg",
                                    "mean": "", "sd": ""},
              "Upper Incisor-SN Angle": {"angle_plants": ["Upper incisor plane", "SN plane"], "description": "",
                                         "type": "Deg", "mean": "", "sd": ""},
              "Lower Incisor-MD Angle": {"angle_plants": ["Lower incisor plane", "MD plane"], "description": "",
                                         "type": "Deg", "mean": "", "sd": ""},
              "Between the Incisors Angle": {"angle_plants": ["Upper incisor plane", "Lower incisor plane"],
                                             "description": "", "type": "Deg", "mean": "", "sd": ""},
              "Saddle Angle": {"angle_plants": ["SN plane", "S-Ar plane"], "description": "N-S-Ar", "type": "Deg",
                               "mean": 123.0, "sd": 4.0},
              "Upper Gonial Angle": {"angle_plants": ["RD plane", "Go-N plane"], "description": "Ar-Go-N",
                                     "type": "Deg", "mean": 53.0, "sd": 2.0},
              "Lower Gonial Angle": {"angle_plants": ["Go-N plane", "Go-Gn plane"], "description": "N-Go-Gn ",
                                     "type": "Deg", "mean": 73.0, "sd": 3.0},
              "Convexity Angle (DOWNS)": {"angle_plants": ["A-B plane", "N-Pog plane"], "description": "-",
                                          "type": "Deg", "mean": 180.0, "sd": 5.0}}

    measurements = {"Wits Appraisal": {"measurement_points": ["A processed point", "B processed point"],
                                       "measure_type": "hypotenuse", "description": "WITS", "type": "mm", "mean": 0.0,
                                       "sd": 1.0},
                    "Li-SL": {"measurement_points": ["Labiale inferior (Li)", "Li processed point"],
                              "measure_type": "hypotenuse", "description": "", "type": "mm", "mean": "", "sd": ""},
                    "Ls-SL": {"measurement_points": ["Labrale superior (Ls)", "Ls processed point"],
                              "measure_type": "hypotenuse", "description": "", "type": "mm", "mean": "", "sd": ""},
                    "Overjet": {"measurement_points": ["Md1c", "Mx1c"], "measure_type": "horizontal",
                                "description": "OVERJET", "type": "mm", "mean": 2.5, "sd": 2.0},
                    "Overbite": {"measurement_points": ["Md1c", "Mx1c"], "measure_type": "vertical",
                                 "description": "OVERBITE", "type": "mm", "mean": 2.5, "sd": 2.0},
                    "Ant. Cranial Base": {"measurement_points": ["Sella (S)", "Nasion (N)"],
                                          "measure_type": "hypotenuse", "description": "N-S", "type": "mm",
                                          "mean": 71.0, "sd": 10.0},
                    "Post. Cranial Base": {"measurement_points": ["Sella (S)", "Articulare (Ar)"],
                                           "measure_type": "hypotenuse", "description": "S-Ar", "type": "mm",
                                           "mean": 32.0, "sd": 5.0},
                    "Ramus Height": {"measurement_points": ["Articulare (Ar)", "Gonion (Go)"],
                                     "measure_type": "hypotenuse", "description": "Ar-Go", "type": "mm", "mean": 44.0,
                                     "sd": 5.0},
                    "Mandibular Body": {"measurement_points": ["Gonion (Go)", "Gnathion (Gn)"],
                                        "measure_type": "hypotenuse", "description": "Go-Gn", "type": "mm",
                                        "mean": 71.0, "sd": 8.0},
                    "Post. Face Height": {"measurement_points": ["Sella (S)", "Gonion (Go)"],
                                          "measure_type": "hypotenuse", "description": "S-Go", "type": "mm",
                                          "mean": "-", "sd": "-"},
                    "Ant. Face Height": {"measurement_points": ["Nasion (N)", "Gnathion (Gn)"],
                                         "measure_type": "hypotenuse", "description": "N-Gn", "type": "mm", "mean": "-",
                                         "sd": "-"},
                    "Upper Face Height": {"measurement_points": ["Nasion (N)", "Anterior Nasal Spina (ANS)"],
                                          "measure_type": "vertical", "description": "N-ANS", "type": "mm", "mean": "-",
                                          "sd": "-"},
                    "Lower Face Height": {"measurement_points": ["Anterior Nasal Spina (ANS)", "Gnathion (Gn)"],
                                          "measure_type": "vertical", "description": "ANS-Gn", "type": "mm",
                                          "mean": "-", "sd": "-"},
                    "Face Height": {"measurement_points": ["Nasion (N)", "Gnathion (Gn)"], "measure_type": "vertical",
                                    "description": "N-Gn", "type": "mm", "mean": "-", "sd": "-"},
                    "PoGonion": {"measurement_points": ["Porion (Po)", "Gonion (Go)"], "measure_type": "hypotenuse",
                                 "description": "", "type": "mm", "mean": "-", "sd": "-"}}

    ratios = {"Upper Face Height Ratio": {"ratio_heights": ["Upper Face Height", "Face Height"], "description": "N-ANS",
                                          "type": "%", "mean": "-", "sd": "-"},
              "Lower Face Height Ratio": {"ratio_heights": ["Lower Face Height", "Face Height"],
                                          "description": "ANS-Gn", "type": "%", "mean": "-", "sd": "-"}}

    spline_points = [["Glabella (G’)", "Soft Tissue Nasion (N’)", "Nasal Dorsum", "Pronasale (Pn)", "Columella (Cm)",
                      "Subnasale (Sn)", "Soft Tissue A point (A’)", "Labrale superior (Ls)", "Stomion superius (Ss)"],
                     ["Stomion inferius (Si)", "Labiale inferior (Li)", "Soft Tissue B point (B’)",
                      "Soft tissue Pogonion (Pg’)", "Gnathion Soft Tissue (Gn’)", "Soft tissue Menton (Me’)"],
                     ["Pogonion (Pg)", "Gnathion (Gn)", "Menton (Me)", "Gonion (Go)", "Ramus (Ra)", "Articulare (Ar)"]]

    analysis_types = {"Bjork-Jarabak Analysis": {
        "angles": ["Saddle Angle", "Articular Angle", "Gonial Angle", "Upper Gonial Angle", "Lower Gonial Angle"],
        "measurements": ["Ant. Cranial Base", "Post. Cranial Base", "Ramus Height", "Mandibular Body",
                         "Post. Face Height", "Ant. Face Height"],
        "ratios": ["Upper Face Height Ratio", "Lower Face Height Ratio"]}, "Skeletal Factors - Anterior/Posterior": {
        "angles": ["SNA Angle", "SNB Angle", "ANB Angle", "Convexity Angle (DOWNS)"],
        "measurements": ["Wits Appraisal", "PoGonion"]}, "Wits Analysis": {"measurements": ["Wits Appraisal"]}}

    analysis_report_dict = {}
    analysis_report_dict.update({"calibration_points": {"calibration_points_xy": [], "calibration_measure": None},
                                 "results": {"cephalometric_landmarks": [], "angles": {}, "measurements": {},
                                             "ratios": {}, "spline_points": {}, "planes": {}, "analysis_types": {}}})

    cephalometric_landmarks = {}
    cephalometric_landmarks.update({"coordinates": [], "label": None, "marking_type": "point"})
from src.point_detection.cephalometric.src.model import Farnet
from src.point_detection.cephalometric.src.configv4 import Config
from src.point_detection.cephalometric.src.utils import get_prepoint_from_htmp
import numpy as np
import cv2
import torch
import math
import json
import warnings
warnings.filterwarnings("ignore")


class CephalometricAnalysis():
    def __init__(self, image=None,
                 calibration_points=[],
                 calibration_measure=None,
                 pixel_to_mm=10,
                 angles=Config.angles,
                 measurements=Config.measurements,
                 ratios=Config.ratios,
                 spline_points=Config.spline_points,
                 model_point_names=Config.model_point_names,
                 planes=Config.planes,
                 analysis_points=None,
                 gender=None,
                 analysis_report={},
                 analysis_report_dict={}):
        self.model = self.load_model()
        self.image = image
        self.calibration_points = calibration_points
        self.calibration_measure = calibration_measure
        self.pixel_to_mm = pixel_to_mm
        self.angles = angles
        self.measurements = measurements
        self.ratios = ratios
        self.spline_points = spline_points
        self.model_point_names = model_point_names
        self.planes = planes
        self.analysis_points = analysis_points
        self.gender = gender
        self.analysis_report = analysis_report
        self.analysis_report_dict = analysis_report_dict
        
    def reset_params(self):
        defaults = self.__class__.__init__.__defaults__
        if defaults is not None:
            num_params = len(defaults)
            param_names = list(self.__class__.__init__.__code__.co_varnames[1:num_params + 1])
            for param in param_names:
                if param != "model":
                    setattr(self, param, defaults[param_names.index(param)])
            
    def load_image(self, image):
        self.reset_params()
        self.image = cv2.imread(image)
        
    def load_model(self):
        model = Farnet()
        checkpoint = torch.load(Config.model_path, map_location=torch.device('cpu'))  # Modeli CPU'ya yükle
        model.load_state_dict(checkpoint)
        return model
        
    def set_calculate_calibration_measure(self):
        points_distance = math.hypot(self.calibration_points[0][0] - self.calibration_points[1][0], self.calibration_points[0][1] - self.calibration_points[1][1])
        self.pixel_to_mm = points_distance / self.calibration_measure
        
    def calculate_mid_point(self, point1, point2):
        return ((np.array(point1) + np.array(point2)) / 2).tolist()
        
    def get_points(self):
        img_h, img_w, _ = self.image.shape
        img_resize = cv2.resize(self.image, (Config.resize_w, Config.resize_h))
        img_data = np.transpose(img_resize, (2, 0, 1))
        img_data = np.reshape(img_data, (1, 3, Config.resize_h, Config.resize_w))
        img_data = torch.from_numpy(img_data).float().cpu()
        scal_ratio_w = img_w / Config.resize_w
        scal_ratio_h = img_h / Config.resize_h
        outputs, _ = self.model(img_data)
        outputs = outputs[0].detach().cpu().numpy()
        analysis_points = get_prepoint_from_htmp(outputs, scal_ratio_w, scal_ratio_h)
        self.analysis_points = {
            list(self.model_point_names.keys())[i]: [round(x, 2) for x in analysis_points[i].tolist()]
            for i in range(len(analysis_points))
        }
        self.get_additional_points()
        
    def get_additional_points(self):
        self.analysis_points["Mid Md1c-Mx1c"] = self.calculate_mid_point(self.analysis_points["Md1c"], self.analysis_points["Mx1c"])
        self.analysis_points["Mid L6o-U6o"] = self.calculate_mid_point(self.analysis_points["L6o"], self.analysis_points["U6o"])
        self.analysis_points["A processed point"] = self.find_projected_point(self.analysis_points["A point"], self.planes["Occlusal plane"])
        self.analysis_points["B processed point"] = self.find_projected_point(self.analysis_points["B point"], self.planes["Occlusal plane"])
        self.analysis_points["Li processed point"] = self.find_projected_point(self.analysis_points["Labiale inferior (Li)"], self.planes["Steiner's S plane"])
        self.analysis_points["Ls processed point"] = self.find_projected_point(self.analysis_points["Labrale superior (Ls)"], self.planes["Steiner's S plane"])
        self.analysis_points["Mx1c processed point"] = self.find_projected_point(self.analysis_points["Mx1c"], self.planes["A-Pg plane"])
                                
    def find_projected_point(self, point, plane):
        point = np.array(point, dtype=np.float64)
        line_point1 = np.array(self.analysis_points[plane[0]], dtype=np.float64)
        line_point2 = np.array(self.analysis_points[plane[1]], dtype=np.float64)
        direction_vector = line_point2 - line_point1
        direction_vector /= np.linalg.norm(direction_vector)
        point_vector = point - line_point1
        dot_product = np.dot(point_vector, direction_vector)
        projection_vector = dot_product * direction_vector
        projected_point = line_point1 + projection_vector
        return list(map(int, projected_point.tolist()))

    def calculate_angle(self, line1_start, line1_end, line2_start, line2_end):
        dx1 = line1_end[0] - line1_start[0]
        dy1 = line1_end[1] - line1_start[1]
        dx2 = line2_end[0] - line2_start[0]
        dy2 = line2_end[1] - line2_start[1]
        cross_product = dx1 * dy2 - dx2 * dy1
        angle = math.degrees(math.atan2(cross_product, dx1 * dx2 + dy1 * dy2))
        if angle < 0:
            angle += 180
        return angle

    def calculate_distance(self, point1, point2, measure_type):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        if measure_type == 'horizontal':
            return dx / self.pixel_to_mm
        elif measure_type == 'vertical':
            return dy / self.pixel_to_mm
        elif measure_type == 'hypotenuse':
            return math.hypot(dx, dy) / self.pixel_to_mm
        
    def angle_results(self):
        angle_analysis = {}
        for angle_name, angle_feature in self.angles.items():

            line1_start = self.analysis_points[self.planes[angle_feature["angle_planes"][0]][0]]
            line1_end = self.analysis_points[self.planes[angle_feature["angle_planes"][0]][1]]
            line2_start = self.analysis_points[self.planes[angle_feature["angle_planes"][1]][0]]
            line2_end = self.analysis_points[self.planes[angle_feature["angle_planes"][1]][1]]
            angle_analysis[angle_name] = [Config.angles[angle_name]["description"],
                                          Config.angles[angle_name]["type"],
                                          Config.angles[angle_name]["mean"],
                                          Config.angles[angle_name]["sd"],
                                          round(self.calculate_angle(line1_start, line1_end, line2_start, line2_end), 2)]
        self.analysis_report["angle_analysis"] = angle_analysis
            
    def measurement_results(self):
        measurement_analysis = {}
        for measurement_name, measure_points in self.measurements.items():
            point1 = self.analysis_points[measure_points["measurement_points"][0]]
            point2 = self.analysis_points[measure_points["measurement_points"][1]]
            measure_type = measure_points["measure_type"]
            measurement_analysis[measurement_name] = [Config.measurements[measurement_name]["description"],
                                                      Config.measurements[measurement_name]["type"],
                                                      Config.measurements[measurement_name]["mean"],
                                                      Config.measurements[measurement_name]["sd"],
                                                      round(self.calculate_distance(point1, point2, measure_type), 2)]
        self.analysis_report["measurement_analysis"] = measurement_analysis
    
    def ratio_results(self):
        ratio_analysis = {}
        for ratio_name, ratio_details in self.ratios.items():
            ratio_analysis[ratio_name] = {}
            for ratio, ratio_feature in ratio_details.items():
                ratio_analysis[ratio_name][ratio] = {}
                distance = round(self.calculate_distance(self.analysis_points[ratio_feature["measurement_points"][0]],
                                                         self.analysis_points[ratio_feature["measurement_points"][1]], "vertical"), 2)
                ratio_analysis[ratio_name][ratio]["distance"] = distance
                ratio_analysis[ratio_name][ratio].update(ratio_feature["ratio_features"])
            ratios = list(ratio_analysis[ratio_name].keys())
            ratio_analysis[ratio_name][ratios[0]]["ratio"] = f'%{round((ratio_analysis[ratio_name][ratios[0]]["distance"] / (ratio_analysis[ratio_name][ratios[0]]["distance"] + ratio_analysis[ratio_name][ratios[1]]["distance"]))*100)}'
            ratio_analysis[ratio_name][ratios[1]]["ratio"] = f'%{round((ratio_analysis[ratio_name][ratios[1]]["distance"] / (ratio_analysis[ratio_name][ratios[0]]["distance"] + ratio_analysis[ratio_name][ratios[1]]["distance"]))*100)}'
            ratio_analysis[ratio_name][ratios[0]].pop("distance")
            ratio_analysis[ratio_name][ratios[1]].pop("distance")
            ratio_analysis[ratio_name][ratios[0]] = list(ratio_analysis[ratio_name][ratios[0]].values())
            ratio_analysis[ratio_name][ratios[1]] = list(ratio_analysis[ratio_name][ratios[1]].values())
        self.analysis_report["ratio_analysis"] = ratio_analysis
        
    def update_ratio_results(self, ratios):
        new_results = {}
        for ratio_results in ratios.values():
            new_results.update(ratio_results)
        return new_results
        
    def create_results_list(self):
        results_list = []
        for point, coordinates in self.analysis_points.items():
            format_dict = Config.cephalometric_landmarks.copy()
            format_dict["coordinates"] = [[int(coordinates[0]), int(coordinates[1])], [int(coordinates[0]), int(coordinates[1])]]
            format_dict["label"] = point
            results_list.append(format_dict)
        return results_list
        
    def get_measurement_points(self, measurement):
        point1 = Config.measurements[measurement]["measurement_points"][0]
        point2 = Config.measurements[measurement]["measurement_points"][1]
        coordinates = {"points" : [self.analysis_points[point1], self.analysis_points[point2]]}
        coordinates["measurement"] = self.analysis_report_dict["results"]["measurements"][measurement][4]
        return coordinates
        
    def get_ratio_measurements(self):
        ratio_measurements = {}
        for ratio_type, ratio_results in Config.ratios.items():
            for ratio_name, ratio_features in ratio_results.items():
                ratio_measurements[ratio_name] = {}
                point1 = ratio_features["measurement_points"][0]
                point2 = ratio_features["measurement_points"][1]
                ratio_measurements[ratio_name]["points"] = [self.analysis_points[point1], self.analysis_points[point2]]
                ratio_measurements[ratio_name]["ratio"] = self.analysis_report_dict["results"]["ratios"][ratio_type][ratio_name][4]
        return ratio_measurements

    
    def get_result_as_json(self):
        self.analysis_report_dict = Config.analysis_report_dict.copy()
        self.analysis_report_dict["calibration_points"]["calibration_points_xy"] = self.calibration_points
        self.analysis_report_dict["calibration_points"]["calibration_measure"] = self.calibration_measure
        self.analysis_report_dict["results"]["cephalometric_landmarks"] = self.create_results_list()
        self.analysis_report_dict["results"]["angles"] = self.analysis_report["angle_analysis"]
        self.analysis_report_dict["results"]["measurements"] = self.analysis_report["measurement_analysis"]
        self.analysis_report_dict["results"]["ratios"] = self.analysis_report["ratio_analysis"]
        self.analysis_report_dict["results"]["spline_points"] = [{point: self.analysis_points[point] for point in sublist} for sublist in Config.spline_points]
        self.analysis_report_dict["results"]["planes"] = {plane: [self.analysis_points[points[0]], self.analysis_points[points[1]]] for plane, points in Config.planes.items()}
        self.analysis_report_dict["results"]["measurement_points"] = {measurement: self.get_measurement_points(measurement) for measurement in Config.measurements}
        self.analysis_report_dict["results"]["ratio_measurements"] = self.get_ratio_measurements()
        self.analysis_report_dict["results"]["analysis_types"] = {analysis: {analysis_type: {result: self.analysis_report_dict["results"][analysis_type][result] for result in analysis_name} for analysis_type, analysis_name in content.items()} for analysis, content in Config.analysis_types.items()}

        self.analysis_report_dict["results"]["analysis_types"] = {analysis_type: {analysis_name: analysis if analysis_name != "ratios" else self.update_ratio_results(analysis) for analysis_name, analysis in analysis_results.items()} for analysis_type, analysis_results in self.analysis_report_dict["results"]["analysis_types"].items()}
        self.analysis_report_dict["results"]["angle_planes"] = {angle: [self.analysis_report_dict["results"]["planes"][Config.angles[angle]["angle_planes"][0]], self.analysis_report_dict["results"]["planes"][Config.angles[angle]["angle_planes"][1]]] for angle in Config.angles}
        # with open("result-v4.json", "w", encoding="utf-8") as f:
        #     json.dump(self.analysis_report_dict, f, indent = 4, ensure_ascii=False)
        return self.analysis_report_dict
    
    
# analyse = CephalometricAnalysis()
# analyse.load_image("2.png")
# analyse.calibration_points = [[1860, 340], [1860, 488]]
# analyse.calibration_measure = 20
# analyse.set_calculate_calibration_measure()
# analyse.get_points()
# analyse.angle_results()
# analyse.measurement_results()
# analyse.ratio_results()
# analyse.get_result_as_json()
from src.cases.point_detection.cephalometric.src.model import Farnet
from src.cases.point_detection.cephalometric.src.configv2 import Config
from src.cases.point_detection.cephalometric.src.utils import get_prepoint_from_htmp
import numpy as np
import cv2
import torch
import math
import json
import warnings

warnings.filterwarnings("ignore")


class CephalometricAnalysis():
    def __init__(self, image=None, calibration_points=[], calibration_measure=None, pixel_to_mm=10,
                 angles=Config.angles, measurements=Config.measurements, ratios=Config.ratios,
                 spline_points=Config.spline_points, model_point_names=Config.model_point_names, planes=Config.planes,
                 analysis_points=None, gender=None, analysis_report={}, analysis_report_dict={}):
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
        checkpoint = torch.load(Config.model_path)
        model.load_state_dict(checkpoint)
        return model.cuda(0)

    def set_calculate_calibration_measure(self):
        points_distance = math.hypot(self.calibration_points[0][0] - self.calibration_points[1][0],
                                     self.calibration_points[0][1] - self.calibration_points[1][1])
        self.pixel_to_mm = points_distance / self.calibration_measure

    def calculate_mid_point(self, point1, point2):
        return ((np.array(point1) + np.array(point2)) / 2).tolist()

    def get_points(self):
        img_h, img_w, _ = self.image.shape
        img_resize = cv2.resize(self.image, (Config.resize_w, Config.resize_h))
        img_data = np.transpose(img_resize, (2, 0, 1))
        img_data = np.reshape(img_data, (1, 3, Config.resize_h, Config.resize_w))
        img_data = torch.from_numpy(img_data).float().cuda()
        scal_ratio_w = img_w / Config.resize_w
        scal_ratio_h = img_h / Config.resize_h
        outputs, _ = self.model(img_data)
        outputs = outputs[0].detach().cpu().numpy()
        analysis_points = get_prepoint_from_htmp(outputs, scal_ratio_w, scal_ratio_h)
        self.analysis_points = {
            list(self.model_point_names.keys())[i]: [round(x, 2) for x in analysis_points[i].tolist()] for i in
            range(len(analysis_points))}
        self.get_additional_points()

    def get_additional_points(self):
        self.analysis_points["Mid Md1c-Mx1c"] = self.calculate_mid_point(self.analysis_points["Md1c"],
                                                                         self.analysis_points["Mx1c"])
        self.analysis_points["Mid L6o-U6o"] = self.calculate_mid_point(self.analysis_points["L6o"],
                                                                       self.analysis_points["U6o"])
        self.analysis_points["A processed point"] = self.find_projected_point(self.analysis_points["A point"],
                                                                              self.planes["Occlusal plane"])
        self.analysis_points["B processed point"] = self.find_projected_point(self.analysis_points["B point"],
                                                                              self.planes["Occlusal plane"])
        self.analysis_points["Li processed point"] = self.find_projected_point(
            self.analysis_points["Labiale inferior (Li)"], self.planes["Steiner's S plane"])
        self.analysis_points["Ls processed point"] = self.find_projected_point(
            self.analysis_points["Labrale superior (Ls)"], self.planes["Steiner's S plane"])

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
        return projected_point

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
            line1_start = self.analysis_points[self.planes[angle_feature["angle_plants"][0]][0]]
            line1_end = self.analysis_points[self.planes[angle_feature["angle_plants"][0]][1]]
            line2_start = self.analysis_points[self.planes[angle_feature["angle_plants"][1]][0]]
            line2_end = self.analysis_points[self.planes[angle_feature["angle_plants"][1]][1]]
            angle_analysis[angle_name] = [Config.angles[angle_name]["description"], Config.angles[angle_name]["type"],
                                          Config.angles[angle_name]["mean"], Config.angles[angle_name]["sd"],
                                          round(self.calculate_angle(line1_start, line1_end, line2_start, line2_end),
                                                2)]
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
        for ratio_name, ratio_feature in self.ratios.items():
            distance1 = self.calculate_distance(
                self.analysis_points[self.measurements[ratio_feature["ratio_heights"][0]]["measurement_points"][0]],
                self.analysis_points[self.measurements[ratio_feature["ratio_heights"][0]]["measurement_points"][1]],
                self.measurements[ratio_feature["ratio_heights"][0]]["measure_type"])
            distance2 = self.calculate_distance(
                self.analysis_points[self.measurements[ratio_feature["ratio_heights"][1]]["measurement_points"][0]],
                self.analysis_points[self.measurements[ratio_feature["ratio_heights"][1]]["measurement_points"][1]],
                self.measurements[ratio_feature["ratio_heights"][1]]["measure_type"])
            ratio_analysis[ratio_name] = [Config.ratios[ratio_name]["description"], Config.ratios[ratio_name]["type"],
                                          Config.ratios[ratio_name]["mean"], Config.ratios[ratio_name]["sd"],
                                          f'%{round((distance1 / distance2) * 100)}']
        self.analysis_report["ratio_analysis"] = ratio_analysis

    def create_results_list(self):
        results_list = []
        for point, coordinates in self.analysis_points.items():
            format_dict = Config.cephalometric_landmarks.copy()
            if point in Config.model_point_names.keys():
                format_dict["coordinates"] = [[int(coordinates[0]), int(coordinates[1])],
                                              [int(coordinates[0]), int(coordinates[1])]]
                format_dict["label"] = point
                results_list.append(format_dict)
        return results_list

    def get_result_as_json(self):
        self.analysis_report_dict = Config.analysis_report_dict.copy()
        self.analysis_report_dict["calibration_points"]["calibration_points_xy"] = self.calibration_points
        self.analysis_report_dict["calibration_points"]["calibration_measure"] = self.calibration_measure
        self.analysis_report_dict["results"]["cephalometric_landmarks"] = self.create_results_list()
        self.analysis_report_dict["results"]["angles"] = self.analysis_report["angle_analysis"]
        self.analysis_report_dict["results"]["measurements"] = self.analysis_report["measurement_analysis"]
        self.analysis_report_dict["results"]["ratios"] = self.analysis_report["ratio_analysis"]
        self.analysis_report_dict["results"]["spline_points"] = [
            {point: self.analysis_points[point] for point in sublist} for sublist in Config.spline_points]
        self.analysis_report_dict["results"]["planes"] = [
            {plane: [self.analysis_points[points[0]], self.analysis_points[points[1]]]} for plane, points in
            Config.planes.items()]

        # {key1: {key: {i: results[key][i] for i in value} for key, value in values.items()} for key1, values in analysis_types.items()}
        self.analysis_report_dict["results"]["analysis_types"] = {analysis: {
            analysis_type: {result: self.analysis_report_dict["results"][analysis_type][result] for result in
                            analysis_name} for analysis_type, analysis_name in content.items()} for analysis, content in
            Config.analysis_types.items()}
        # with open("result.json", "w") as f:
        #     json.dump(self.analysis_report_dict, f, indent = 4, ensure_ascii=False)
        return self.analysis_report_dict


# analyse = CephalometricAnalysis()
# analyse.load_image("bcb8fe49-3a3e-48b3-b641-d63a79d8fa44.jpg")
# analyse.calibration_points = [[1860, 340], [1860, 488]]
# analyse.calibration_measure = 20
# analyse.set_calculate_calibration_measure()
# analyse.get_points()
# analyse.angle_results()
# analyse.measurement_results()
# analyse.ratio_results()
# analyse.get_result_as_json()
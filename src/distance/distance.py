# -- coding: utf-8 --
import math # Бібліотека для праці з математичними функціями

# Дистанція між двома вершинами
class Distance:
    distance_result = 0

    # Метод пошуку дистанції
    def get_2d_distance(self, x1, y1, x2, y2):
        a_ = abs(x1 - x2) # катет а
        b_ = abs(y1 - y2) # катет б
        c_ = math.sqrt(a_**2 + b_**2) # гіпотенуза прямокутного трикутника
        self.distance_result = c_

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import random
import numpy as np
from scipy import stats
from datetime import datetime, time

# Create your views here.


class DataView(APIView):
    def get(self, request):
        # Verificar parámetros
        if request.query_params.get("grupo"):
            try:
                group = int(request.query_params.get("grupo"))
                if group > 100 or group < 0:
                    return Response(
                        {
                            "error": "El número del grupo debe ser un número entero entre 01 y 99."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except ValueError:
                return Response(
                    {"error": "El número del grupo debe ser un número entero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            timestamp = datetime.now()
            if group == 0:
                # Datos de ejemplo
                seed = group + int(timestamp.timestamp())
                sample_size = 4
                noise = stats.norm.rvs(size=sample_size, random_state=seed)
                colors = [
                    "negro",
                    "azul",
                    "café",
                    "gris",
                    "verde",
                    "naranja",
                    "rosado",
                    "morado",
                    "rojo",
                    "blanco",
                    "amarillo",
                ]
                variable_1 = np.random.randint(0, 100, sample_size)
                variable_2 = transform(variable_1) + noise
                variable_3 = random.sample(colors, sample_size)

                return Response(
                    {
                        "group": group,
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "sample_size": sample_size,
                        "variable_1": variable_1,
                        "variable_2": variable_2,
                        "variable_3": variable_3,
                    }
                )
            else:
                # Datos del proyecto
                distributions = [
                    "burr12",
                    "chi2",
                    "expon",
                    "f",
                    "fisk",
                    "gamma",
                    "laplace",
                    "lognorm",
                    "nakagami",
                    "rayleigh",
                    "rice",
                    "t",
                    "uniform",
                ]
                params = {
                    "burr12": (3, 3),
                    "chi2": (4,),
                    "expon": (),
                    "f": (5, 5),
                    "fisk": (3,),
                    "gamma": (2,),
                    "laplace": (),
                    "lognorm": (2,),
                    "nakagami": (2.12,),
                    "rayleigh": (),
                    "rice": (3,),
                    "t": (4,),
                    "uniform": (2, 3),
                }

                random.seed(group)
                dist_name = random.sample(distributions, 1)[0]
                dist_class = getattr(stats, dist_name)
                X = dist_class(*params[dist_name])
                sample_size = 100
                random_state = group + int(timestamp.timestamp())
                variable_1 = X.rvs(size=sample_size, random_state=random_state)
                variable_2 = transform(variable_1)
                variable_3 = transform(variable_2)

                return Response(
                    {
                        "group": group,
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "sample_size": sample_size,
                        "variable_1": variable_1,
                        "variable_2": variable_2,
                        "variable_3": variable_3,
                    }
                )
        else:
            return Response(
                {
                    "error": "Es necesario especificar el número del grupo como parámetros de la solicitud al API."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProcessView(APIView):
    def get(self, request):
        # Verificar parámetros
        if request.query_params.get("grupo"):
            try:
                group = int(request.query_params.get("grupo"))
                if group > 300 or (group < 100 and group != 0):
                    return Response(
                        {
                            "error": "El número del grupo debe ser un número entero entre 100 y 300."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except ValueError:
                return Response(
                    {"error": "El número del grupo debe ser un número entero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            timestamp = datetime.now()
            param, sunlight = time_variation(timestamp, group)

            distributions = [
                "expon",
                "gompertz",
                "levy",
                "logistic",
                "norm",
                "rayleigh",
            ]
            params = {
                "expon": (0, 1 + param),
                "gompertz": (1, 0, 1 + param),
                "levy": (0, 1 + param),
                "logistic": (2 * param, 1 + param),
                "norm": (3 * param, 1 + param),
                "rayleigh": (0, 1 + param),
            }

            random.seed(group)
            dist_name = random.sample(distributions, 1)[0]
            print(f"Distribución para grupo {group}: {dist_name}")
            dist_class = getattr(stats, dist_name)
            X = dist_class(*params[dist_name])
            sample_size = 100
            random_state = group + int(timestamp.timestamp())
            data = X.rvs(size=sample_size, random_state=random_state)

            return Response(
                {
                    "group": group,
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "sample_size": sample_size,
                    "sunlight": sunlight,
                    "data": data,
                }
            )
        else:
            return Response(
                {
                    "error": "Es necesario especificar el número del grupo como parámetro de la solicitud al API."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


def transform(x):
    return np.power(x, 0.5) + 1


def time_variation(timestamp, group):
    sunrise = time(6, 0, 0)
    sunset = time(18, 0, 0)
    today = datetime.today()
    # sunrise_datetime = datetime.combine(today, sunrise)
    # sunset_datetime = datetime.combine(today, sunset)
    # Determinación de la ecuación de la parábola
    # min_total = (sunset_datetime - sunrise_datetime).total_seconds() / 60
    # offset = min_total / 2
    # z1 = -offset
    # z2 = offset
    # Valor máximo
    # c = 2
    # Fórmula general
    # a1, b1, c1 = 4 * z1**2, 4 * z1, -4 * c
    # a2, b2, c2 = 4 * z2**2, 4 * z2, -4 * c
    # A = np.array([[a1, b1], [a2, b2]])
    # B = np.array([c1, c2])
    # solution = np.linalg.solve(A, B)
    # Coeficientes de la parábola
    # a, b = solution
    a, b, c = -1.54320987654321e-05, 0, 2
    offset = 360
    # Parámetro de la distribución
    if sunrise <= timestamp.time() <= sunset:
        min = (timestamp - datetime.combine(timestamp.date(), sunrise)).seconds / 60
        param = a * (min - offset) ** 2 + b * (min - offset) + c
        sunlight = True
    else:
        param = 0
        sunlight = False

    print(f"Valor del parámetro para el grupo {group}: {param}")

    return param, sunlight

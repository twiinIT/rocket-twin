motor_data = {"availability": "regular", "avgThrustN": 185, "burnTimeS": 6.87, "caseInfo": "RMS-54/1706", "certOrg": "Tripoli Rocketry Association, Inc.", "commonName": "K185", "dataFiles": 2, "delays": "6,8,10,12,14", "designation": "K185W", "diameter": 54, "impulseClass": "K", "length": 437, "manufacturer": "AeroTech", "manufacturerAbbrev": "AeroTech", "maxThrustN": 404.7, "motorId": "5f4294d2000231000000012d", "propInfo": "White Lightning", "propWeightG": 836.8, "samples": [[0, 0], [0.15, 279.1], [0.452, 308.2], [0.754, 328.4], [1.056, 338.9], [1.359, 339.7], [1.663, 333.2], [1.965, 321.9], [2.267, 309.7], [2.57, 293.3], [2.873, 271.5], [3.175, 247.2], [3.477, 216.9], [3.78, 187], [4.083, 161.1], [4.385, 138.1], [4.688, 117.7], [4.991, 99.37], [5.294, 82.76], [5.596, 68.43], [5.898, 55.13], [6.201, 44.16], [6.504, 34.21], [6.806, 25.06], [7.108, 16.88], [7.411, 9.2], [7.715, 0]], "totImpulseNs": 1417, "totalWeightG": 1434, "type": "reload", "updatedOn": "2019-04-17"}

import matplotlib.pyplot as plt

def thrustcurve(motor_name):
    global motor_data
    d = motor_data['samples']
    x = [d[i][0] for i in range(len(d))]
    y = [d[i][1] for i in range(len(d))]

    plt.plot(x,y)
    plt.xlabel('time (s)')
    plt.ylabel('impulse (N)')
    plt.title(f'{motor_name} thrust curve')
    plt.show()

thrustcurve("K185W")
import numpy as np

class DemandCurveModel:

    def fit_curve(self, prices, demand):
        """
        Fit a polynomial regression curve (degree=2) without sklearn.
        Returns polynomial coefficients and smoothed curve.
        """

        x = np.array(prices, dtype=float)
        y = np.array(demand, dtype=float)

        if len(x) < 3:
            # fallback if insufficient data
            coeffs = np.polyfit([1, 2, 3], [y.mean(), y.mean()*0.8, y.mean()*0.6], 2)
        else:
            coeffs = np.polyfit(x, y, 2)  # quadratic model

        # Generate smooth curve across price range
        x_line = np.linspace(min(x), max(x), 40)
        y_line = np.polyval(coeffs, x_line)

        # Smoothing (simple moving avg)
        window = 3
        y_smooth = np.convolve(y_line, np.ones(window)/window, mode='same')

        # Convert to points format for frontend
        points = [
            {"x": float(px), "y": float(py)}
            for px, py in zip(x_line, y_smooth)
        ]

        return {
            "coeffs": [float(c) for c in coeffs],
            "points": points
        }

    def analyze_curve(self, prices, demand):
        """
        Determine zones: underpricing, optimal, overpricing.
        Sensitivity: based on slope between endpoints.
        """

        # Basic slope for sensitivity
        slope = (demand[-1] - demand[0]) / (prices[-1] - prices[0] + 0.0001)

        if slope < -1.0:
            sensitivity = "High Sensitivity"
        elif slope < -0.3:
            sensitivity = "Moderate Sensitivity"
        else:
            sensitivity = "Low Sensitivity"

        # Zones based on mid quartiles
        p1 = prices[1] if len(prices) > 2 else prices[0]
        p2 = prices[-2] if len(prices) > 2 else prices[-1]

        return {
            "sensitivity": sensitivity,
            "zone_low": f"Below {p1} SAR → Underpricing (lost margin).",
            "zone_optimal": f"{p1}–{p2} SAR → Balanced demand zone.",
            "zone_high": f"Above {p2} SAR → Sharp demand drop.",
        }

    def generate(self, prices, demand):
        """
        Full pipeline: regression + smoothing + zone analysis
        """

        curve = self.fit_curve(prices, demand)
        zones = self.analyze_curve(prices, demand)

        return {
            "curve": curve,
            "zones": zones
        }

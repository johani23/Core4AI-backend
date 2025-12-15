import numpy as np

class ElasticityModel:

    def compute_regression(self, price_points, conversions, traffic, competitor_price):
        """
        Compute regression coefficients using normal equation.
        demand_norm = conversions/traffic
        Features: price, competitor_price, constant
        """

        price = np.array(price_points)
        conv = np.array(conversions)
        traffic = np.array(traffic) + 1  # avoid division by zero
        comp = np.array(competitor_price)

        # normalized demand = conversion rate
        demand_norm = conv / traffic

        # Design matrix
        X = np.vstack([price, comp, np.ones(len(price))]).T
        y = demand_norm

        try:
            beta = np.linalg.inv(X.T @ X) @ X.T @ y
        except:
            beta = np.array([0, 0, np.mean(y)])  # fallback

        return {
            "coef_price": float(beta[0]),
            "coef_competitor": float(beta[1]),
            "intercept": float(beta[2]),
            "demand_norm": demand_norm.tolist(),
        }

    def elasticity(self, price_points, conversions, traffic, competitor_price):
        reg = self.compute_regression(price_points, conversions, traffic, competitor_price)

        coef_price = reg["coef_price"]
        avg_price = np.mean(price_points)
        avg_conv_rate = max(0.001, np.mean(reg["demand_norm"]))

        elasticity_val = float(coef_price * (avg_price / avg_conv_rate))

        return {
            "elasticity": round(elasticity_val, 4),
            "details": reg
        }

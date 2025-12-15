import numpy as np

from engines.ml.elasticity_model import ElasticityModel
from engines.ml.demand_curve_model import DemandCurveModel
from engines.ml.evc_model import EVCModel


class PricingEngineV22:

    def __init__(self, competitor_db, feature_engine, audience_engine, scaling_engine, roi_engine):
        self.competitor_db = competitor_db
        self.feature_engine = feature_engine
        self.audience_engine = audience_engine
        self.scaling_engine = scaling_engine
        self.roi_engine = roi_engine

        # ML modules
        self.elasticity = ElasticityModel()
        self.curve_model = DemandCurveModel()
        self.evc_model = EVCModel()


    # ---------------------------------------------------
    # 🔥 FETCH COMPETITORS FOR THE CATEGORY
    # ---------------------------------------------------
    def competitor_prices(self, product_name):
        cat = product_name.lower().strip()
        comps = self.competitor_db.data.get(cat, [])

        if not comps:
            comps = [
                {"competitor": "Market Basic", "price": 100},
                {"competitor": "Market Pro", "price": 140},
                {"competitor": "Market Max", "price": 180},
            ]
        return [float(c["price"]) for c in comps]


    # ---------------------------------------------------
    # 🔥 FEATURE UTILITIES VIA FEATURE ENGINE
    # ---------------------------------------------------
    def compute_utilities(self, features):
        """
        Each feature scored → normalized → converted to utility value
        """
        utilities = []
        for f in features:
            score = self.feature_engine.compute_feature_score({f: 7})
            utility = round(score * 2.0, 2)
            utilities.append({"feature": f, "utility": utility})
        return utilities


    # ---------------------------------------------------
    # 🔥 PRICE → DEMAND SAMPLES (synthetic for now)
    # ---------------------------------------------------
    def synthetic_demand_samples(self, base_price):
        """
        Creates realistic synthetic samples until real data collection begins.
        """
        prices = []
        demand = []

        # 6 price points around base price
        for offset in [-15, -5, 0, 5, 15, 25]:
            p = max(10, base_price + offset)
            prices.append(p)

            # demand decay pattern
            d = max(5, int(140 - (p * np.random.uniform(0.3, 0.7))))
            demand.append(d)

        return prices, demand


    # ---------------------------------------------------
    # 🔥 FULL PRICING PIPELINE
    # ---------------------------------------------------
    def dynamic_price(self, product, persona, product_name=""):

        features = product.get("features", {})
        feature_list = list(features.keys())

        utilities = self.compute_utilities(feature_list)
        competitor_list = self.competitor_prices(product_name)

        # ============================================================
        # 1) GENERATE SYNTHETIC DEMAND SAMPLES
        # ============================================================

        base_price = np.random.randint(40, 80)
        prices, demand = self.synthetic_demand_samples(base_price)

        # ============================================================
        # 2) ELASTICITY MODEL
        # ============================================================
        elasticity_info = self.elasticity.elasticity(
            prices,
            conversions=demand,
            traffic=[200]*len(demand),
            competitor_price=[competitor_list[0]] * len(demand)
        )

        elasticity_val = elasticity_info["elasticity"]

        if elasticity_val < -1:
            sensitivity_label = "High Sensitivity"
        elif elasticity_val < -0.3:
            sensitivity_label = "Moderate Sensitivity"
        else:
            sensitivity_label = "Low Sensitivity"

        # ============================================================
        # 3) DEMAND CURVE (POLYNOMIAL + SMOOTHING)
        # ============================================================
        curve_info = self.curve_model.generate(prices, demand)

        # ============================================================
        # 4) EVC MODEL (Value-Based Prediction)
        # ============================================================
        evc_result = self.evc_model.compute(
            competitor_list,
            utilities,
            sensitivity_label
        )

        # ============================================================
        # 5) PRICE SCORING & WEIGHTED FUSION
        # ============================================================
        # Base weights
        w_elasticity = 0.35
        w_evc = 0.45
        w_competitor = 0.20

        recommended_elasticity = float(np.mean(prices)) + (elasticity_val * 10)
        recommended_competitor = float(np.mean(competitor_list) * 0.92)

        final_price = (
            evc_result["recommended_price"] * w_evc +
            recommended_elasticity * w_elasticity +
            recommended_competitor * w_competitor
        )

        final_price = round(max(10, final_price), 2)

        # ============================================================
        # 6) FINAL OUTPUT
        # ============================================================
        return {
            "final_price": final_price,
            "elasticity": elasticity_val,
            "sensitivity": sensitivity_label,
            "curve": curve_info,
            "evc": evc_result,
            "competitors": competitor_list,
        }

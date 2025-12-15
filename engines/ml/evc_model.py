import numpy as np

class EVCModel:

    def reference_price(self, competitor_prices):
        """
        Compute baseline reference price from competitor prices.
        """
        if not competitor_prices:
            return 100  # fallback baseline

        competitor_prices = np.array(competitor_prices, dtype=float)
        return float(np.median(competitor_prices))


    def compute_differentiation_value(self, utilities):
        """
        Sum up the economic value add from each feature.
        Each utility → SAR value mapped linearly.
        """

        if not utilities:
            return 0.0

        dollar_per_util = 12
        values = [
            {
                "feature": u["feature"],
                "utility": float(u["utility"]),
                "value": float(u["utility"]) * dollar_per_util,
            }
            for u in utilities
        ]

        diff_value = float(sum(v["value"] for v in values))
        return diff_value, values


    def compute_total_evc(self, reference_price, diff_value):
        """
        Basic EVC = reference price + feature differentiation value.
        """
        return float(reference_price + diff_value)


    def fair_price(self, total_evc):
        """
        Fair price = 85% of total EVC.
        """
        return float(round(total_evc * 0.85, 2))


    def premium_price(self, total_evc):
        """
        Premium price = 125% of total EVC.
        """
        return float(round(total_evc * 1.25, 2))


    def recommended_price(self, total_evc, sensitivity_label, diff_value):
        """
        Intelligent recommended price:
        - High sensitivity → lower bound
        - Moderate → midpoint
        - Low sensitivity → premium-leaning
        """

        fair = self.fair_price(total_evc)
        premium = self.premium_price(total_evc)

        # normalize differentiation to scale recommendation
        diff_factor = min(diff_value / 40, 1.5)

        if sensitivity_label == "High Sensitivity":
            return float(round(fair, 2))

        if sensitivity_label == "Moderate Sensitivity":
            mid = (fair + premium) / 2
            return float(round(mid * diff_factor, 2))

        # Low sensitivity → confident premium recommendation
        return float(round(premium * diff_factor, 2))


    def compute(self, competitor_prices, utilities, sensitivity_label):
        """
        Main pipeline → EVC results ready for API.
        """

        ref_price = self.reference_price(competitor_prices)

        diff_value, mapped_utilities = self.compute_differentiation_value(utilities)

        total_evc = self.compute_total_evc(ref_price, diff_value)

        fair = self.fair_price(total_evc)
        premium = self.premium_price(total_evc)

        recommended = self.recommended_price(
            total_evc,
            sensitivity_label,
            diff_value
        )

        return {
            "reference_price": ref_price,
            "differentiation_value": diff_value,
            "utilities": mapped_utilities,
            "total_evc": total_evc,
            "fair_price": fair,
            "premium_price": premium,
            "recommended_price": recommended,
        }

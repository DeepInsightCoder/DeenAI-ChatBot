from typing import Dict, Optional, Union
import logging
from .constants import (
    ZAKAT_NISAB_GOLD,
    ZAKAT_NISAB_SILVER,
    ZAKAT_RATE,
    GOLD_PRICE_PER_GRAM,
    SILVER_PRICE_PER_GRAM
)

class ZakatCalculator:
    def __init__(self):
        self.nisab_gold_value = ZAKAT_NISAB_GOLD * GOLD_PRICE_PER_GRAM
        self.nisab_silver_value = ZAKAT_NISAB_SILVER * SILVER_PRICE_PER_GRAM
        
    def calculate_zakat(self, assets: Dict[str, Union[float, int]]) -> Optional[Dict[str, float]]:
        """
        Calculate Zakat based on provided assets.
        
        Args:
            assets: Dictionary containing asset values:
                   - cash: Cash savings in USD
                   - gold: Gold in grams
                   - silver: Silver in grams
                   
        Returns:
            Dictionary containing Zakat calculations or None if below Nisab
        """
        try:
            # Calculate total asset value
            cash = float(assets.get('cash', 0))
            gold_weight = float(assets.get('gold', 0))
            silver_weight = float(assets.get('silver', 0))
            
            gold_value = gold_weight * GOLD_PRICE_PER_GRAM
            silver_value = silver_weight * SILVER_PRICE_PER_GRAM
            total_value = cash + gold_value + silver_value
            
            logging.info(f"Calculating Zakat for total assets worth: ${total_value:.2f}")
            
            # Check if total wealth meets Nisab threshold
            if total_value < min(self.nisab_gold_value, self.nisab_silver_value):
                logging.info("Assets below Nisab threshold - no Zakat due")
                return {
                    'status': 'below_nisab',
                    'total_value': total_value,
                    'nisab_gold': self.nisab_gold_value,
                    'nisab_silver': self.nisab_silver_value
                }
            
            # Calculate Zakat
            zakat_amount = total_value * ZAKAT_RATE
            
            return {
                'status': 'calculated',
                'total_value': total_value,
                'zakat_amount': zakat_amount,
                'gold_value': gold_value,
                'silver_value': silver_value,
                'cash_value': cash
            }
            
        except (ValueError, TypeError) as e:
            logging.error(f"Error calculating Zakat: {str(e)}")
            return None

    def get_nisab_values(self) -> Dict[str, float]:
        """Get current Nisab thresholds."""
        return {
            'gold': self.nisab_gold_value,
            'silver': self.nisab_silver_value
        }

"""
Portfolio optimization module using Modern Portfolio Theory.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import seaborn as sns

class PortfolioOptimizer:
    """Class for portfolio optimization using MPT."""
    
    def __init__(self, returns: pd.DataFrame):
        """
        Initialize portfolio optimizer.
        
        Args:
            returns (pd.DataFrame): Daily returns for assets
        """
        self.returns = returns
        self.cov_matrix = returns.cov()
        self.mean_returns = returns.mean()
        
    def calculate_portfolio_performance(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate portfolio return, volatility, and Sharpe ratio.
        
        Args:
            weights (np.ndarray): Portfolio weights
            
        Returns:
            Tuple[float, float, float]: Return, volatility, Sharpe ratio
        """
        portfolio_return = np.sum(self.mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def generate_efficient_frontier(self, num_portfolios: int = 10000) -> pd.DataFrame:
        """
        Generate efficient frontier.
        
        Args:
            num_portfolios (int): Number of random portfolios
            
        Returns:
            pd.DataFrame: Portfolio statistics
        """
        num_assets = len(self.mean_returns)
        results = []
        
        for _ in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            ret, vol, sharpe = self.calculate_portfolio_performance(weights)
            results.append({
                'Return': ret,
                'Volatility': vol,
                'Sharpe': sharpe,
                'weights': weights
            })
        
        return pd.DataFrame(results)
    
    def get_max_sharpe_portfolio(self) -> Dict[str, float]:
        """
        Find portfolio with maximum Sharpe ratio.
        
        Returns:
            Dict[str, float]: Optimal weights and metrics
        """
        from scipy.optimize import minimize
        
        def neg_sharpe(weights):
            _, _, sharpe = self.calculate_portfolio_performance(weights)
            return -sharpe
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(len(self.mean_returns)))
        
        result = minimize(neg_sharpe, 
                         num_assets * [1. / num_assets],
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints)
        
        weights = result.x
        ret, vol, sharpe = self.calculate_portfolio_performance(weights)
        
        return {
            'weights': weights,
            'return': ret,
            'volatility': vol,
            'sharpe': sharpe
        }
    
    def get_min_volatility_portfolio(self) -> Dict[str, float]:
        """
        Find portfolio with minimum volatility.
        
        Returns:
            Dict[str, float]: Optimal weights and metrics
        """
        from scipy.optimize import minimize
        
        def volatility(weights):
            _, vol, _ = self.calculate_portfolio_performance(weights)
            return vol
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(len(self.mean_returns)))
        
        result = minimize(volatility,
                         num_assets * [1. / num_assets],
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints)
        
        weights = result.x
        ret, vol, sharpe = self.calculate_portfolio_performance(weights)
        
        return {
            'weights': weights,
            'return': ret,
            'volatility': vol,
            'sharpe': sharpe
        }
    
    def plot_efficient_frontier(self, frontier_df: pd.DataFrame, 
                               max_sharpe: Dict, min_vol: Dict):
        """
        Plot efficient frontier with key portfolios.
        
        Args:
            frontier_df (pd.DataFrame): Frontier data
            max_sharpe (Dict): Max Sharpe portfolio
            min_vol (Dict): Min volatility portfolio
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot efficient frontier
        ax.scatter(frontier_df['Volatility'], frontier_df['Return'],
                  c=frontier_df['Sharpe'], cmap='viridis', alpha=0.5)
        ax.set_xlabel('Volatility (Risk)')
        ax.set_ylabel('Expected Return')
        ax.set_title('Efficient Frontier')
        
        # Mark key portfolios
        ax.scatter(max_sharpe['volatility'], max_sharpe['return'],
                  color='red', s=100, label='Max Sharpe Ratio', marker='*')
        ax.scatter(min_vol['volatility'], min_vol['return'],
                  color='blue', s=100, label='Min Volatility', marker='o')
        
        ax.legend()
        plt.colorbar(ax.collections[0], label='Sharpe Ratio')
        plt.tight_layout()
        plt.show()

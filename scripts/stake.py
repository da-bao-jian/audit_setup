from brownie import Contract, accounts
from brownie_tokens import MintableForkToken

def main():
	dai_addr = "0x6b175474e89094c44da98b954eedeac495271d0f"

	usdc_addr = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

	curve_registry_addr = "0x0000000022D53366457F9d5E68Ec105046FC4383"

	amount = 100_000 * 10 ** 18

	dai = MintableForkToken(dai_addr)
	dai._mint_for_testing(accounts[0], amount)

	registry = Contract(curve_registry_addr)
	pool_addr = registry.find_pool_for_coins(dai_addr, usdc_addr)
	pool = Contract(pool_addr)

	dai.approve(
		pool_addr,
		amount,
		{'from': accounts[0]}
	)

	pool.add_liquidity(
		[amount, 0, 0], 0,
		{"from": accounts[0]}
	)


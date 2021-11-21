
To run, 
```
pip install -r requirement
```

For testing, move contracts to `/contracts` folder and tests to `./tests` folder, then run
```
brownie test tests/<contract name>
```

#### All the audit scripts live in `./utils`

* To pull the original [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts) contracts into `/contracts` folder for fixing compiler errors (only works if import statements starts with "@openzeppelin"):
    ```
    python3 utils/fetch_openzeppelin.py <contract path: contracts/ERC20.sol>
    ```
* To show functions and their visibilities:
    ```
    python3 audit.py <contract path: contracts/ERC20.sol> <contract name: ERC20> <option: show-all> 
    ```
* To show `public` functions that should'be been declared `external`:
    ```
    python3 audit.py <contract path: contracts/ERC20.sol> <contract name: ERC20> <option: optimize-sig"> 
    ```
* To generate C-risk finding:
    ```
    python3 audit.py <contract path: contracts/ERC20.sol> <contract name: ERC20> <option: get-Crisk"> 
    ```

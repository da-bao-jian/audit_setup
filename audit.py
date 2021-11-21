from slither.slither import Slither, SlitherError
import sys
from utils.fetch_openzeppelin import fetch_openzeppelin
from utils.logs import *

class Audit:

    def __init__(self, contract_name: str, file_path: str):

        # initiate Slither  
        try:
            self.slither = Slither(file_path)
        except SlitherError as error:
            # if sol file uses the import statements with @openzeppelin, fetch_openzeppelin fetches the original open zeppelin contract
            print(error)
            # fetch_openzeppelin(file_path)
            print("if error is about importing @openzeppeling contract, you can run 'python3 utils/fetch_openzeppelin <contract path i.e. contracts/ERC20>'")
            exit(-1)

        # an array of slither.core.declarations.contract.Contract
        self.contracts = self.slither.get_contract_from_name(contract_name)
        if not self.contracts:
            print(f"Contract {contract_name} not found")
            exit(-1)
        if len(self.contracts) != 1:
            print("")

        # an instance of slither.core.declarations.contract.Contract
        self.contract = self.contracts[0]

    def show_all_functions_and_visibility(self):
        '''
        Show all the function names and their visibilities
        '''
        for function in self.contract.functions:
            print(f"Function name: {function.name}, Function Visibility: {function.visibility} \n")
    
    def _is_interface(self, contract):
        '''
        To see if the contract devlarer is an interface
        contract: slither.core.declarations.contract.Contract

        Used in _get_only_real_functions
        '''
        return contract.contract_kind == "interface"

    def _get_only_real_functions(self):
        '''
        filter all the interfaces
        '''
        return [f for f in self.contract.functions if not self._is_interface(f.contract_declarer)]

    def get_public_functions_not_used_internally(self):
        all_functions = self._get_only_real_functions()
        print("The following functions are declared as `public`, contain array function arguments, and are not invoked in any of the contracts contained within the project's scope: \n")
        for f in all_functions:
            all_calls = f.all_internal_calls()
            if f.visibility == "public" and len(all_calls) == 0 and f.name != "constructor":
                print(f"{f.canonical_name}")

    def get_functions_with_restricted_access(self):
        roles = set()
        all_functions = self._get_only_real_functions()
        print(f"In the contract `{self.contract.name}`, the role 'FILL IN' has the authority over the following function: \n")
        for f in all_functions:
            if len(f.modifiers) > 0:
                for mod in f.modifiers:
                    if "only" in mod.name:
                        role = mod.name.split("only")[1].lower()
                        print(f"- `{f.canonical_name}` allows the `{role}` to `FILL IN`;")
                        roles.add(role)

        if len(roles) == 1: 
            role = roles.pop()
            print(f"Any compromise to the `{role}` accounts may allow the hacker to take advantage of these functions. ")
        elif len(roles) == 0:
            print("No priviledged roles")
        else:
            segment = ""
            for role in roles:
                segment += "{role}, "
            segment = segment[:-1]
            print(f"Any compromise to the `{segment}` accounts may allow the hacker to take advantage of these functions. ")



if __name__ == "__main__":

    if len(sys.argv) != 4:
        print('Input format: python3 audity.py contracts/<contract.sol> <contract name> <functionality>')
        exit(-1)

    # use relative path to audit.py
    file_path = sys.argv[1]
    contract_name = sys.argv[2]
    functionality = sys.argv[3]
    audit = Audit(contract_name, file_path)

    if functionality == "show-all":
        audit.show_all_functions_and_visibility()
    elif functionality == "optimize-sig":
        audit.get_public_functions_not_used_internally()
    elif functionality == "get-Crisk":
        audit.get_functions_with_restricted_access()
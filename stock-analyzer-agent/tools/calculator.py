# exp gets directly calculated, but llm will be needed to explicitly mentioned in system prompt that use ** for exponent and not ^
from langchain_core.tools import tool

import numexpr as ne

@tool
def calculate(exp:str)->float|str :
    """
    Evaluates a mathematical expression using numexpr. 
    Use this for calculating growth rates, price differences, or valuation ratios.
    use ** for exponentiation instead of ^.
    Input should be a string like '100 * (1 + 0.05)**5.
    """
    print("Agent calculating!!!")
    try:
        result:float = float(ne.evaluate(exp))
        return result
    except Exception as e:
        return f"I couldn't calculate that. Error: {str(e)}. Please ensure you are sending a valid mathematical expression."

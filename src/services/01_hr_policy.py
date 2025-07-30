####################################################################
# Tools Usage: Function Calling for LLM
# Making all neccessary import
# instantiate the OpenAI API using API_KEY
####################################################################

from openai import OpenAI
# from mftool import Mftool
from pydantic import BaseModel, Field
import os
import json

os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

########################################################################
# Using the Pydantic BaseModel, define the structured output
########################################################################


class MFDetails(BaseModel):
    mf_name: str = Field(
        description="The name of the mutual fund scheme mentioned by the user"
    )
    units: float = Field(
        description="Total number of units held, this can be a float/decimal value"
    )
    asset_value: float = Field(
        description="This is the total current value in INR for the units held by user"
    )


class MfToolResponse(BaseModel):
    net_value: float = Field(
        description="The current value of the asset in INR(Indian Rupees) for the given MF name"
    )
    response: str = Field(
        description="A natural language response to the users question "
    )


###############################################################################
# Defining the function to call mftool to fetch Mutual fund information
###############################################################################

def create_vector_store:
    



def get_mfdetails(mf_name, units):
    mf = Mftool()
    sch_codes = mf.get_scheme_codes()
    sch_code = [key for key, val in sch_codes.items() if val == mf_name]

    asset_value = mf.calculate_balance_units_value(sch_code[0], units)
    if isinstance(asset_value, dict):
        value_net = asset_value.get("balance_units_value")
        return value_net
    else:
        msg = "return type is not dictionary"
        return msg


tools = [
    {
        "type": "function",
        "name": "get_mfdetails",
        "description": "Get total assset value in INR for provided fund name and number of units.",
        "parameters": {
            "type": "object",
            "properties": {"mf_name": {"type": "string"}, "units": {"type": "number"}},
            "required": ["mf_name", "units"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

input_messages = [
    {
        "role": "user",
        "content": "What's total value for 565.78 units of Franklin India Credit Risk Fund - Direct - Growth",
    }
]

response = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)

####################################################################################
# Append the previous messages and call the user defined function
####################################################################################

tool_call = response.output[0]
args = json.loads(tool_call.arguments)

result = get_mfdetails(args["mf_name"], args["units"])

################################################################################################
# Append the post function execution messages and again call the model to rephrase the response
################################################################################################
input_messages.append(tool_call)
input_messages.append(
    {
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result),
    }
)

#######################################################################################
# Calling LLM to produce a natural language response
#######################################################################################

response_2 = client.responses.create(
    model="gpt-4.1",
    input=input_messages,
    tools=tools,
)

print(response_2.output_text)

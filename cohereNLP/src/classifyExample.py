# Customer support tickets can come from all directions, and manually analyzing and routing information is an overwhelming job.
# A text classification system can help support teams accelerate this process. 
# It can augment a team’s capacity by automatically assigning each ticket to the right type or next action.

# Here we look at an example of classifying customer emails to an insurance company into four types of requests, 
# Finding policy details, Change account settings, Filing a claim and viewing status, and Cancelling coverage.

import cohere
from cohere.responses.classify import Example

# These are the training examples we give the model to show the classes we want it to classify. 
# Each example contains the text itself and the corresponding label, or class. 
# The minimum number of examples required is two per class.

api_key='GC8Ay3eFBB6DhjjTMTqmB3JZewNXcZtvZ0022xlr'
co = cohere.Client(api_key)

examples =[
  Example("How do I find my insurance policy?", "Finding policy details"),
  Example("How do I download a copy of my insurance policy?", "Finding policy details"),
  Example("How do I find my policy effective date?", "Finding policy details"),
  Example("When does my insurance policy end?", "Finding policy details"),
  Example("Could you please tell me the date my policy becomes effective?", "Finding policy details"),
  Example("How do I sign up for electronic filing?", "Change account settings"),
  Example("How do I change my policy?", "Change account settings"),
  Example("How do I sign up for direct deposit?", "Change account settings"),
  Example("I want direct deposit. Can you help with that?", "Change account settings"),
  Example("Could you deposit money into my account rather than mailing me a physical cheque?", "Change account settings"),
  Example("How do I file an insurance claim?", "Filing a claim and viewing status"),
  Example("How do I file a reimbursement claim?", "Filing a claim and viewing status"),
  Example("How do I check my claim status?", "Filing a claim and viewing status"),
  Example("When will my claim be reimbursed?", "Filing a claim and viewing status"),
  Example("I filed my claim 2 weeks ago but I still haven’t received a deposit for it.", "Filing a claim and viewing status"),
  Example("I want to cancel my policy immediately! This is nonsense.", "Cancelling coverage"),
  Example("Could you please help my end my insurance coverage? Thank you.",
  "Cancelling coverage"),
  Example("Your service sucks. I’m switching providers. Cancel my coverage.", "Cancelling coverage"),
  Example("Hello there! How do I cancel my coverage?", "Cancelling coverage"),
  Example("How do I delete my account?", "Cancelling coverage")
]

inputs=[" I want to change my password",
        "Does my policy cover prescription medication?"
        ]
response = co.classify(
    # model='large',
    inputs=inputs,
    examples=examples
)
# print(response.classifications)
print(response)

inputs=[" Am I still able to return my order?",  
        "When can I expect my package?",  
        "Do you ship overseas?",  ]
examples=[ Example("Do you offer same day shipping?", "Shipping and handling policy"),  
  Example("Can you ship to Italy?", "Shipping and handling policy"),  
	Example("How long does shipping take?", "Shipping and handling policy"),  
	Example("Can I buy online and pick up in store?", "Shipping and handling policy"),  
	Example("What are your shipping options?", "Shipping and handling policy"),  
	Example("My order arrived damaged, can I get a refund?", "Start return or exchange"),  
	Example("You sent me the wrong item", "Start return or exchange"),  
	Example("I want to exchange my item for another colour", "Start return or exchange"),  
	Example("I ordered something and it wasn't what I expected. Can I return it?", "Start return or exchange"),  
	Example("What's your return policy?", "Start return or exchange"),  
	Example("Where's my package?", "Track order"),  
	Example("When will my order arrive?", "Track order"),  
	Example("What's my shipping number?", "Track order"),  
	Example("Which carrier is my package with?", "Track order"),  
	Example("Is my package delayed?", "Track order")
    ]
response=co.classify(
    inputs=inputs,
    examples=examples
)
print(response)
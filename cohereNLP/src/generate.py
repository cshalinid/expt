import cohere


api_key='GC8Ay3eFBB6DhjjTMTqmB3JZewNXcZtvZ0022xlr'
co=cohere.Client(api_key)

response=co.generate(prompt="please explain to me LLMs working",)
print(response)
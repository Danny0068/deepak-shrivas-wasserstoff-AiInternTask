from query_llm import answer_query_with_context
from vector_store import add_to_vector_store

# Add test documents about climate policy
test_docs = [
    "The climate policy aims to reduce carbon emissions by 50% by 2030.",
    "Key measures include renewable energy subsidies and carbon pricing.",
    "The policy also focuses on protecting vulnerable communities from climate impacts.",
    "International cooperation is essential for effective climate action.",
    "Regular monitoring and reporting will ensure policy effectiveness."
]
test_ids = [f"climate_policy_para{i+1}" for i in range(len(test_docs))]

# Add documents to vector store
add_to_vector_store(test_docs, test_ids)

# Now query the LLM
response = answer_query_with_context("What are the key takeaways from the climate policy?")
print(response["answer"])
print(response["formatted_sources"])

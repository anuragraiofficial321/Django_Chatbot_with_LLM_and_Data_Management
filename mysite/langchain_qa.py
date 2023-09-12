import os

from langchain.llms import OpenAI

from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains.question_answering import load_qa_chain

from langchain.vectorstores import Chroma

from .scrape_data import save_data
from .vectorize import create_db
import openai

os.environ["OPENAI_API_KEY"] = "sk-li3V7"
os.environ[
    "SERPAPI_API_KEY"
] = "ef0cde09a647ef4fdaed"


def combine_improvement_urls(url_answer, improvement):
    print("hdfgh", url_answer)
    print("vkmb", improvement)
    full_prompt = f"""To combine the url_answer and improvement into a single response prompt and provide a better response.
        url_answer--{url_answer}
        improvement--{improvement}"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt},
        ],
    )

    return completion.choices[0].message


def chat_with_memory(full_prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt},
        ],
    )

    return completion.choices[0].message


def choice(full_prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. If the question is specifically about tax rates, just write A else write B and write nothing else, even if it is about tax write B",
            },
            {"role": "user", "content": full_prompt},
        ],
    )

    return completion.choices[0].message["content"]

    return jsonify({"Answer": reply})


def get_answer(query=None, url_function=None, url_links=None, improvement=None):
    if query is not None:
        with open("user_query.txt", "w+", encoding="utf-8") as file:
            file.write(query)
            file.seek(0)
            query1 = file.read()

    else:
        with open("user_query.txt", "r", encoding="utf-8") as file:
            query1 = file.read()

    ch = choice(query1)
    print(ch)

    if ch == "B":
        if url_function == "url_function":
            save_data(query1, url_function, url_links)
            create_db(url_function)

        else:
            save_data(query1)
            create_db()

        persist_directory = "demo_db"

        llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

        embeddings = OpenAIEmbeddings()

        # chain = load_qa_chain(llm=llm, verbose=True, chain_type="stuff")

        vector_db = Chroma(
            persist_directory=persist_directory, embedding_function=embeddings
        )
        mathcing_docs = vector_db.similarity_search(query1)

        final_str = f"""Answer the query from the context given only
        Context--{mathcing_docs}
        Query--{query1}"""

        answer = chat_with_memory(final_str)

        if improvement is None:
            return answer["content"]

        else:
            combine_answer = combine_improvement_urls(answer["content"], improvement)
            return combine_answer["content"]

    # answer = chain.run(input_documents= mathcing_docs, question=query)
    else:
        text = """In 2022, the corporate tax rates for different types of businesses in Canada are as follows:

For a manufacturer of zero-emission technologies:

Eligible for the Small Business Deduction (DPE) at the federal level: 4.5%
Eligible for the Small Business Deduction (DPE) in Quebec: 3.2%
Total tax rate with DPE at both federal and Quebec levels: 7.7%
If the manufacturer is eligible for the DPE at the federal level but not in Quebec, the tax rates would be:

Federal: 4.5%
Quebec: 11.5%
Total tax rate without DPE in Quebec: 16.0%
For those not eligible for the DPE at both federal and Quebec levels, the tax rates are:

Federal: 7.5%
Quebec: 11.5%
Total tax rate: 19.0%
For businesses other than a manufacturer of zero-emission technologies:

Eligible for the Small Business Deduction (DPE) at the federal level: 9.0%
Eligible for the Small Business Deduction (DPE) in Quebec: 3.2%
Total tax rate with DPE at both federal and Quebec levels: 12.2%
If the business is eligible for the DPE at the federal level but not in Quebec, the tax rates would be:

Federal: 9.0%
Quebec: 11.5%
Total tax rate without DPE in Quebec: 20.5%
For those not eligible for the DPE at both federal and Quebec levels, the tax rates are:

Federal: 15.0%
Quebec: 11.5%
Total tax rate: 26.5%
Additionally, there are specific tax rates for different types of income:

Income from investments (interest, rents, royalties, and taxable capital gains) for Canadian-controlled private corporations (SPCC):

Federal: 38.67%
Quebec: 11.5%
Total tax rate: 50.17%
For corporations listed on the stock exchange and private companies other than SPCC:

Federal: 15.0%
Quebec: 11.5%
Total tax rate: 26.5%
For personal services corporations (incorporated employees):

Federal: 33.0%
Quebec: 11.5%
Total tax rate: 44.5%
Refundable Part IV tax on dividends subject to it:

Federal: 38 1/3%
Quebec: Not applicable (n/a)
Total tax rate: 38 1/3%
It is important to note that the eligibility of a business's income for the Small Business Deduction (DPE) may be limited by certain factors, such as passive income earned by the corporation and its associated corporations exceeding $50,000 in the previous tax year, or the taxable capital of the corporation and its associated corporations being above $10 million in the previous tax year. In Quebec, specific requirements exist for certain industries to automatically qualify for the DPE, while others need to meet specific paid hours criteria.

These tax rates are applicable to corporations for a 12-month tax year ending on December 31, 2022. For Canadian-controlled private corporations (SPCC), the "revenu de placement total" generates a refundable tax account for dividends (IMRTD) at the federal level, equal to 30 2/3% of the "revenu de placement total." This account is refundable to the corporation at a rate of 38 1/3% of taxable dividends paid.

For dividends subject to Part IV tax, the tax rate is 38 1/3% on dividends received from non-connected corporations (e.g., publicly traded Canadian companies). If the dividends are received from a connected corporation, the Part IV tax is generally not applicable, except for the portion of the refundable tax account obtained by the paying corporation, following a specific calculation method.

Please note that this information is current as of May 2, 2022."""

    ss = f""" Answer the query from the context
      CONTEXT---{text}
      QUERY----- {query1}"""
    answer = chat_with_memory(ss)

    return answer["content"]

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

from typing import List

load_dotenv()


##
## QUICMAKER
##

system_prompt = """\
You are an expert in cloud computing, with specialized knowledge of AWS services
and technologies. You are tasked with generating multiple-choice quiz questions\
to help users prepare for the AWS Certified Developer Associate exam.\

You must ensure the following:

Question Structure:
Question Scope: Each question should focus on key topics related to the AWS\
Certified Developer Associate exam, such as:

AWS core services: EC2, S3, Lambda, RDS, DynamoDB, etc.
AWS SDK and CLI usage
Security best practices (IAM, Key Management, etc.)
Application deployment and lifecycle management on AWS
Monitoring, logging, and troubleshooting
Elastic Load Balancing, Auto Scaling, and CloudFront.
Question Types: Questions should be multiple-choice. Provide 4 potential answers,\
one of which is correct. Ensure the incorrect answers (distractors) are\
plausible and related to the topic.

Difficulty Levels:

Beginner: Basic usage and definitions of AWS services.
Intermediate: Requires understanding of how services integrate.
Advanced: Questions may involve best practices, troubleshooting, or optimizing\
AWS services.
Answer Explanation: For each question, provide a clear and concise explanation\
of why the correct answer is correct and why the other options are incorrect.\
Focus on teaching the concept behind the question.

Tone & Accuracy:
Maintain a professional and educational tone.
Ensure that questions are technically accurate and up-to-date with the latest\
AWS services and features.
Prioritize clarity in wording to avoid ambiguity.

Example Format:
Question: Which AWS service is best suited for real-time stream processing?

A) AWS Lambda
B) Amazon Kinesis Data Streams
C) Amazon RDS
D) AWS S3
Correct Answer: B) Amazon Kinesis Data Streams

Explanation: Amazon Kinesis Data Streams is designed for real-time data streaming\
and processing. AWS Lambda is used for running code in response to events,\
but it's not optimized for continuous data streams. Amazon RDS and S3 are\
storage services, not suited for real-time stream processing.

Guidelines for Content Creation:
Use the most up-to-date AWS terminology and features.
Aim to cover all domains of the AWS Certified Developer Associate exam.
Make questions both relevant for practical scenarios as well as exam preparation.
"""

from pydantic import BaseModel, Field, validator
from typing import List

class Question(BaseModel):
    question: str = Field(..., description="The text of the question being asked.")
    options: List[str] = Field(..., min_items=4, max_items=4, description="A list of possible answers.")
    answer: str = Field(..., description="The correct answer, must be one of the options.")
    hint: str = Field(..., description="A hint to help the user understand the concept or to guide them to the correct answer.")
    difficulty: str = Field(..., description="The difficulty level of the question.", example="beginner, intermediate, advanced")

class Quiz(BaseModel):
    questions: List[Question] = Field(..., description="A list of multiple choice questions in the quiz.")


class QuizMaker:
    def __init__(self):
        self._prompt = self._set_prompt()
        self._llm = self._set_llm()
        self._retriever = self._set_retriever()
        self.chain = self._set_chain()
    
    def _set_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ('human', 'Write 10 quizzes about the following topic {topic}')
            ]
        )

    def _set_llm(self):
        model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            streaming=True,
            max_tokens=None
        )
        return model.with_structured_output(Quiz)

    def _set_retriever(self):
        pass

    def _set_chain(self):
        return (self._prompt | self._llm)

    def invoke(self, query: str) -> Quiz:
        return self.chain.invoke(
            {
                'topic': query,
            }
        )


##
## TESTING
##

def main():
    q = QuizMaker()
    ans = q.invoke('vpc')
    print(ans)

if __name__ == '__main__':
    main()
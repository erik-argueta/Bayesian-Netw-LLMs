"""
Title: Programming Project 2 (Bayesian Networks with LLMs)
Authors: Erik Argueta, Jerico Avila, Jose Cervantes
"""

from aima.probability import *
from openai import OpenAI 
from pydantic import BaseModel, Field
from typing import Literal
import json
import os

# Use the NRP-issued key with the NRP endpoint.
client = OpenAI(
    api_key=os.environ["NRP_API_KEY"],
    base_url="https://ellm.nrp-nautilus.io/v1",
)
T, F = True, False

class DiagnosticExtraction(BaseModel):
    diagnosis: Literal["TB", "Cancer", "Bronchitis"]
    probability: float = Field(ge=0, le=1)
    
class Diagnostics:
    """ Use a Bayesian network to diagnose between three lung diseases """
    

    def __init__(self):
        '''
        Placing diagn_cancer within init so it can be shared with every instance of Diagnostics.  
        '''
        self.diagn_cancer = BayesNet([
        
                ('Asia', '', 0.01),                                             # P(+Asia) = 0.01
                ('Smoking', '', 0.5),                                           # P(+Smoking) = 0.5
                           
                ('TB', 'Asia', { (T): 0.05, (F): 0.01 }),                       # Var: TB; Parent: Asia; P(+TB | Asia) 
                ('Cancer', 'Smoking', {(T): 0.1, (F): 0.01}),                   # Var: Cancer; Parent: Smoking; P(+Cancer | Smoking)
                ('Bronchitis', 'Smoking', {(T): 0.6, (F): 0.3}),                # Var: Bronchitis; Parent: Smoking; P(+Bronchitis | Smoking)
                            
                ('TBorCancer', 'TB Cancer',                                     # Var: TBorCancer; Parents: TB & Cancer; P(+TBorCancer | TB, Cancer)
                    {
                        (T, T): 1.0,                                            # P(+TBorCancer | TB=True,  Cancer= True)
                        (T, F): 1.0,                                            # P(+TBorCancer | TB=True,  Cancer= False)
                        (F, T): 1.0,                                            # P(+TBorCancer | TB=False, Cancer= True)
                        (F, F): 0                                               # P(+TBorCancer | TB=False, Cancer= False)
                    }), 
        
                    ('Dyspnea', 'TBorCancer Bronchitis', 
                    {
                        (T, T): 0.9,                                            # P(+Dyspnea | TBorCancer = True, Bronchitis = True)
                        (T, F): 0.7,                                            # P(+Dyspnea | TBorCancer = True, Bronchitis = False)
                        (F, T): 0.8,                                            # P(+Dyspnea | TBorCancer = False, Bronchitis = True)
                        (F, F): 0.1                                             # P(+Dyspnea | TBorCancer = False, Bronchitis = False)
                    }),
                    
                    ('Xray', 'TBorCancer', {(T): 0.99, (F): 0.05})              # Var: xray; Parent: TBorCancer; P(+xray | TBorCancer)
            ])
        

    def diagnose (self, asia, smoking, xray, dyspnea):

        # ===============================================================================
        # Conversions to T/F values based on the fields in diangostics_gui
        # ===============================================================================
        conversion = {
            "Abnormal" : T,
            "Normal" : F,
            "Present": T,
            "Absent": F,
            "Yes" : T,
            "No" : F
        }


        """
        ===============================================================================
        Creating a dictionary, evidence, based on the conversions; omitting "NA"
            { "Asia" : T/F
            "Smoking" : T/F
            "Xray" : T/F
            "Dyspnea": T/F }
        ===============================================================================
        """
        evidence = {}
        if asia != "NA":
            evidence["Asia"]  = conversion[asia]
        if smoking != "NA":
            evidence["Smoking"] = conversion[smoking]
        if xray != "NA":
            evidence["Xray"] = conversion[xray]
        if dyspnea != "NA":
            evidence["Dyspnea"] = conversion[dyspnea]

        prompt = f"""
                The following is a Bayesian network used to determine the most likely disease.

                All variables are Boolean. Each probability below is for the variable
                being True. The probability of False is its complement.

                Network:
                - P(Asia=True) = 0.01
                - P(Smoking=True) = 0.5

                - P(TB=True | Asia=True) = 0.05
                - P(TB=True | Asia=False) = 0.01

                - P(Cancer=True | Smoking=True) = 0.1
                - P(Cancer=True | Smoking=False) = 0.01

                - P(Bronchitis=True | Smoking=True) = 0.6
                - P(Bronchitis=True | Smoking=False) = 0.3

                - TBorCancer is True exactly when TB or Cancer is True.

                - P(Dyspnea=True | TBorCancer=True, Bronchitis=True) = 0.9
                - P(Dyspnea=True | TBorCancer=True, Bronchitis=False) = 0.7
                - P(Dyspnea=True | TBorCancer=False, Bronchitis=True) = 0.8
                - P(Dyspnea=True | TBorCancer=False, Bronchitis=False) = 0.1

                - P(Xray=True | TBorCancer=True) = 0.99
                - P(Xray=True | TBorCancer=False) = 0.05

                The joint distribution factors as:
                P(Asia) * P(Smoking) * P(TB|Asia) * P(Cancer|Smoking) *
                P(Bronchitis|Smoking) * P(TBorCancer|TB,Cancer) *
                P(Dyspnea|TBorCancer,Bronchitis) * P(Xray|TBorCancer)

                Observed evidence:
                {json.dumps(evidence)}

                Any variable(s) not present from the evidence are unobserved.
                Do not assume unobserved variables are False.

                Calculate P(TB=True | evidence), P(Cancer=True | evidence),
                and P(Bronchitis=True | evidence).
                
                Return the disease with the highest posterior probability:
                - diagnosis: exactly "TB", "Cancer", or "Bronchitis"
                - probability: that disease's posterior probability, between 0 and 1
                """
                
        


                
        # Follow the same Chat Completions structure as the NRP example.
        print("Observed evidence:", evidence)
        completion = client.chat.completions.create(
            model="gpt-oss",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Solve the Bayesian diagnosis problem. Return only a JSON "
                        "object with diagnosis and probability fields. "
                        "Do not include Markdown fences or explanatory text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        content = completion.choices[0].message.content
        if not content:
            raise RuntimeError("ERROR: No diagnosis returned")

        # Validate the JSON response before passing the two values to the GUI.
        result = DiagnosticExtraction.model_validate_json(content)
        print("Diagnosis:", result.diagnosis, "Probability:", result.probability)
        return [result.diagnosis, result.probability]
